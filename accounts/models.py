import os
from io import BytesIO
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.files.base import ContentFile
from django.utils import timezone
from PIL import Image


def nombre_imagen_personalizado(instance, filename):
    nombre, extension = os.path.splitext(filename)
    timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    return f"{instance.user.username}_{timestamp}{extension}"


class UserStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stats')
    total_score = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)
    consecutive_days = models.IntegerField(default=0)
    avg_score = models.IntegerField(default=0)
    last_play_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Estadísticas de {self.user.username}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=nombre_imagen_personalizado, null=True, blank=True)
    thumbnail = models.ImageField(upload_to=nombre_imagen_personalizado, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk and not self.image:
            super().save(*args, **kwargs)
            return
        
        if not self.pk:
            super().save(*args, **kwargs)
        
        if self.image:
            img = Image.open(self.image)
            formato = img.format or 'JPEG'
        
            def procesar_imagen_cuadrada(imagen, tamaño_final):
                ancho, alto = imagen.size
                
                #recortar
                lado = min(ancho, alto)
                izquierda = (ancho - lado) // 2
                superior = (alto - lado) // 2
                derecha = izquierda + lado
                inferior = superior + lado
                
                img_cuadrada = imagen.crop((izquierda, superior, derecha, inferior))
                
                #rediensionar
                img_final = img_cuadrada.resize((tamaño_final, tamaño_final), Image.Resampling.LANCZOS)
                
                return img_final
            
            # Imagen grande 512x512
            img_grande = procesar_imagen_cuadrada(img.copy(), 512)
            buffer_grande = BytesIO()
            img_grande.save(buffer_grande, format=formato, quality=95)
            self.image.save(
                f"{self.user.username}_grande.{formato.lower()}",
                ContentFile(buffer_grande.getvalue()),
                save=False
            )
            
            # Miniatura 256x256
            img_mini = procesar_imagen_cuadrada(img.copy(), 256)
            buffer_mini = BytesIO()
            img_mini.save(buffer_mini, format=formato, quality=90)
            self.thumbnail.save(
                f"{self.user.username}_mini.{formato.lower()}",
                ContentFile(buffer_mini.getvalue()),
                save=False
            )
            super().save(*args, **kwargs)

    def __str__(self):
        return f"Perfil de {self.user.username}"
    
@receiver(post_save, sender=User)
def crear_perfil_y_stats(sender, instance, created, **kwargs):
    if created:
        UserStats.objects.get_or_create(user=instance)
        Profile.objects.get_or_create(user=instance)
        
@receiver(pre_save, sender=Profile)
def borrar_imagenes_antiguas(sender, instance, **kwargs):
    if not instance.pk:
        return  # Es un objeto nuevo, no hay nada que borrar
    
    try:
        perfil_antiguo = Profile.objects.get(pk=instance.pk)
    except Profile.DoesNotExist:
        return  # No existe el perfil anterior
    
    # Borrar imagen grande si cambió o se limpió
    if perfil_antiguo.image and str(perfil_antiguo.image) != str(instance.image):
        try:
            if os.path.isfile(perfil_antiguo.image.path):
                os.remove(perfil_antiguo.image.path)
                print(f"✅ Signal borró imagen: {perfil_antiguo.image.path}")
        except Exception as e:
            print(f"❌ Error en signal borrando imagen: {e}")
    
    # Borrar miniatura si cambió o se limpió
    if perfil_antiguo.thumbnail and str(perfil_antiguo.thumbnail) != str(instance.thumbnail):
        try:
            if os.path.isfile(perfil_antiguo.thumbnail.path):
                os.remove(perfil_antiguo.thumbnail.path)
                print(f"✅ Signal borró miniatura: {perfil_antiguo.thumbnail.path}")
        except Exception as e:
            print(f"❌ Error en signal borrando miniatura: {e}")