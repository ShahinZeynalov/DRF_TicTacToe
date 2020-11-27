from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from collections import Counter
import random

User = get_user_model()



class Game(models.Model):
    winning = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
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


    @property
    def is_game_over(self):
        """
        If the game is over and there is a winner, returns 'X' or 'O'.
        If the game is a stalemate, it returns ' ' (space)
        If the game isn't over, it returns None.
        The test is to simple check for each combination of winnable
        states --- across, down, and diagonals.
        If none of the winning states is reached and there are
        no empty squares, the game is declared a stalemate.
        """
        board = self.board
        for wins in self.winning:
            # Create a tuple
            w = (board[wins[0]], board[wins[1]], board[wins[2]])
            if w == ('X', 'X', 'X'):
                self.result = 1
                return 'X'
            if w == ('O', 'O', 'O'):
                self.result = 2
                return 'O'
        # Check for stalemate
        if '-' in board:
            self.result = 0
            return None
        self.result = -1
        return 'draw'

    @property
    def next_player(self):
        """
        Returns 'X' if the next play is player X, otherwise 'O'.
        This is easy to calculate based on how many plays have taken place:
        if X has played more than O, it's O's turn; otherwise, X plays.
        """
        # Counter is a useful class that counts objects.
        count = Counter(self.board)
        if count.get('X', 0) > count.get('O', 0):
            return 'O'
        return 'X'
        
    def play(self, index):
        
        """
        Plays a square specified by ``index``.
        The player to play is implied by the board state.
        If the play is invalid, it raises a ValueError.
        """
        index = index - 1
        if index < 0 or index >= 9:
            return "Invalid board index"

        if self.board[index] != '-':
            return "Square already played"

        # One downside of storing the board state as a string
        # is that you can't mutate it in place.
        board = self.board
        board[index] = self.next_player

    def play_auto(self):
        """Plays for any artificial/computers players.
        Returns when the computer players have played or the game is over."""
        
        if self.result == 0:
            unplayed_tiles = [i+1 for i, item in enumerate(self.board) if item == '-']
            computer_move = random.choice(unplayed_tiles)
            return self.play(computer_move)
            
        else:
            return self.result

# class Move(models.Model):
#     game = models.ForeignKey(Game, on_delete=models.CASCADE)
#     is_user = models.BooleanField()
#     number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)])


#     created_at = models.DateTimeField(auto_now_add=True) 

# class Tile(models.Model):
#     number = models.IntegerField()
#     sign = models.CharField(max_length=1, default='-')

#     updated_at = models.DateTimeField(auto_now=True)
    
