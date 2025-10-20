from django.shortcuts import render, redirect
import random

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

    # Mezclar aleatoriamente y seleccionar 10
    random.shuffle(QUESTIONS)
    selected_questions = QUESTIONS[:10]

    # Renderizar la plantilla con las preguntas
    return render(request, "quiz.html", {"questions": selected_questions})


# Vista de resultados
def results_view(request):
    score = request.GET.get("score", 0)
    return render(request, "results.html", {"score": score})
