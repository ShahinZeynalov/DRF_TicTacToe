from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import GameDetailSerializer, GameListSerializer, TileNumberSerializer
from .models import Game
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import (
    ListAPIView, CreateAPIView, RetrieveUpdateAPIView, get_object_or_404,
    RetrieveUpdateDestroyAPIView, GenericAPIView, RetrieveDestroyAPIView
)
from rest_framework import permissions, filters, status
from rest_framework.response import Response
import json
"""
    https://www.django-rest-framework.org/api-guide/generic-views/
    Django’s generic views... were developed as a shortcut for common usage patterns... 
    They take certain common idioms and patterns found in view development and abstract them so that you can
    quickly write common views of data without having to repeat yourself.
"""
class GameListAPIView(ListAPIView):
    """
    Listing all of the games which created by current authhenticated user.
    """
    #https://pythondjangorestapi.com/django-advanced-rest-api-permissions/
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = GameListSerializer
    #we're using django-filtering package to filter games for game results.
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['result']

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Game.objects.filter(user=user)

#creating a game.
class GameCreateAPIView(CreateAPIView):
    serializer_class = GameDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

class GameRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    serializer_class = GameDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Game.objects.all()


class CheckGame(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TileNumberSerializer
    queryset = Game.objects.all()

    @swagger_auto_schema(request_body=TileNumberSerializer)
    def put(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = self.request.user
            try:
                game = user.games.get(id=pk)
            except:
                return Response({"message": "Game not found with this id"}, status=status.HTTP_404_NOT_FOUND)
            number = serializer.validated_data.get('number')
            if game.result == 0:
                try:
                    game.play(int(number))
                    game.save()
                except Exception as e:
                    return Response({"message": getattr(e, 'message', repr(e))[11:-2]}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                if game.result == 0:
                    game.play_auto()
                    game.save()
                    return Response({"result_code": game.result, "board": game.board}, status=status.HTTP_200_OK)
            return Response({"result_code": game.result, 'board': game.board}, status=status.HTTP_200_OK)
        return Response(serializer.error_messages, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class GameStatistic(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        user = self.request.user
        data = {}
        data['all'] = user.games.all().count()
        data['win'] = user.games.filter(result=1).count()
        data['lose'] = user.games.filter(result=2).count()
        data['draw'] = user.games.filter(result=-1).count()
        data['continue'] = user.games.filter(result=0).count()
        return Response({"data": data}, status=status.HTTP_200_OK)