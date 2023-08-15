
class Ask:
    def __init__(self, user):
        self.user = user

    async def ask_about_time_for_everyday_reminders(self, bot, message):
        """
        Перед тем, как создавать таску для ежедневных уведомлений, надлежит спросить у пользователя, во сколько именно
        он желает получать эти уведомления
        """
        self.user.info[message.chat.id]['setting the time for notifications once a day'] = True
        await bot.delete_message(message.chat.id, message.id)
        await bot.send_message(message.chat.id, 'Укажите конкретное время, когда боту следует '
                                                'присылать вам уведомление '
                                                '(используйте следующий формат: 9:00, 16:30 и т.д.)')

    async def ask_about_a_convenient_time_interval(self, bot, message):
        """
        Уточняем у пользователя удобный для него временной интервал уведомлений
        """
        self.user.info[message.chat.id]['setting the time for notifications by own configuration'] = True
        await bot.delete_message(message.chat.id, message.id)
        await bot.send_message(message.chat.id, 'Укажите удобный временной интервал (в минутах), с которым '
                                                'вам должны приходить уведомления о курсе доллара')

    async def ask_about_own_delta(self, bot, message):
        self.user.info[message.chat.id]['setting own delta'] = True
        await bot.delete_message(message.chat.id, message.id)
        await bot.send_message(message.chat.id, 'Укажите необходимую величину изменения курса '
                                                'в диапазоне от 0.001 до 1.0 BYN')
