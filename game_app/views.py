from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import GameDetailSerializer, GameListSerializer
from .models import Game
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    ListAPIView, CreateAPIView, RetrieveUpdateAPIView, get_object_or_404,
    RetrieveUpdateDestroyAPIView, GenericAPIView, RetrieveDestroyAPIView
)
from rest_framework import permissions, filters


class GameListAPIView(ListAPIView):
    serializer_class = GameListSerializer
    filter_backends = [DjangoFilterBackend]
    queryset = Game.objects.all()
    filterset_fields = ['result']

class GameCreateAPIView(CreateAPIView):
    serializer_class = GameDetailSerializer
    permission_classes = (permissions.IsAuthenticated, )

class GameRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    serializer_class = GameDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Game.objects.all()

