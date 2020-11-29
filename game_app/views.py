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
        return Game.objects.filter(user=user).order_by('-updated_at')

#creating a game.
class GameCreateAPIView(CreateAPIView):
    """
    Create a game by current user.
    """
    serializer_class = GameDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)


class GameRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    """
    RetrieveDestroyAPIView can get detail of the game or it can removed by user.
    """
    #passing a serializer class to return it in json format.
    serializer_class = GameDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Game.objects.all()


class CheckGame(GenericAPIView):
    """
    This endpoint represents the game which playing authenticated user and computer.
    When a user select a square and if game still continues computer makes a move too.

    if user wins the game of the result will be          1
    if computer wins the game of the result will be      2
    if game is draw the result of the game will be       -1
    if game stil continues it will return                0
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TileNumberSerializer
    queryset = Game.objects.all()

    @swagger_auto_schema(request_body=TileNumberSerializer)
    def put(self, request, pk):
        #Passing incoming data in TileSerializer class to vaildate
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = self.request.user
            try:
                #i
                game = user.games.get(id=pk)
            except:
                return Response({"message": "you have not any game with provided game id."}, status=status.HTTP_404_NOT_FOUND)
            #getting the number from validated data
            number = serializer.validated_data.get('number')
            #if game still continues the user will play.
            if game.result == 0:
                #game.play() methods raises error if not correct move.
                try:
                    #checking user move if number is correct else raises an error message.
                    game.play(int(number))
                    game.save()
                except Exception as e:
                    #Getting error message and return it.
                    return Response({"message": getattr(e, 'message', repr(e))[11:-2]}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                #after user move if game is continue computer play a move.
                if game.result == 0:
                    #computer plays a random move.
                    game.play_auto()
                    game.save()
                    #After computer move the result of the game returns updated data.
                    return Response({"result_code": game.result, "board": game.board}, status=status.HTTP_200_OK)
            # If game is finished returning the result of the game.
            return Response({"result_code": game.result, 'board': game.board}, status=status.HTTP_200_OK)
        #if serializer is not valid response returns error message
        return Response(serializer.error_messages, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class GameStatistic(APIView):
    """
    This api endpoint represents allover result of user games.
    """
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