import asyncio
import aiohttp
import telebot
from datetime import datetime
from envparse import Env
from telebot import types
from telebot.async_telebot import AsyncTeleBot

from user_info import User
from markups import MarkupCreator, MarkupSetter
from exchange_getting import ExchangeGetter
from valid import Validator
from calc import Calculator
from coroutine_creating import CoroutineCreator
from task_setting import TaskSetter
from ask_operations import Ask
from cancel_operations import Cancel
from automatic_recovery import Restorer
from massage_handler_operations import MessageHandlerOperator
from telegram_client import TelegramClient
from database_operations import DataBaseClient, UserActioner


user = User()
user_actioner = UserActioner(DataBaseClient('users.db'))
validator = Validator()
calculator = Calculator()
markup_creator = MarkupCreator()
markup_setter = MarkupSetter()
exchange_getter = ExchangeGetter()
cancel = Cancel(user)
ask = Ask(user)
task_setter = TaskSetter(user)
coroutine_creator = CoroutineCreator(user, task_setter, markup_creator, exchange_getter)
msg_handler = MessageHandlerOperator(user, exchange_getter, markup_setter, markup_creator,
                                     validator, calculator, coroutine_creator, task_setter)
task_setter.cor = coroutine_creator


env = Env()
TOKEN = env.str('TOKEN')
ADMIN_CHAT_ID = env.int('ADMIN_CHAT_ID')


