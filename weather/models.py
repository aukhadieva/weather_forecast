from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Weather(models.Model):
    """
    Модель погоды.
    """
    location = models.CharField(max_length=50, verbose_name='город')
    temperature = models.FloatField(verbose_name='температура', **NULLABLE)
    datetime = models.DateTimeField(verbose_name='дата и время', **NULLABLE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)

    def __str__(self):
        return self.location

    class Meta:
        verbose_name = 'погода'
        verbose_name_plural = 'погода'
