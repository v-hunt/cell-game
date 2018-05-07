from django.urls import path, include

urlpatterns = [
    path('game/', include('my_game.api_v1.urls')),
    path(r'auth/', include('rest_auth.urls'))
]