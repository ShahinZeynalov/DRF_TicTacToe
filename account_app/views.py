from django.shortcuts import render
from django.contrib.auth import get_user_model, logout
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from .serializers import UserCreateSerializer, LoginUserSerializer, UserSerializer
from account_app.utils import CustomSwaggerAutoSchema
from knox.views import LoginView
from rest_framework import permissions, status

User = get_user_model()

class UserAPIView(RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class MyLoginView(LoginView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginUserSerializer

    @swagger_auto_schema(request_body=LoginUserSerializer)
    def post(self, request, format=None):
        serializer = LoginUserSerializer(data=request.data, context={'request': request})
        serializer.is_valid()
        if not serializer.is_valid(raise_exception=True):
            message = _("Unable to log in with provided credentials.")
            return Response({'message': message}, status=409)
        user = serializer.validated_data
        request.user = user
        token = super().post(request, format).data['token']
        response_data = {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'token': f"Token {token}"
        }
        return Response(response_data, status=status.HTTP_200_OK)



class RegisterAPIView(CreateAPIView):
    model = User
    serializer_class = UserCreateSerializer

    @swagger_auto_schema(auto_schema=CustomSwaggerAutoSchema, request_body=UserCreateSerializer,)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)