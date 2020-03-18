import pyowm

owm = pyowm.OWM('6d00d1d4e704068d70191bad2673e0cc', language = "ua")

place = input('Введіть місто: ')

observation = owm.weather_at_place(place)
w = observation.get_weather()

press = w.get_pressure()["press"]               
humi = w.get_humidity()
temp = w.get_temperature('celsius')["temp"]

print("В місті " + place + " зараз " + w.get_detailed_status())
print("Температура – " + str(temp) + "C°")
print("Вологість – " + str(humi) + "%")
print("Тиск – " + str(press) + "hPa")

