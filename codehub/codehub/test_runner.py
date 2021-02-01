from typing import List, ContextManager
from unittest.mock import patch

import django_nose
from django.test import override_settings
from django.test.runner import DiscoverRunner


class RequestsAreForbiddenInTests(AssertionError):
    pass


class CodehubTestRunner(django_nose.NoseTestSuiteRunner):
    def __init__(self, *args, **kwargs):
        assert isinstance(self, DiscoverRunner), (
            f"The {self.__class__.__name__} can only be applied to django.test.runner.DiscoverRunner, "
            "because it extends the DiscoverRunner.setup_test_environment() method.\n"
            "If third-party test runner does not inherit DiscoverRunner, it will not be affected "
            "by this mix-in.\n"
            "In this case you have to extend the TestRunner.run_tests() method, "
            "which is a protocol for being django 'TestRunner'. See:\n"
            "https://docs.djangoproject.com/en/2.2/topics/testing/advanced/#defining-a-test-runner"
        )
        self.test_environment_context_managers: List[ContextManager] = [
            patch(
                'requests.api.request',
                side_effect=RequestsAreForbiddenInTests(
                    "You must mock all code that calls requests.{get,post,...} in tests",
                ),
            ),
            override_settings(
                DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage',
                PASSWORD_HASHERS=(
                    'django.contrib.auth.hashers.MD5PasswordHasher',
                ),
                CACHES={
                    # Django does not clear cache between tests >:[
                    # This causes problems, for example, when running tests relying on
                    # extra_settings.models.Setting.get() method which tries to use cache before making query to
                    # database
                    'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'},
                },
            ),
        ]
        super().__init__(*args, **kwargs)

    def setup_test_environment(self, **kwargs):
        super().setup_test_environment(**kwargs)
        for cm in self.test_environment_context_managers:
            cm.__enter__()

    def teardown_test_environment(self, **kwargs):
        for cm in self.test_environment_context_managers:
            cm.__exit__(None, None, None)
        super().teardown_test_environment(**kwargs)
