from django.shortcuts import render
from django.contrib.auth import get_user_model, logout
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import CreateAPIView
from .serializers import UserCreateSerializer
from account_app.utils import CustomSwaggerAutoSchema

User = get_user_model()

class RegisterAPIView(CreateAPIView):
    model = User
    serializer_class = UserCreateSerializer

    @swagger_auto_schema(auto_schema=CustomSwaggerAutoSchema, request_body=UserCreateSerializer,)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)