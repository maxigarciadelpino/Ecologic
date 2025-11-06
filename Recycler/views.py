from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from accounts.models import UserStats
import random
import datetime
from django.contrib.auth.models import AnonymousUser

# Vista principal (menú del juego)
def recycler_view(request):
    return render(request, "recycler.html")


# Vista del quiz (preguntas del juego)
def quiz_view(request):
    # Lista de preguntas (con sus imágenes y respuestas correctas)
    PREGUNTAS = [
        {"image": "recycler/images/plastico.png", "correct": "Plástico", "options": ["Plástico", "Metal", "Vidrio", "Papel"]},
        {"image": "recycler/images/plastico2.png", "correct": "Plástico", "options": ["Plástico", "Metal", "Vidrio", "Papel"]},
        {"image": "recycler/images/plastico3.png", "correct": "Plástico", "options": ["Plástico", "Metal", "Vidrio", "Papel"]},
        {"image": "recycler/images/papel.png", "correct": "Papel", "options": ["Papel", "Plástico", "Vidrio", "Metal"]},
        {"image": "recycler/images/papel2.png", "correct": "Papel", "options": ["Papel", "Plástico", "Vidrio", "Metal"]},
        {"image": "recycler/images/papel3.png", "correct": "Papel", "options": ["Papel", "Plástico", "Vidrio", "Metal"]},
        {"image": "recycler/images/metal.png", "correct": "Metal", "options": ["Papel", "Plástico", "Vidrio", "Metal"]},
        {"image": "recycler/images/metal2.png", "correct": "Metal", "options": ["Papel", "Plástico", "Vidrio", "Metal"]},
        {"image": "recycler/images/metal3.png", "correct": "Metal", "options": ["Papel", "Plástico", "Vidrio", "Metal"]},
        {"image": "recycler/images/vidrio.png", "correct": "Vidrio", "options": ["Papel", "Plástico", "Vidrio", "Metal"]},
        {"image": "recycler/images/vidrio2.png", "correct": "Vidrio", "options": ["Papel", "Plástico", "Vidrio", "Metal"]},
        {"image": "recycler/images/vidrio3.png", "correct": "Vidrio", "options": ["Papel", "Plástico", "Vidrio", "Metal"]},
    ]

    # Mezclar las preguntas y seleccionar 10 al azar
    random.shuffle(PREGUNTAS)
    preguntas_seleccionadas = PREGUNTAS[:10]

    # Renderizar la plantilla del quiz con las preguntas
    return render(request, "quiz.html", {"questions": preguntas_seleccionadas})

def results_view(request):
    puntaje = int(request.GET.get("puntaje", 0))
    usuario = request.user

    if isinstance(usuario, AnonymousUser):
        return render(request, "results.html", {"puntaje": puntaje})

    estadisticas, _ = UserStats.objects.get_or_create(user=usuario)
    estadisticas.total_score += puntaje
    estadisticas.games_played = (estadisticas.games_played or 0) + 1

    if estadisticas.games_played > 0:
        promedio = estadisticas.total_score / estadisticas.games_played
        promedio_redondeado = round(promedio, -2)
        estadisticas.avg_score = int(promedio_redondeado)
    else:
        estadisticas.avg_score = 0

    # Actualizar los días consecutivos jugando
    hoy = timezone.now().date()
    ultima_fecha_jugada = estadisticas.last_play_date

    if ultima_fecha_jugada == hoy - datetime.timedelta(days=1):
        estadisticas.consecutive_days += 1
    elif ultima_fecha_jugada != hoy:
        estadisticas.consecutive_days = 1

    estadisticas.last_play_date = hoy

    estadisticas.save()

    return render(request, "results.html", {"puntaje": puntaje})

def leaderboard_view(request):
    jugadores = UserStats.objects.filter(games_played__gte=3).order_by("-consecutive_days", "-avg_score")[:100]
    return render(request, "leaderboard.html", {"jugadores": jugadores, "enumerate": enumerate})