from django.urls import path

from content import views

urlpatterns = [
    path('content/uploads/', views.UploadArticleImageView.as_view()),
]
