import asyncio


class TaskSetter:
    def __init__(self, user):
        self.user = user
        self.cor = None

    async def set_a_task_for_time_reminders(self, bot, message, seconds, end_words=None, restoration=False):
        """
        Оборачиваем корутину в таску и создаём второй процесс. Если он существовал до этого - пересоздаём
        """
        if seconds in (1200, 3600, 86400):
            seconds_dir = {
                1200: '20 минут',
                3600: '1 час',
                86400: '1 день'
            }
            self.user.info[message.chat.id]['time_interval_str'] = seconds_dir[seconds]
        else:
            self.user.info[message.chat.id]['time_interval_str'] = f'{int(seconds / 60)} мин'

        if end_words is not None:
            await bot.send_message(message.chat.id, f'Отлично! Уведомления о курсе доллара '
                                                    f'будут приходить вам {end_words}')

        if seconds in (1200, 3600) and restoration is False:
            await bot.delete_message(message.chat.id, message.id)

        if self.user.info[message.chat.id]['task_2_object'] is not None:
            self.user.info[message.chat.id]['task_2_object'].cancel()
            print(self.user.info[message.chat.id]['task_2_object'].get_name(), 'отменена')

        bot.update_time_interval(message.chat.id, str(seconds))
        if seconds != 86400:
            bot.update_everyday_time(message.chat.id, None)

        # self.user.info[message.chat.id]['task_2_object'] = self.user.info[message.chat.id]['task_2'](msg=message,
        #                                                                                              sec=seconds)

        self.user.info[message.chat.id]['task_2_object'] = asyncio.create_task(self.cor.form_the_coroutine_for_time_reminders(bot,
                                                                               message,
                                                                               seconds))

        print(self.user.info[message.chat.id]['task_2_object'].get_name(), 'создана')

    async def set_a_task_for_delta_reminders(self, bot, message, delta, delete=True, restoration=False):
        self.user.info[message.chat.id]['delta_str'] = str(delta)
        bot.update_delta(message.chat.id, str(delta))
        if self.user.info[message.chat.id]['task_3_object'] is not None:
            self.user.info[message.chat.id]['task_3_object'].cancel()
            print(self.user.info[message.chat.id]['task_3_object'].get_name(), 'отменена')

        self.user.info[message.chat.id]['task_3_object'] = self.user.info[message.chat.id]['task_3'](msg=message,
                                                                                                     delta=delta,
                                                                                                     rest=restoration)
        print(self.user.info[message.chat.id]['task_3_object'].get_name(), 'создана')
        if delete:
            await bot.delete_message(message.chat.id, message.id)




