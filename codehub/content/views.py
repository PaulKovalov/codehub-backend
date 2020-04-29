# Create your views here.
import urllib

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from content.models import ErrorMessage
from content.models import ImageSource
from content.search_engine import SearchEngine
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


class SearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get('query')
        if query is None:
            return Response()
        query = urllib.parse.unquote(query)
        if len(query) > settings.SEARCH_QUERY_MAX_LENGTH:
            raise ValidationError(f'Query is longer than {settings.SEARCH_QUERY_MAX_LENGTH}')
        search_engine = SearchEngine()
        return Response(data=search_engine.search(query))


@ensure_csrf_cookie
def get_csrf(request):
    return HttpResponse('')
