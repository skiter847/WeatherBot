from settings import *
from telebot import types
from user import User
from sql import DB


# TODO: implement a weather distribution system, for example, send message with weather for tomorrow in 22:00


def change_city_step(message, user):
    updates = user.update_city(message.text)
    if updates:
        bot.send_message(user.tg_id, lang[user.lang]['success_change_city'])
    else:
        bot.register_next_step_handler(message, change_city_step, user)


def city_step(message, user):
    """
    2/2 step to create user in database
    """
    response = WeatherBit.check_city(message.text.title(), weather)
    if response:
        user.city = message.text.title()
        user.add_to_db()
        user.create_user_menu()
    else:
        bot.send_message(message.chat.id, lang[user.lang]['city_not_found'])
        bot.register_next_step_handler(message, city_step, user)


def lang_step(message, user):
    """
    1/2 step to create user in database

    """
    if 'Русский' in message.text:
        user.lang = 'ru'
        bot.send_message(message.chat.id, lang[user.lang]['lang_save'])
        bot.register_next_step_handler(message, city_step, user)
    elif 'English' in message.text:
        user.lang = 'en'
        bot.send_message(message.chat.id, lang[user.lang]['lang_save'])
        bot.register_next_step_handler(message, city_step, user)


def choose_lang():
    return types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=1, one_time_keyboard=True).row('Русский🇷🇺',
                                                                                                 'English🇺🇸')


@bot.message_handler(commands=['start'])
def start_command(message):
    user = User()
    if user.exist(message.chat.id) is None:
        user.tg_id = message.chat.id
        user.first_name = message.from_user.first_name
        bot.send_message(message.chat.id, 'Please select your Language', reply_markup=choose_lang())
        bot.register_next_step_handler(message, lang_step, user)
    else:
        user.get(message.chat.id)
        bot.send_message(message.chat.id, lang[user.lang]['registered'])
        user.create_user_menu()


@bot.message_handler(
    func=lambda message: True if message.text == 'Прогноз на сегодня' or message.text == 'Forecast today' else False)
def forecast_today(message):
    user = User()
    user.get(message.chat.id)
    result = weather.get_current_weather(user)
    if user.lang == 'ru':
        bot.send_message(user.tg_id, f"""
Время: {result['ob_time']}
Город: {result['city_name']}
Скорость ветра (По умолчанию м/с): {result['wind_spd']} мс
Температура: {result['temp']}
Давление: {result['rh']} (Па)
Часть дня: {'День' if result['pod'] == 'd' else 'Ночь'}
Погода: {result['weather']['description']}
        """)
    else:
        bot.send_message(user.tg_id, f"""
Time: {result['ob_time']}
City: {result['city_name']}
Wind speed (Default m/s): {result['wind_spd']} ms
Temperature: {result['temp']}
Humidity: {result['rh']} (Pa)
Part of the day: {'Day' if result['pod'] == 'd' else 'Night'}
Weather: {result['weather']['description']}
""")


@bot.message_handler(func=lambda message: True if 'Подписка' in message.text or 'Subscribe' in message.text else False)
def upd_subscribe(message):
    user = User()
    user.get(message.chat.id)
    user.update_subscribe()


@bot.message_handler(
    func=lambda message: True if message.text == 'Сменить город' or 'Change city' == message.text else False)
def change_city(message):
    user = User()
    user.get(message.chat.id)
    bot.send_message(message.chat.id, lang[user.lang]['change_city'])
    bot.register_next_step_handler(message, change_city_step, user)


@bot.message_handler(
    func=lambda message: True if message.text == 'Прогноз на завтра' or 'Forecast tomorrow' == message.text else False)
def forecast_tomorrow(message):
    user = User()
    user.get(message.chat.id)
    result = weather.get_tomorrow_weather(user)
    if user.lang == 'ru':
        bot.send_message(user.tg_id, f"""

Дата: {result['data'][-1]['timestamp_utc'].split('T')[0]}
Город: {result['city_name']}
Скорость ветра (По умолчанию м/с): {result['data'][-1]['wind_spd']} мс
Температура: {result['data'][-1]['temp']}
Давление: {result['data'][-1]['rh']} Па
Часть дня: {'Day' if result['data'][-1]['pod'] == 'd' else 'Night'}
Погода: {result['data'][-1]['weather']['description']}

""")
    else:
        bot.send_message(user.tg_id, f"""
Date: {result['data'][-1]['timestamp_utc'].split('T')[0]}
City: {result['city_name']}
Wind speed (Default m/s): {result['data'][-1]['wind_spd']} ms
Temperature: {result['data'][-1]['temp']}
Humidity: {result['data'][-1]['rh']} (Pa)
Part of the day: {'Day' if result['data'][-1]['pod'] == 'd' else 'Night'}
Weather: {result['data'][-1]['weather']['description']}
        """)


@bot.message_handler(
    func=lambda message: True if message.text == 'Weekly forecast' or 'Прогноз на неделю' == message.text else False)
def week_forecast(message):
    user = User()
    user.get(message.chat.id)
    result = weather.get_weather_week(user)

    for index in range(7):
        if user.lang == 'ru':
            bot.send_message(user.tg_id, f"""
        Дата: {result['data'][index]['valid_date']}
        Город: {result['city_name']}
        Скорость ветра (По умолчанию м/с): {result['data'][index]['wind_spd']} мс
        Максимальная температура: {result['data'][index]['low_temp']}
        Максимальная температура: {result['data'][index]['max_temp']}
        Давление: {result['data'][index]['rh']} (Па)
        Погода: {result['data'][index]['weather']['description']}
                """)
        else:
            bot.send_message(user.tg_id, f"""
        Date: {result['ob_time']}
        City: {result['city_name']}
        Wind speed (Default m/s): {result['wind_spd']} ms
        Temperature: {result['temp']}
        Humidity: {result['rh']} (Pa)
        Part of the day: {'Day' if result['pod'] == 'd' else 'Night'}
        Weather: {result['weather']['description']}
        """)


@bot.message_handler(
    func=lambda message: True if message.text == 'Изменить язык' or 'Change language' == message.text else False)
def change_lang(message):
    user = User()
    user.get(message.chat.id)
    bot.send_message(message.chat.id, lang[user.lang]['choose_lang'], reply_markup=choose_lang())
    bot.register_next_step_handler(message, user.update_lang)


if __name__ == '__main__':
    DB.init_db()
    bot.polling()
