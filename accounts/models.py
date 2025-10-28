from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stats')
    total_score = models.IntegerField(default=0)
    consecutive_days = models.IntegerField(default=0)
    max_streak = models.IntegerField(default=0)
    avg_response_time = models.FloatField(default=0.0)
    avg_score = models.IntegerField(default=0)
    last_play_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Estadísticas de {self.user.username}"



# 🚀 Crear automáticamente las estadísticas cuando se crea un nuevo usuario
@receiver(post_save, sender=User)
def create_user_stats(sender, instance, created, **kwargs):
    if created:
        UserStats.objects.create(user=instance)


# 🧩 Guardar automáticamente las estadísticas al guardar el usuario
@receiver(post_save, sender=User)
def save_user_stats(sender, instance, **kwargs):
    instance.stats.save()