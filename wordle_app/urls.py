from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('guess/', views.submit_guess, name='submit_guess'),
    path('game-over/<int:session_id>/', views.game_over, name='game_over'),
    path('history/', views.history, name='history'),
    path('stats/', views.stats_view, name='stats_view'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='wordle_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]