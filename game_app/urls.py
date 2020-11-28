"""game_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from .views import (
    GameListAPIView, GameCreateAPIView, GameRetrieveDestroyAPIView,
    CheckGame, GameStatistic
)

urlpatterns = [
    path('', GameListAPIView.as_view(), name='games'),
    path('create/', GameCreateAPIView.as_view(), name='game-create'),
    path('statistic/', GameStatistic.as_view(), name='game-statistic'),
    path('<int:pk>/', GameRetrieveDestroyAPIView.as_view(), name='game-detail'),
    path('<int:pk>/check/', CheckGame.as_view(), name='check-game'),
]
