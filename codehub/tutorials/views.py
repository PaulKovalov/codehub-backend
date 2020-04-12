# Create your views here.
from rest_framework import viewsets

from tutorials.models import Tutorial
from tutorials.permissions import TutorialPermission
from tutorials.serializers import TutorialSerializer, TutorialPreviewSerializer


class TutorialsViewSet(viewsets.ModelViewSet):
    permission_classes = [TutorialPermission]
    serializer_class = TutorialSerializer

    def get_queryset(self):
        qs = Tutorial.objects.filter(published=True)
        return qs

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'list':
            return TutorialPreviewSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
