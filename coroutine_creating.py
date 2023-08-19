import asyncio
from decimal import Decimal


class CoroutineCreator:
    def __init__(self, user, task_setter, markup_creator, exchange_getter):
        self.user = user
        self.task_setter = task_setter
        self.markup_creator = markup_creator
        self.exchange_getter = exchange_getter

    async def form_the_coroutine_for_time_reminders(self, bot, target_id, seconds):
        """
        Формируем корутинную функцию для отправки временных уведомлений
        """
        default_markup = self.markup_creator.create_default_markup()
        while True:
            await asyncio.sleep(seconds)
            await self.exchange_getter.set_exchange(bot, target_id, default_markup)

    async def form_the_waiting_coroutine_for_everyday_reminders(self, bot, target_id, await_time, message):
        """
        Цель данной функции - дождаться указанного пользователем времени ежедневного уведомления, чтобы потом запустить
        таску классическим способом (form_the_coroutine_for_time_reminders)
        """
        default_markup = self.markup_creator.create_default_markup()
        self.user.info[target_id]['time_interval_str'] = '1 день'
        await asyncio.sleep(await_time)
        await self.exchange_getter.set_exchange(bot, target_id, default_markup)
        message.chat.id = target_id
        await self.task_setter.set_a_task_for_time_reminders(bot, message, 86400)

    async def form_the_coroutine_for_delta_reminders(self, bot, target_id, delta, restoration=False):
        """
        Формируем корутинную функцию для отправки уведомлений об изменении курса доллара
        """
        default_markup = self.markup_creator.create_default_markup()
        previous_exchange = await self.exchange_getter.get_exchange(for_delta=True)
        if restoration is False:
            await bot.send_message(target_id,
                                   f'Отлично! Теперь при каждом изменении курса доллара на {delta} BYN '
                                   f'вам будет приходить об этом уведомление.'
                                   f'\n'
                                   f'\nВ настоящий момент по данным Минфина РБ курс составляет:'
                                   f'\nпродажа: <b>{previous_exchange[0]} BYN</b>'
                                   f'\nпокупка: <b>{previous_exchange[1]} BYN</b>', parse_mode='HTML')

        while True:
            await asyncio.sleep(60)
            exchange_at_the_moment = await self.exchange_getter.get_exchange(for_delta=True)
            change = Decimal(exchange_at_the_moment[0]) - Decimal(previous_exchange[0])
            if abs(change) >= Decimal(str(delta)):
                await self.exchange_getter.set_exchange(bot, target_id, default_markup, change=change)
                previous_exchange = exchange_at_the_moment


