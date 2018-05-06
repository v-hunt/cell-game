from django.urls import path, include

urlpatterns = [
    path('game/', include('my_game.api_v1.urls')),
]