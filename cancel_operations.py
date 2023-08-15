
class Cancel:
    def __init__(self, user):
        self.user = user

    async def cancel_time_reminders(self, bot, message):
        await bot.delete_message(message.chat.id, message.id)
        if self.user.info[message.chat.id]['task_2_object'] is not None:
            self.user.info[message.chat.id]['task_2_object'].cancel()
            self.user.info[message.chat.id]['task_2_object'] = None
            await bot.send_message(message.chat.id, 'Временные уведомления отключены.')
            bot.update_time_interval(message.chat.id, None)
            bot.update_everyday_time(message.chat.id, None)
        else:
            await bot.send_message(message.chat.id, 'У вас не было временных уведомлений')

    async def cancel_delta_reminders(self, bot, message):
        await bot.delete_message(message.chat.id, message.id)
        if self.user.info[message.chat.id]['task_3_object'] is not None:
            self.user.info[message.chat.id]['task_3_object'].cancel()
            self.user.info[message.chat.id]['task_3_object'] = None
            await bot.send_message(message.chat.id, 'Уведомления об изменении курса доллара отключены.')
            bot.update_delta(message.chat.id, None)
        else:
            await bot.send_message(message.chat.id, 'У вас не было уведомлений об изменении курса доллара')

    async def cancel_all_settings(self, bot, message, from_start=False):

        await bot.delete_message(message.chat.id, message.id)
        for task_object in ('task_2_object', 'task_3_object'):
            if self.user.info[message.chat.id][task_object] is not None:
                self.user.info[message.chat.id][task_object].cancel()
                self.user.info[message.chat.id][task_object] = None
        if from_start is False:
            await bot.send_message(message.chat.id, 'Все настроенные ранее уведомления отключены.')
        bot.update_time_interval(message.chat.id, None)
        bot.update_delta(message.chat.id, None)
        bot.update_everyday_time(message.chat.id, None)



