from pprint import pprint

import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


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

# Чтання файлу google sheets стовпчик PRESURE
values = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='C2:C',
    majorDimension='ROWS'
).execute()

# Створив список "presureList" і записав у неї значення з словника "values" за ключем 'values'
pressureList = values.get('values')

# Створив список в який запишу дані float (дані телеметрії: атмосферний тиск)
pressureFloatList = []

# Записав дані типу float в новий список
for item in pressureList:
    pressureFloatList.append(float(item[0]))

# Роблю реверс списку і рахую кількість елементів масиву щоб відфільтрувати неактуальні дані
revPressureList = list(reversed(pressureFloatList))
lenList = len(revPressureList)

# Створюю змінну для актуальних даних
oneHourPressure = revPressureList
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

now = threeHoursPressure[0]
threeHoursAgo = threeHoursPressure[1]

#print()
print("Теперішні показники тиску: " + str(now) + "hPa")
print("Попередні показники тиску: " + str(threeHoursAgo) + "hPa")
print()

difference = now - threeHoursAgo
print("Різниця між показниками за останні 3 години складає: " + str("%.2f" % difference) + "hPa")
print()

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