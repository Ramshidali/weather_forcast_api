from django.db import models

# Create your models here.
from django.db import models

class WeatherForecast(models.Model):
    timestamp = models.DateTimeField()
    temperature = models.FloatField()
    weather_condition = models.CharField(max_length=100)
    humidity = models.IntegerField()