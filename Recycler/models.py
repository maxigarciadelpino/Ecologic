from django.db import models

# Create your models here.
class Question(models.Model):
    image = models.ImageField(upload_to='Recycler/images/')
    correct_category = models.CharField(max_length=50)
    option_1 = models.CharField(max_length=50)
    option_2 = models.CharField(max_length=50)
    option_3 = models.CharField(max_length=50)
    option_4 = models.CharField(max_length=50)

    def __str__(self):
        return self.correct_category