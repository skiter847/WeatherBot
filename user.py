from sql import DB
from telebot import types
from weather import WeatherBit
from settings import lang, bot, weather


class User(DB):
    """
    User obj
    attr: tg_id, first_name, city, lang, emailing_support
    """

    def __init__(self):
        self.tg_id = None
        self.first_name = None
        self.city = None
        self.lang = None
        self.subscribe = None

    def add_to_db(self):
        """
        add user in db

        """
        self._add_new_user()
        bot.send_message(self.tg_id, lang[self.lang]['city_save'])

    def create_user_menu(self):
        """
        Create inline keyboard
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=1)
        if self.lang == 'ru':
            markup.row('Прогноз на сегодня', 'Прогноз на завтра')
            markup.row('Прогноз на неделю', 'Изменить язык', )
            markup.row('Сменить город', f'Подписка на рассылку{self._check_sub()}')
            bot.send_message(self.tg_id, 'Выберите действие:', reply_markup=markup)
        else:
            markup.row('Forecast today', 'Forecast tomorrow')
            markup.row('Weekly forecast', 'Change language')
            markup.row('Change city', f'Subscribe to sending{self._check_sub()}')
            bot.send_message(self.tg_id, 'Choose action:', reply_markup=markup)

    def exist(self, user_id):
        """

        :param user_id: id user telegram
        :return: return NOne if user not exist in db
        """
        return self._get_user_data(user_id)

    def _check_sub(self):
        if self.subscribe == 0:
            return '✔️'
        else:
            return '✖️'

    def get(self, user_id):
        """
        add data for self attributes
        """
        user_data = self._get_user_data(user_id)
        attrs = self.__dict__
        for index, key in enumerate(attrs):
            attrs[key] = user_data[index]

    def update_city(self, value):
        """
            update in db column city for user
        """
        if WeatherBit.check_city(value, weather):
            self._update_user_data(self.tg_id, 'city', value)
            return True
        else:
            bot.send_message(self.tg_id, lang[self.lang]['city_not_found'])
            return False

    def update_subscribe(self):
        """
            update in db column subscribe for user
        """
        if self.subscribe == 0:
            self._update_user_data(self.tg_id, 'subscribe', 1)
        else:
            self._update_user_data(self.tg_id, 'subscribe', 0)

        bot.send_message(self.tg_id, lang[self.lang]['status_upd'])
        self.create_user_menu()

    def update_lang(self, message):
        """
        update in db column lang for user
        """
        if 'English' in message.text:
            self.lang = 'en'
            self._update_user_data(self.tg_id, 'lang', 'ru')
            bot.send_message(self.tg_id, lang[self.lang]['success'])
        elif 'Русский' in message.text:
            self.lang = 'ru'
            self._update_user_data(self.tg_id, 'lang', 'en')
            bot.send_message(self.tg_id, lang[self.lang]['success'])

        self.create_user_menu()
