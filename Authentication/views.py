
from drf_yasg.utils import swagger_auto_schema
from Authentication.docs import schema_example
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model

from .serializers import SignUpSerializer, LoginSerializer, UserSerializer

from Helpers.response import Response
from rest_framework.views import APIView



class SignUpView(APIView):
    @swagger_auto_schema(
        operation_description="Sign up user",
        operation_summary="Sign up user",
        tags=["Auth"],
        request_body=SignUpSerializer,
        responses=schema_example.SIGN_UP_EXAMPLE,
    )
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginInView(APIView):
    @swagger_auto_schema(
        operation_description="Log in user",
        operation_summary="Log in user",
        tags=["Auth"],
        request_body=LoginSerializer,
        responses=schema_example.LOGIN_EXAMPLE,
    )    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = RefreshToken.for_user(user)
            data = {
                "token": {"refresh": str(token), 
                "access": str(token.access_token)},
            }
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    pass


class UsersView(APIView):
    @swagger_auto_schema(
        operation_description="Get Users",
        operation_summary="Get Users",
        tags=["Auth"],
    )    
    def get(self, request):
        User = get_user_model()
        return Response(
            data = {
                "users": UserSerializer(User.objects.all(), many=True).data,
            },
            status=status.HTTP_200_OK
        )

