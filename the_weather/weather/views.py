import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm
import logging

logging.basicConfig(level=logging.DEBUG)


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=898ffc72e88c5f89c3d3274f84335e20'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        data = requests.get(url.format(city)).json()

        try:
            city_weather = {
                'city': city.name,
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
            }
        except KeyError:
            break

        weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather/weather.html', context)
