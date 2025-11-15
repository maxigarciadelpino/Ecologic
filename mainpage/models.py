from django.db import models

# Create your models here.
class PuntoVerde(models.Model):
    nombre = models.CharField(max_length=200)
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return self.nombre