import asyncio
from decimal import Decimal


class CoroutineCreator:
    def __init__(self, user, task_setter, markup_creator, exchange_getter):
        self.user = user
        self.task_setter = task_setter
        self.markup_creator = markup_creator
        self.exchange_getter = exchange_getter

    async def form_the_coroutine_for_time_reminders(self, bot, message, seconds):
        """
        Формируем корутинную функцию для отправки уведомлений
        """
        default_markup = self.markup_creator.create_default_markup()
        while True:
            print(f'запущено для {message.chat.id}')
            await asyncio.sleep(seconds / 30)
            await bot.send_message(message.chat.id, f'test {seconds}')
            # await self.exchange_getter.set_exchange(bot, message, default_markup)

    async def form_the_waiting_coroutine_for_everyday_reminders(self, bot, message, await_time):
        """
        Цель данной функции - дождаться указанного пользователем времени ежедневного уведомления, чтобы потом запустить
        таску классическим способом (как снизу)
        """
        default_markup = self.markup_creator.create_default_markup()
        self.user.info[message.chat.id]['time_interval_str'] = '1 день'
        await asyncio.sleep(await_time)
        await self.exchange_getter.set_exchange(bot, message, default_markup)
        await self.task_setter.set_a_task_for_time_reminders(bot, message, 86400)

    async def form_the_coroutine_for_delta_reminders(self, bot, message, delta, restoration=False):
        default_markup = self.markup_creator.create_default_markup()
        previous_exchange = self.exchange_getter.get_exchange(for_delta=True)
        if restoration is False:
            await bot.send_message(message.chat.id,
                                   f'Отлично! Теперь при каждом изменении курса доллара на {delta} BYN '
                                   f'вам будет приходить об этом уведомление.'
                                   f'\n'
                                   f'\nВ настоящий момент по данным Минфина РБ курс составляет:'
                                   f'\nпродажа: <b>{previous_exchange[0]} BYN</b>'
                                   f'\nпокупка: <b>{previous_exchange[1]} BYN</b>', parse_mode='HTML')

        while True:
            await asyncio.sleep(60)
            exchange_at_the_moment = self.exchange_getter.get_exchange(for_delta=True)
            change = Decimal(exchange_at_the_moment[0]) - Decimal(previous_exchange[0])
            print(f'заданная величина: {delta}, текущее изменение: {Decimal(exchange_at_the_moment[0])} - '
                  f'{Decimal(previous_exchange[0])} = {change}')
            if abs(change) >= Decimal(str(delta)):
                await self.exchange_getter.set_exchange(bot, message, default_markup, change=change)
                previous_exchange = exchange_at_the_moment


