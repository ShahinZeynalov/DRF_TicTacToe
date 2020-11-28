
from django.urls import path, include
from knox import views as knox_views
from .views import (
    RegisterAPIView, MyLoginView, UserAPIView
)

app_name = 'accounts'

urlpatterns = [
    # path('', include('knox.urls')),
    path('user', UserAPIView.as_view()),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='knox_login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),

]