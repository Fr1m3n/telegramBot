#Fr1m3n github.com/Fr1m3n

import requests
import json
import time

hi = set()
hi = {'привет', 'Привет', 'Дарова', 'Здравствуй', 'дарова', 'здравствуй', 'hi', 'hello', 'Hello'}
w = set()
w = {'Погода', 'погода', 'weather'}
help = set()
help = {'Помощь', 'помощь', 'help'}
#Множества слов для определения операции


url_bot = "https://api.telegram.org/bot536135996:AAFPk1NDzmbjolFSdCd64KDj-UsBAvracnY"
url_weather = "https://api.openweathermap.org/data/2.5/weather"
city_id = 487839
weather_token = "71d5c90dcb320f0e49bcb8af0c50fb41"


def get_weather_by_id(id):
    params = {"id": id, "APPID": weather_token}
    res = requests.get(url_weather, params)
    return res.json()


def get_temp(weath):
    return convert(weath["main"]["temp"])


def get_updates_json():
    res = requests.get(url_bot + "/getUpdates")
    return res.json()


def send_mes(id, text):
    print(id)
    params = {"chat_id": id, "text": text}
    res = requests.post(url_bot + '/sendMessage', data=params)


def get_id(update):
    id = update['message']['chat']['id']
    return id


def get_text(update):
    text = update['message']['text']
    return text

def last_update(data):
    results = data['result']
    total_updates = len(results) - 1
    return results[total_updates]


def convert(fhar):
    return fhar - 273.15


def generate_temp(weather):
    return ('--Ставрополь--\nТемпература: %.2f С°. \nСкорость ветра: %.2f. \nДавление: %.2f. \nУдачного дня!' % (get_temp(weather), weather["wind"]["speed"], weather["main"]["pressure"]))

#min - 4

def _main():
    weather = get_weather_by_id(city_id)
    weather_update_time = time.localtime()[4]
    #print(weather_update_time[4])
    temp = get_temp(weather)
    message = ''
    last_id = None
    while 1 == 1:
        if message == get_text(last_update(get_updates_json())):
            #print(message)
            continue
        now = time.localtime()
        if(min(now[4] - weather_update_time, now[4] + 60 - weather_update_time) >= 7 or time.localtime()[4] <= 8):
            weather = get_weather_by_id(city_id)
            weather_update_time = now[4]
        last_id = get_id(last_update(get_updates_json()))
        message = get_text(last_update(get_updates_json()))
        if (message in hi):
            send_mes(last_id, 'Привет!')
        elif (message in w):
            send_mes(last_id, generate_temp(weather))
        elif (message in help):
            send_mes(last_id, 'Отправь мне сообщение \'Погода\'.')
        else:
            send_mes(last_id, 'Я тебя не понимаю :c\nОтправь \'Помощь\'.')
        time.sleep(3)


if __name__ == "__main__":
    _main()
#weather = get_weather_by_id(city_id)
#print(json.dumps(weather, indent=4))
#print(get_text(last_update(get_updates_json())))