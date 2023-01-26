from django.urls import path
from knox import views as knox_views
from .views import RegisterAPI, LoginAPI

urlpatterns = [
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path('register/', RegisterAPI.as_view()),
]