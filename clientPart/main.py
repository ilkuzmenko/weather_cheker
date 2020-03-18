import os
import time
from progress.bar import IncrementalBar
import pyowm
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import colorama
from colorama import Fore, Back, Style
colorama.init()

# Progress bar 
bar = IncrementalBar('Processing', max = 10)
progressBar = [i for i in range(10)]
for item in progressBar[:1]:
    bar.next()
    time.sleep(0.05)


# Ініціалізую API openweathermap.org
owm = pyowm.OWM('6d00d1d4e704068d70191bad2673e0cc', language = "ua")
observation = owm.weather_at_place('Бориспіль')
w = observation.get_weather()
# Ініціалізую необхідні змінні з даними тиску, вологості, температури
press = w.get_pressure()["press"]
humi = w.get_humidity()
temp = w.get_temperature('celsius')["temp"]

# Файл Google Developer Console
CREDENTIALS_FILE = 'creds.json'
# ID Google Sheets
spreadsheet_id = '1fP8QlmM7sNZchGmdGMi5WVcdVjmhXMuGqVUnK3Sw7oI'

# Доступ до API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

######################################TEMPERATURE###########################################
# Чтання файлу google sheets стовпчик TEMPERATURE
valuesTemperature = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='B2:B',
    majorDimension='ROWS'
).execute()
# Створив список "temperatureList" і записав у неї значення з словника valuesTemperature за ключем 'values'
temperatureList = valuesTemperature.get('values')

# Створив список в який запишу дані float (дані телеметрії: атмосферний тиск)
temperatureFloatList = []

# Записав дані типу float в новий список
for item in temperatureList:
    temperatureFloatList.append(float(item[0]))

# Роблю реверс щоб підняти актуальні данні до верху списку
TemperatureList = list(reversed(temperatureFloatList))

# Progress bar 
for item in progressBar[1:4]:
    bar.next()
    time.sleep(0.05)


######################################HUMIDITY##############################################
# Чтання файлу google sheets стовпчик HUMIDITY
valuesHumidity = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='D2:D',
    majorDimension='ROWS'
).execute()
# Створив список "humidityList" і записав у неї значення з словника valuesHumidity за ключем 'values'
humidityList = valuesHumidity.get('values')

# Створив список в який запишу дані float (дані телеметрії: атмосферний тиск)
humidityFloatList = []

# Записав дані типу float в новий список
for item in humidityList:
    humidityFloatList.append(float(item[0]))

# # Роблю реверс щоб підняти актуальні данні до верху списку
HumidityList = list(reversed(humidityFloatList))

# Progress bar 
for item in progressBar[4:7]:
    bar.next()
    time.sleep(0.05)

######################################PRESURE###############################################
# Чтання файлу google sheets стовпчик PRESURE
valuesPressure = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='C2:C',
    majorDimension='ROWS'
).execute()

# Створив список "presureList" і записав у неї значення з словника valuesPressure за ключем 'values'
pressureList = valuesPressure.get('values')

# Створив список в який запишу дані float (дані телеметрії: атмосферний тиск)
pressureFloatList = []

# Записав дані типу float в новий список
for item in pressureList:
    pressureFloatList.append(float(item[0]))

# # Роблю реверс щоб підняти актуальні данні до верху списку і рахую кількість елементів масиву щоб відфільтрувати неактуальні дані
PressureList = list(reversed(pressureFloatList))
lenList = len(PressureList)

# Progress bar
for item in progressBar[7:10]:
    bar.next()
    time.sleep(0.05) 
bar.finish()
os.system('clear')

############################################################################################

# Створюю змінну для актуальних даних
oneHourPressure = PressureList
# Прибираю неактуальні дані зі списку
while lenList > 24 :
	oneHourPressure.pop()
	lenList -= 1

# Виводжу список актуальних даних з інтервалом в 1 годину за добу
#print("Дані телеметрії тиску з інтервалом в 1 годину за добу:")
#for item in oneHourPressure:
#	print(item)

#print()
#print()
#print()

# Роблю реверс списку і cтворюю змінну в яку записую дані з інтервалом в 3 години
threeHoursPressure = list(reversed(pressureFloatList))[::3]

# Рахую кількість елементів списку щоб забрати дані за 24 години
lenThreeHoursPressure = len(threeHoursPressure)

# Створюю змінну для актуальних даних за 24 години
twentyFourHoursPressure = threeHoursPressure

# Прибираю неактуальні дані зі списку
while lenThreeHoursPressure > 8 :
	twentyFourHoursPressure.pop()
	lenThreeHoursPressure -= 1

# Виводжу список актуальних даних з інтервалом в 3 години за добу
#print("Дані телеметрії тиску з інтервалом в 3 години за добу:")
#for item in threeHoursPressure:
#	print(item)



print()
print(Fore.YELLOW + "За даними ресурсу openweathermap.org:")
print("В місті Бориспіль зараз " + w.get_detailed_status())
print("Температура – " + str(temp) + "C°")
print("Вологість – " + str(humi) + "%")
print("Тиск – " + str(press) + "hPa" + Style.RESET_ALL)
print()
print(Fore.GREEN + "За даними зібраними за допомогою датчика BME280:")
print("В місті Бориспіль зараз " + w.get_detailed_status())
print("Температура – " + str(TemperatureList[0]) + "C°")
print("Вологість – " + str(HumidityList[0]) + "%")
print("Тиск – " + str(PressureList[0]) + "hPa" + Style.RESET_ALL)
print()
now = threeHoursPressure[0]
threeHoursAgo = threeHoursPressure[1]
difference = now - threeHoursAgo

if difference < 1.1 and difference > -1.1 :
	print("Різких змін погодних умов не прогнозується.")
elif difference >= 1.1 and difference <= 2.7 :
	print("Погода погіршується, вірогідність опадів мінімальна.")
elif difference > 2.7 and difference <= 6:
	print("Попередження про сильний вітер.")
elif difference > 6 :
	print("Попередження про бурю.")
elif difference <= -1.1 and difference >= -2.7 :
	print("Погода погіршується, вітряно, є вірогідність опадів.")
elif difference < -2.7 and difference >= -4 :
	print("Вірогідно буде дощ та вітряно.")
elif difference < -4 and difference >= -7 :
	print("Вірогідно буде шторм, попередження про сильний вітер.")
elif difference < -7 and difference >= -10 :
	print("Вірогідно буде гроза. ")
elif difference < -10 :
	print("Шторм, буря.")
else:
	print("error")
 
#print("Попередні показники тиску: " + str(threeHoursAgo) + "hPa")
#print("Теперішні показники тиску: " + str(now) + "hPa")
print("Різниця між показниками тиску за останні 3 години складає: " + str("%.2f" % difference) + "hPa")
print()



