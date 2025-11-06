from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from accounts.models import UserStats

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/accounts/")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("/accounts/")

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # crea el nuevo usuario
            login(request, user)  # inicia sesión automáticamente
            messages.success(request, "Cuenta creada correctamente")
            return redirect("/accounts/")  # redirige a la pagina de cuentas
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})

def profile_view(request):
    usuario = request.user

    if not usuario.is_authenticated:
        return render(request, "profile.html", {"usuario": None, "estadisticas": None})

    estadisticas = UserStats.objects.get(user=usuario)

    return render(request, "profile.html", {"usuario": usuario, "estadisticas": estadisticas})