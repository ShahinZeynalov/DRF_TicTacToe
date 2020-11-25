from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

class Game(models.Model):

    class Result(models.IntegerChoices):
        UWin = 1
        CWin = 2
        Draw = -1
        ND = 0

    
    def get_callable_board():
        return ['-', '-', '-', '-', '-', '-', '-', '-', '-']

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    result = models.IntegerField(choices=Result.choices, null=True, blank=True, default=0)
    board = ArrayField(
            models.CharField(max_length=1, blank=True), default=get_callable_board, 
            size=9
        )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Move(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    is_user = models.BooleanField()
    number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)])

    created_at = models.DateTimeField(auto_now_add=True)
