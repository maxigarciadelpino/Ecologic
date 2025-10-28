from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from accounts.models import UserStats
import random
import datetime


@login_required
def results_view(request):
    score = int(request.GET.get("score", 0))
    user = request.user

    # Obtener o crear las estadísticas
    stats, _ = UserStats.objects.get_or_create(user=user)

    # 1️⃣ Actualizar puntaje total
    stats.total_score += score

    # 2️⃣ Calcular puntaje promedio (redondeado a la centena)
    games_played = getattr(user, "games_played", 0) + 1
    avg_score = round(stats.total_score / games_played, -2)
    stats.avg_score = int(avg_score)
    user.games_played = games_played  # solo temporal si aún no tienes un campo en BD

    # 3️⃣ Actualizar racha máxima global
    current_streak = request.session.get("current_streak", 0)
    if current_streak > stats.max_streak:
        stats.max_streak = current_streak

    # 4️⃣ Actualizar días consecutivos jugando
    today = timezone.now().date()
    last_play_date = getattr(stats, "last_play_date", None)
    if hasattr(stats, "last_play_date"):
        if last_play_date == today - datetime.timedelta(days=1):
            stats.consecutive_days += 1
        elif last_play_date != today:
            stats.consecutive_days = 1
    else:
        stats.consecutive_days = 1
    stats.last_play_date = today

    # 5️⃣ (Opcional) Tiempo promedio de respuesta
    avg_response_time = request.session.get("avg_response_time", None)
    if avg_response_time:
        # Si ya había datos previos, hacer promedio nuevo
        if stats.avg_response_time == 0:
            stats.avg_response_time = avg_response_time
        else:
            stats.avg_response_time = (stats.avg_response_time + avg_response_time) / 2

    # Guardar cambios
    stats.save()

    return render(request, "results.html", {"score": score})


# Vista principal (menú del reciclador)
def recycler_view(request):
    return render(request, "recycler.html")

# Vista del quiz
def quiz_view(request):
    # Lista de preguntas (con rutas relativas a /static/)
    QUESTIONS = [
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

    # Mezclar preguntas y seleccionar 10
    random.shuffle(QUESTIONS)
    selected_questions = QUESTIONS[:10]

    # Mostrar la vista de la pagina con las preguntas seleccionadas
    return render(request, "quiz.html", {"questions": selected_questions})


# Vista de resultados
def results_view(request):
    score = request.GET.get("score", 0)
    return render(request, "results.html", {"score": score})
