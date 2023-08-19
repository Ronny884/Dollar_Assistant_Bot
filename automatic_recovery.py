from decimal import Decimal
import asyncio


class Restorer:
    def __init__(self, bot, user, task_setter, calculator, coroutine_creator):
        self.bot = bot
        self.user = user
        self.task_setter = task_setter
        self.calculator = calculator
        self.coroutine_creator = coroutine_creator

    class FictionChat:
        def __init__(self, id):
            self.id = id

    class FictionMessage:
        """
        Класс для создания объекта-пустышки с нужной структурой, что будет содержать в себе лишь
        id пользователя или же не содержать ничего. Этот объект необходим для последующей передачи
        его методам других классов с целью корректной работы программы
        """
        def __init__(self, chat):
            self.chat = chat

    fiction_message = FictionMessage(FictionChat(None))
    empty_fiction_message = FictionMessage(FictionChat(None))

    def get_info_from_db(self):
        return self.bot.select_all_users_info()

    async def restore_state(self):
        """
        Автоматическое восстановление работы бота: взятие настроек из БД и запуск соответствующих тасок
        для каждого пользователя
        """
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
                    await_time = self.calculator.calculate_wait(everyday_time)
                    self.user.info[int(user_id)]['task_2_object'] = \
                        asyncio.create_task(
                            self.coroutine_creator.form_the_waiting_coroutine_for_everyday_reminders(bot=self.bot,
                                                                                                     target_id=int(user_id),
                                                                                                     await_time=await_time,
                                                                                                     message=self.empty_fiction_message))

                if delta is not None:
                    await self.task_setter.set_a_task_for_delta_reminders(bot=self.bot,
                                                                          message=self.fiction_message,
                                                                          delta=Decimal(delta),
                                                                          delete=False,
                                                                          restoration=True)




