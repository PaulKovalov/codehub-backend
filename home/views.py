from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from home.models import ErrorMessage
from home.serializers import ErrorMessageSerializer


class ErrorMessagesViewSet(ReadOnlyModelViewSet):
    queryset = ErrorMessage.objects.filter(active=True)
    serializer_class = ErrorMessageSerializer
    permission_classes = [AllowAny]

    @action(methods=['GET'], detail=False)
    def current(self, request):
        error_object = self.queryset.latest()
        return Response(self.serializer_class(error_object).data)


@ensure_csrf_cookie
def get_csrf(request):
    return HttpResponse('')
