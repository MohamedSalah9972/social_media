from django.urls import path

from .views import ProfileAPIView, GetCustomFilter, ProfileRestBackendFilters

urlpatterns = [
    path('<int:pk>/', ProfileAPIView.as_view(), name='profile_views'),
    path('custom-filter/', GetCustomFilter.as_view(), name='get_custom_filter'),
    path('backend-filter/', ProfileRestBackendFilters.as_view(), name='profile_backend_filter'),
]