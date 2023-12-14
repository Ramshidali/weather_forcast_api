#standerd
import requests
from datetime import datetime
#django
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework import status
#third party
#local
from weather.models import WeatherForecast
from .serializers import WeatherForecastSerializer

@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def get_weather_forecast(request):
    
    if request.method == 'GET':
        try:
            timestamp = request.GET.get('timestamp')
            timestamp = int(timestamp)

            api_key = settings.WEATHER_API_KEY
            lat, lon = 11.2588, 75.7804
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                closest_time = min(data["list"], key=lambda x: abs(timestamp - x["dt"]))

                weather_info = {
                    "timestamp": datetime.utcfromtimestamp(closest_time["dt"]),
                    "temperature": closest_time["main"]["temp"],
                    "weather_condition": closest_time["weather"][0]["description"],
                    "humidity": closest_time["main"]["humidity"]
                }
                # Save weather data to the database
                serializer = WeatherForecastSerializer(data=weather_info)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response({'error': 'Data not saved'})
                # Return weather information
                return Response(weather_info)
            else:
                return Response({'error': 'Failed to fetch weather data'})
        except Exception as e:
            return Response({'error': str(e)})
