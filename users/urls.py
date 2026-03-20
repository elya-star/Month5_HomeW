from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegistrationAPIView.as_view()),
    path('auth/', views.LoginAPIView.as_view()),
    path('confirm/', views.ConfirmationAPIView.as_view()),
]