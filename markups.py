import time
import asyncio
import aiohttp
import telebot
from datetime import datetime
from telebot import types
from telebot.async_telebot import AsyncTeleBot


class MarkupCreator:
    @staticmethod
    def create_default_markup():
        """
        Дефолтная панель, что появляется внизу и не исчезает
        """
        markup_with_reminders = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_get_exchange = types.KeyboardButton('Текущий курс доллара 💵')
        btn_setup_reminders = types.KeyboardButton('Настроить уведомления 🔔')
        markup_with_reminders.row(btn_get_exchange)
        markup_with_reminders.row(btn_setup_reminders)
        return markup_with_reminders

    @staticmethod
    def create_start_markup_to_set_reminders(task_2, task_3):
        """
        Панель в сообщении сразу после нажатия кнопки "настроить уведомления"
        """
        start_markup_to_set_reminders = types.InlineKeyboardMarkup()
        btn_set_time = types.InlineKeyboardButton(text='Установить временной интервал ⏱', callback_data='set time')
        btn_set_delta = types.InlineKeyboardButton(text='Установить изменение курса 💲', callback_data='set delta')
        btn_cancel_all_settings = types.InlineKeyboardButton(text='Отменить все уведомления 🔕',
                                                             callback_data='cancel all settings')
        start_markup_to_set_reminders.row(btn_set_time)
        start_markup_to_set_reminders.row(btn_set_delta)
        if task_2 is not None or task_3 is not None:
            start_markup_to_set_reminders.row(btn_cancel_all_settings)
        return start_markup_to_set_reminders

    @staticmethod
    def create_markup_to_set_the_time():
        """
        Панель в сообщении для конфигурирования временных уведомлений
        """
        markup_to_set_the_time = types.InlineKeyboardMarkup()
        btn_20_min = types.InlineKeyboardButton(text='Раз в 20 минут', callback_data='20 min')
        btn_hour = types.InlineKeyboardButton(text='Раз в час', callback_data='60 min')
        btn_day = types.InlineKeyboardButton(text='Раз в день', callback_data='once a day')
        btn_own_config = types.InlineKeyboardButton(text='Ввести свой нитервал ⚙️', callback_data='own config')
        btn_cancel = types.InlineKeyboardButton(text='Отключить данные уведомления 🙅‍♂️',
                                                callback_data='cancel time')
        markup_to_set_the_time.row(btn_20_min)
        markup_to_set_the_time.row(btn_hour)
        markup_to_set_the_time.row(btn_day)
        markup_to_set_the_time.row(btn_own_config)
        markup_to_set_the_time.row(btn_cancel)
        return markup_to_set_the_time

    @staticmethod
    def create_markup_to_set_delta():
        """
        Панель в сообщении для конфигурирования уведомлений об изменении курса
        """
        markup_to_set_delta = types.InlineKeyboardMarkup()
        btn_0001 = types.InlineKeyboardButton(text='При изменении на 0.001 BYN', callback_data='0.001')
        btn_001 = types.InlineKeyboardButton(text='При изменении на 0.01 BYN', callback_data='0.01')
        btn_005 = types.InlineKeyboardButton(text='При изменении на 0.05 BYN', callback_data='0.05')
        btn_01 = types.InlineKeyboardButton(text='При изменении на 0.1 BYN', callback_data='0.1')
        btn_own_delta = types.InlineKeyboardButton(text='Ввести свою величину ⚙️', callback_data='own_delta')
        btn_cancel_delta = types.InlineKeyboardButton(text='Отключить данные уведомления 🙅‍♂️',
                                                      callback_data='cancel delta')
        markup_to_set_delta.row(btn_0001)
        markup_to_set_delta.row(btn_001)
        markup_to_set_delta.row(btn_005)
        markup_to_set_delta.row(btn_01)
        markup_to_set_delta.row(btn_own_delta)
        markup_to_set_delta.row(btn_cancel_delta)
        return markup_to_set_delta


class MarkupSetter(MarkupCreator):
    async def set_start_markup_to_set_reminders(self, bot, task_2, task_3, message, time_interval=None, delta=None):
        message_dir = {
            (task_2 is None and task_3 is None): 'На данный момент у вас не установлены уведомления о курсе доллара. '
                                                 'Давайте это исправим!\n'
                                                 '\n'
                                                 '⏱ Вы можете установить удобную частоту, с которой бот будет присылать вам уведомления '
                                                 '(кнопка "Установить временной интервал").\n'
                                                 '\n'
                                                 '💲 Так же можете настроить величину изменения курса, при которой боту следует прислать вам '
                                                 'уведомление '
                                                 'вне зависимости от того, в какой момент времени это изменение произошло '
                                                 '(кнопка "Установить изменение курса").\n'
                                                 '\n'
                                                 'Допускается использование как одного из типов уведомлений, так и обоих сразу',
            (
                        task_2 is None and task_3 is not None): f'На данный момент у вас установлены уведомления о каждом изменении '
                                                                f'курса на {delta} BYN.\n'
                                                                f'\n'
                                                                f'Можете изменить конфигурацию в соответствии с вашими нуждами',
            (
                        task_2 is not None and task_3 is None): f'На данный момент у вас установлены временные уведомления о курсе '
                                                                f'доллара с интервалом '
                                                                f'в {time_interval}.\n'
                                                                f'\n'
                                                                f'Можете изменить конфигурацию уведомлений в соответствии с '
                                                                f'вашими нуждами',
            (task_2 is not None and task_3 is not None): f'На данный момент у вас установлены временные уведомления '
                                                         f'о курсе доллара с интервалом '
                                                         f'в {time_interval}, а так же уведомления о каждом изменении курса '
                                                         f'на {delta} BYN.\n'
                                                         f'\n'
                                                         f'Можете изменить конфигурацию уведомлений '
                                                         f'в соответствии с вашими нуждами'
        }
        start_markup_to_set_reminders = self.create_start_markup_to_set_reminders(task_2, task_3)
        for condition in message_dir:
            if condition:
                await bot.send_message(message.chat.id, message_dir[condition],
                                       reply_markup=start_markup_to_set_reminders)
                break

    async def set_markup_to_set_the_time(self, bot, message):
        """
        При получении соответствующего сигнала устанавливаем
        панель для конфигурирования временных уведомлений
        """
        await bot.delete_message(message.chat.id, message.id)
        markup_to_set_the_time = self.create_markup_to_set_the_time()
        await bot.send_message(message.chat.id, 'Выберете, с какой переодичностью вы хотели бы получать уведомления',
                               reply_markup=markup_to_set_the_time)

    async def set_delta(self, bot, message):
        """
        При получении соответствующего сигнала устанавливаем
        панель для конфигурирования уведомлении при изменении дельты
        """
        await bot.delete_message(message.chat.id, message.id)
        markup_to_set_delta = self.create_markup_to_set_delta()
        await bot.send_message(message.chat.id, 'Выберете величину изменения курса доллара, при которой бот должен '
                                                'присылать вам уведомление',
                               reply_markup=markup_to_set_delta)



