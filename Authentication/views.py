
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework import viewsets, status, permissions

from .serializers import SignUpSerializer, LoginSerializer

from Helpers.response import Response



class SignUpView(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_description="Sign up user",
        operation_summary="Sign up user",
        tags=["Auth"],
        request_body=SignUpSerializer
        # responses=schema_example.COMPLETE_REGISTRATION_RESPONSES,
    )
    @action(methods=['POST'], url_path="signup", detail=False)
    def sign_up(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        operation_description="Log in user",
        operation_summary="Log in user",
        tags=["Auth"],
        request_body=LoginSerializer
        # responses=schema_example.COMPLETE_REGISTRATION_RESPONSES,
    )    
    @action(methods=["POST"], url_path="login", detail=False)
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)