class MyBot(AsyncTeleBot):
    def __init__(self, telegram_client: TelegramClient, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.telegram_client = telegram_client
        self.user_actioner = user_actioner

    def setup_resources(self):
        self.user_actioner.setup()

    def create_table(self):
        self.user_actioner.create_table()

    def shutdown(self):
        self.user_actioner.shutdown()

    def update_time_interval(self, user_id, time_interval):
        self.user_actioner.update_time_interval(user_id, time_interval)

    def update_delta(self, user_id, delta):
        self.user_actioner.update_delta(user_id, delta)

    def update_everyday_time(self, user_id, everyday_time):
        self.user_actioner.update_everyday_time(user_id, everyday_time)

    def select_all_users_info(self):
        return self.user_actioner.select_all_users_info()


tg_client = TelegramClient(token=TOKEN, base_url='https://api.telegram.org')
bot = MyBot(token=TOKEN, telegram_client=tg_client)
restorer = Restorer(bot, user, task_setter, calculator, coroutine_creator)


async def func_restore():
    await restorer.restore_state()


async def func_polling():
    await bot.polling()


async def restore_and_polling():
    task_restorer = asyncio.create_task(func_restore())
    task_polling = asyncio.create_task(func_polling())
    await task_restorer
    await task_polling


@bot.message_handler(commands=['start'])
async def start_command(message):
    """
    Всякий пользователь, нажавший /start, будет добавлен в базу
    """
    user_id = message.chat.id
    username = message.from_user.username
    user_exists = bot.user_actioner.get_user(user_id)
    if not user_exists:
        bot.user_actioner.create_user(user_id, username, None, None, None)
        bot.telegram_client.post(method='sendMessage', params={'text': f'Новый пользователь: {username}, id {user_id}',
                                                               'chat_id': ADMIN_CHAT_ID})

    await cancel.cancel_all_settings(bot, message, from_start=True)

    user.set_default_info(user_id)
    default_markup = markup_creator.create_default_markup()
    text = 'Dollar Assistant BY - бот для получения актуального курса доллара.' \
                    '\n' \
                    '\n<b>Команды</b>' \
                    '\n/start - перезапуск и сброс настроек' \
                    '\n/help - подробное описание бота' \
                    '\n/info - информация о ваших текущих настройках'
    await bot.send_message(user_id, text, reply_markup=default_markup, parse_mode='HTML')


@bot.message_handler(commands=['help'])
async def help_command(message):
    text = 'Dollar Assistant BY - это бот в Telegram, позоляющий получать актуальную информацию о курсе ' \
           'доллара по отношению к белорусскому рублю.\n ' \
           '\nЕсли вам нужно сиюминутно узнать курс - нажмите кнопку ' \
           '"Текущий курс доллара". Если требуется получать уведомления, то, нажав кнопку "Настроить уведомления", вы ' \
           'можете настроить их отправку в соответствии с удобной для вас конфигурацией.' \
           '\n' \
           '\n<b>Виды уведомлений</b>' \
           '\n' \
           '\n⏱ Временные уведомления. Приходят вам регулярно с определённой, настроенной вами частотой ' \
           '(20 минут, час, день и т.д.).' \
           '\n' \
           '\n💲 Уведомления об изменении курса. Бот постоянно мониторит курс доллара и в случае изменения её на ' \
           'какую-либо фиксированную величину присылает вам об этом уведомление. Значение этой величины вы ' \
           'настраиваете сами так же, как и частоту для предыдущего вида уведомлений.' \
           '\n' \
           '\n<b>Важные моменты</b>' \
           '\n' \
           '\n📩 Вы можете использовать как один из видов уведомлений, так и оба сразу.' \
           '\n' \
           '\n🏦 Информация о курсе берётся из раздела "Лучшие курсы" на официальном сайте myfin.by. ' \
           'Если по каким-либо причинам этот сайт не доступен, бот делает запрос для получения курса на официальный ' \
           'сайт Беларусбанка.' \
           '\n' \
           '\n💰 При подсчёте величины изменения курса вычисления ведутся относительно стоимости доллара при покупке.' \
           '\n' \
           '\n🌍 Бот работает в часовом поясе GMT+3 (Москва). Это важно иметь в виду при установке ежедневных ' \
           'уведомлений. Если вы находитесь в другом часовом поясе, то во избежание некорректной ' \
           'работы бота вам следует отдать предпочтение другим вариациям временных уведомлений' \
           '\n' \
           '\n<b>Команды</b>' \
           '\n/start - перезапуск и сброс настроек' \
           '\n/help - подробное описание бота' \
           '\n/info - информация о ваших текущих настройках.'

    await bot.send_message(message.chat.id, text, parse_mode='HTML')


@bot.message_handler(commands=['info'])
async def help_command(message):
    await markup_setter.set_start_markup_to_set_reminders(bot=bot,
                                                          task_2=user.info[message.chat.id]['task_2_object'],
                                                          task_3=user.info[message.chat.id]['task_3_object'],
                                                          message=message,
                                                          time_interval=user.info[message.chat.id]['time_interval_str'],
                                                          delta=user.info[message.chat.id]['delta_str'],
                                                          for_info=True)


@bot.message_handler()
async def correct_input(message):

    if message.text.lower() in ('текущий курс доллара 💵', 'курс доллара', 'курс', 'доллар', '$', '💵'):
        await msg_handler.processing_a_request_to_get_the_dollar_exchange(bot, message)

    elif message.text == 'Настроить уведомления 🔔':
        await msg_handler.process_a_request_to_configure_notifications(bot, message)

    elif user.info[message.chat.id]['setting the time for notifications once a day']:
        await msg_handler.process_data_when_setting_one_day_notifications(bot, message)

    elif user.info[message.chat.id]['setting the time for notifications by own configuration']:
        await msg_handler.process_data_when_setting_notifications_with_own_interval(bot, message)

    elif user.info[message.chat.id]['setting own delta']:
        await msg_handler.process_data_when_setting_own_delta(bot, message)

    else:
        await msg_handler.process_any_other_message(bot, message)


@bot.callback_query_handler(func=lambda callback: callback)
async def callback_manager(callback):
    callback_dir = {
        '20 min': lambda: task_setter.set_a_task_for_time_reminders(bot, callback.message, 1200, 'каждые 20 минут.'),
        '60 min': lambda: task_setter.set_a_task_for_time_reminders(bot, callback.message, 3600, 'каждый час.'),
        'once a day': lambda: ask.ask_about_time_for_everyday_reminders(bot, callback.message),
        'own config': lambda: ask.ask_about_a_convenient_time_interval(bot, callback.message),
        'cancel time': lambda: cancel.cancel_time_reminders(bot, callback.message),

        '0.001': lambda: task_setter.set_a_task_for_delta_reminders(bot, callback.message, 0.001),
        '0.01': lambda: task_setter.set_a_task_for_delta_reminders(bot, callback.message, 0.01),
        '0.05': lambda: task_setter.set_a_task_for_delta_reminders(bot, callback.message, 0.05),
        '0.1': lambda: task_setter.set_a_task_for_delta_reminders(bot, callback.message, 0.1),
        'own_delta': lambda: ask.ask_about_own_delta(bot, callback.message),
        'cancel delta': lambda: cancel.cancel_delta_reminders(bot, callback.message),

        'set time': lambda: markup_setter.set_markup_to_set_the_time(bot, callback.message),
        'set delta': lambda: markup_setter.set_delta(bot, callback.message),
        'cancel all settings': lambda: cancel.cancel_all_settings(bot, callback.message)
    }
    await callback_dir[callback.data]()


if __name__ == '__main__':
    while True:
        try:
            bot.setup_resources()
            bot.create_table()
            asyncio.run(restore_and_polling())

        except Exception as err:
            bot.telegram_client.post(method='sendMessage', params={'text': f'{datetime.now()}\nОШИБКА: '
                                                                           f'\n{err}',
                                                                   'chat_id': ADMIN_CHAT_ID})
            bot.shutdown()
