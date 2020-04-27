# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from content.models import ErrorMessage
from content.models import ImageSource
from content.serializers import ArticleImageSerializer
from content.serializers import ErrorMessageSerializer


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class UploadArticleImageView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        serializer = ArticleImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = ImageSource.objects.create(file=serializer.validated_data['file'])
        return Response({'location': image.source_url}, status=status.HTTP_201_CREATED)


class ErrorMessagesViewSet(ReadOnlyModelViewSet):
    queryset = ErrorMessage.objects.filter(active=True)
    serializer_class = ErrorMessageSerializer
    permission_classes = [AllowAny]


@ensure_csrf_cookie
def get_csrf(request):
    return HttpResponse('')
