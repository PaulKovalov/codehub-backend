from django.conf import settings
from model_mommy.recipe import Recipe

from accounts.models import User

user_recipe = Recipe(User,
                     avatar=settings.DEFAULT_AVATAR_URL
                     )
