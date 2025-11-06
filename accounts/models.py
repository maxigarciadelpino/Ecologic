from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserStats(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='stats',
        verbose_name="Usuario"
    )
    total_score = models.IntegerField(default=0, verbose_name="Puntaje total")
    games_played = models.IntegerField(default=0, verbose_name="Partidas jugadas")
    consecutive_days = models.IntegerField(default=0, verbose_name="Días consecutivos jugando")
    avg_score = models.IntegerField(default=0, verbose_name="Puntaje promedio")
    last_play_date = models.DateField(null=True, blank=True, verbose_name="Última fecha jugada")

    class Meta:
        verbose_name = "Estadística de usuario"
        verbose_name_plural = "Estadísticas de usuarios"

    def __str__(self):
        return f"Estadísticas de {self.user.username}"


# Crear automáticamente las estadísticas al crear un nuevo usuario
@receiver(post_save, sender=User)
def crear_estadisticas_usuario(sender, instance, created, **kwargs):
    if created:
        UserStats.objects.create(user=instance)


# Guardar automáticamente las estadísticas al guardar el usuario
@receiver(post_save, sender=User)
def guardar_estadisticas_usuario(sender, instance, **kwargs):
    instance.stats.save()