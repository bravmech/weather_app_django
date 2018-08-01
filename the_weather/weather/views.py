import requests
import logging

from django.shortcuts import render
from django.conf import settings

from .models import City
from .forms import CityForm

logging.basicConfig(level=logging.INFO)


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()
    form = CityForm()

    cities = City.objects.all()

    weather_data = []
    for city in cities:
        full_url = url.format(city, settings.OPENWEATHERMAP_KEY)
        data = requests.get(full_url).json()
        logging.info('requests.get: {}'.format(full_url))

        try:
            city_weather = {
                'city': city.name,
                'temperature': round(data['main']['temp'], 1),
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
            }
        except KeyError:
            logging.error('unexpected response')
            break

        weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather/weather.html', context)
