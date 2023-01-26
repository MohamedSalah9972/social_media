from django.urls import path

from .views import ProfileAPIView

urlpatterns = [
    path('<int:pk>/', ProfileAPIView.as_view(), name='profile_views'),
]