from rest_framework.routers import DefaultRouter

from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import SignUpView


routers = DefaultRouter(trailing_slash=False)

routers.register("", SignUpView, basename="auth")

urlpatterns = routers.urls