from decimal import Decimal
import asyncio


class Restorer:
    def __init__(self, bot, user, task_setter):
        self.bot = bot
        self.user = user
        self.task_setter = task_setter

    class FictionChat:
        def __init__(self, id):
            self.id = id

    class FictionMessage:
        def __init__(self, chat):
            self.chat = chat

    fiction_message = FictionMessage(FictionChat(None))

    def get_info_from_db(self):
        return self.bot.select_all_users_info()

    async def restore_state(self):
        info = self.get_info_from_db()
        if info:
            for user_tuple in info:
                user_id, time_interval, delta, everyday_time = user_tuple[0], user_tuple[2], \
                    user_tuple[3], user_tuple[4]
                self.user.set_default_info(int(user_id))
                self.fiction_message.chat.id = int(user_id)

                if time_interval is not None and everyday_time is None:
                    await self.task_setter.set_a_task_for_time_reminders(self.bot, self.fiction_message,
                                                                         int(time_interval),
                                                                         restoration=True)

                if everyday_time is not None:
                    pass

                if delta is not None:
                    await self.task_setter.set_a_task_for_delta_reminders(self.bot, self.fiction_message,
                                                                          Decimal(delta),
                                                                          delete=False,
                                                                          restoration=True)



