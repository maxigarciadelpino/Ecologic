import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from accounts.models import UserStats, Profile
from .forms import ImagenPerfilForm
from django.utils import timezone

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
            user = form.save()
            messages.success(request, "Tu cuenta se ha creado correctamente.")
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "accounts/register.html", {"form": form})

def profile_view(request):
    usuario = request.user
    
    if not usuario.is_authenticated:
        return render(request, "profile.html", {
            "usuario": None,
            "estadisticas": None,
            "perfil": None,
            "form": None,
            "now": timezone.now().timestamp()
        })
    
    estadisticas = UserStats.objects.get(user=usuario)
    perfil, _ = Profile.objects.get_or_create(user=usuario)
    
    if request.method == 'POST':
        if 'borrar_imagen' in request.POST:
            print("🔔 Botón Reiniciar Foto presionado")
            
            if perfil.image:
                try:
                    ruta_imagen = perfil.image.path
                    if os.path.isfile(ruta_imagen):
                        os.remove(ruta_imagen)
                        print(f"✅ Imagen borrada: {ruta_imagen}")
                except Exception as e:
                    print(f"❌ Error borrando imagen: {e}")
            
            if perfil.thumbnail:
                try:
                    ruta_mini = perfil.thumbnail.path
                    if os.path.isfile(ruta_mini):
                        os.remove(ruta_mini)
                        print(f"✅ Miniatura borrada: {ruta_mini}")
                except Exception as e:
                    print(f"❌ Error borrando miniatura: {e}")
            
            perfil.image = None
            perfil.thumbnail = None
            perfil.save()
            
            messages.success(request, "Imagen de perfil eliminada correctamente.")
            return redirect('profile')
        
        form = ImagenPerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, "Imagen de perfil actualizada correctamente.")
            return redirect('profile')
        else:
            messages.error(request, "Error al subir la imagen.")
    else:
        form = ImagenPerfilForm(instance=perfil)
    
    return render(request, "profile.html", {
        "usuario": usuario,
        "estadisticas": estadisticas,
        "perfil": perfil,
        "form": form,
        "now": timezone.now().timestamp()
    })