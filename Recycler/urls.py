from django.urls import path
from . import views

urlpatterns = [
    path('', views.recycler_view, name='recycler'),
    path('quiz/', views.quiz_view, name='start_quiz'),
    path('results/', views.results_view, name='results'),
]
