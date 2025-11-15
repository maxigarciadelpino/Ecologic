from django.urls import path
from . import views
from .views import maps_view, puntos_verdes_cercanos

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_view, name='about'),
    path('mapaverde/', maps_view, name='map'),
    path('api/puntos-verdes/', puntos_verdes_cercanos, name='api_puntos_verdes'),
]
