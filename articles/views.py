"""
Codehub Article API endpoints
Pavlo Kovalov 2019
"""
from .serializers import ArticleSerializer
from .permissions import ArticlePermission
from codehub import config
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

class ArticlesViewSet(viewsets.ModelViewSet):
	permission_classes = [ArticlePermission]
	serializer_class = ArticleSerializer
	
	def get_queryset(self):
		starting_from = self.request.data.get('from', 0)
		data = Article.objects.filter(published=true).order_by('-id')[starting_from: 10 + starting_from]
		return data

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)