from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from accounts.models import UserStats
import random
import datetime


@login_required
def results_view(request):
    puntaje = int(request.GET.get("puntaje", 0))
    usuario = request.user

    # Obtener o crear las estadísticas del usuario
    estadisticas, _ = UserStats.objects.get_or_create(user=usuario)

    # Actualizar puntaje total
    estadisticas.total_score += puntaje

    # Calcular el puntaje promedio (redondeado a la centena más cercana)
    partidas_jugadas = getattr(usuario, "partidas_jugadas", 0) + 1
    puntaje_promedio = round(estadisticas.total_score / partidas_jugadas, -2)
    estadisticas.avg_score = int(puntaje_promedio)
    usuario.partidas_jugadas = partidas_jugadas

    # Actualizar la racha máxima global
    racha_actual = request.session.get("racha_actual", 0)
    if racha_actual > estadisticas.max_streak:
        estadisticas.max_streak = racha_actual

    # Actualizar los días consecutivos jugando
    hoy = timezone.now().date()
    ultima_fecha_jugada = getattr(estadisticas, "last_play_date", None)
    if hasattr(estadisticas, "last_play_date"):
        if ultima_fecha_jugada == hoy - datetime.timedelta(days=1):
            estadisticas.consecutive_days += 1
        elif ultima_fecha_jugada != hoy:
            estadisticas.consecutive_days = 1
    else:
        estadisticas.consecutive_days = 1
    estadisticas.last_play_date = hoy

    # (Opcional) Calcular tiempo promedio de respuesta
    tiempo_promedio_respuesta = request.session.get("tiempo_promedio_respuesta", None)
    if tiempo_promedio_respuesta:
        # Si ya había datos previos, recalcular el promedio
        if estadisticas.avg_response_time == 0:
            estadisticas.avg_response_time = tiempo_promedio_respuesta
        else:
            estadisticas.avg_response_time = (
                estadisticas.avg_response_time + tiempo_promedio_respuesta
            ) / 2

    # Guardar los cambios en la base de datos
    estadisticas.save()

    return render(request, "results.html", {"puntaje": puntaje})


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


# Vista de resultados (simple, usada al final del juego)
def results_view(request):
    puntaje = request.GET.get("puntaje", 0)
    return render(request, "results.html", {"puntaje": puntaje})
