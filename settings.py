import telebot
import os
from weather import WeatherBit

TOKEN_BOT = os.environ.get('BOT')

TOKEN_WEATHERBIT = os.environ.get('WEATHER')

bot = telebot.TeleBot(TOKEN_BOT)

weather = WeatherBit(TOKEN_WEATHERBIT)

lang = {
    'ru': {
        'success': 'Успешно.',
        'choose_lang': 'Пожалуйста выберите язык.',
        'city_not_found': 'Я не нашел такой город, повторите попытку.',
        'lang_save': 'Отлично, теперь напишите город в котором вы проживаете.',
        'city_save': 'Все данные сохранены успешно.',
        'registered': 'Вы уже зарегестрированы.',
        'change_city': 'Введите название города.',
        'success_change_city': 'Город был успешно изменен.',
        'status_upd': 'Статус изменен.',
    },
    'en': {
        'success': 'Success',
        'choose_lang': 'Please select your Language.',
        'city_not_found': 'I have not found such a city, try again.',
        'lang_save': 'Great, now write the city you live in.',
        'city_save': 'All data has been saved successfully.',
        'registered': 'You are already registered.',
        'change_city': 'Enter the name of the city.',
        'success_change_city': 'The city has been successfully changed.',
        'status_upd': 'Status changed.',
    }

}
