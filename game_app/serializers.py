from rest_framework import serializers
from .models import Game
# from rest_framework.fields import CurrentUserDefault

class GameListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'result', 'created_at', 'updated_at']

class GameDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Game
        fields = '__all__'
        read_only_fields = ['id', 'user', 'result', 'board', 'created_at', 'updated_at']