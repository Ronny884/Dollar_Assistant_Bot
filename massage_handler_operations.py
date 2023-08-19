import asyncio


class MessageHandlerOperator:
    def __init__(self, user, exchange_getter, markup_setter, markup_creator,
                 validator, calculator, coroutine_creator, task_setter):
        self.user = user
        self.exchange_getter = exchange_getter
        self.markup_setter = markup_setter
        self.markup_creator = markup_creator
        self.validator = validator
        self.calculator = calculator
        self.coroutine_creator = coroutine_creator
        self.task_setter = task_setter

    async def processing_a_request_to_get_the_dollar_exchange(self, bot, message):
        """
        При нажатии на кнопку 'Текущий курс доллара'
        """
        default_markup = self.markup_creator.create_default_markup()
        self.user.info[message.chat.id]['setting the time for notifications once a day'] = False
        self.user.info[message.chat.id]['setting the time for notifications by own configuration'] = False
        self.user.info[message.chat.id]['setting own delta'] = False
        await self.exchange_getter.set_exchange(bot, message.chat.id, default_markup)

    async def process_a_request_to_configure_notifications(self, bot, message):
        """
        При нажатии на кнопку 'Настроить уведомления'
        """
        self.user.info[message.chat.id]['setting the time for notifications once a day'] = False
        self.user.info[message.chat.id]['setting the time for notifications by own configuration'] = False
        self.user.info[message.chat.id]['setting own delta'] = False
        await self.markup_setter.set_start_markup_to_set_reminders(bot=bot,
                                                              task_2=self.user.info[message.chat.id]['task_2_object'],
                                                              task_3=self.user.info[message.chat.id]['task_3_object'],
                                                              message=message,
                                                              time_interval=self.user.info[message.chat.id][
                                                                  'time_interval_str'],
                                                              delta=self.user.info[message.chat.id]['delta_str'])

    async def process_data_when_setting_one_day_notifications(self, bot, message):
        """
        Обработка введённых пользователем данных при установке времени ежедневных уведомлений
        """
        default_markup = self.markup_creator.create_default_markup()
        if await self.validator.validate_input_time_by_format(message.text):
            await_time = self.calculator.calculate_wait(message.text)

            if self.user.info[message.chat.id]['task_2_object'] is not None:
                self.user.info[message.chat.id]['task_2_object'].cancel()

            self.user.info[message.chat.id]['task_2_object'] = \
                asyncio.create_task(self.coroutine_creator.form_the_waiting_coroutine_for_everyday_reminders(bot=bot,
                                                                                                             target_id=message.chat.id,
                                                                                                             await_time=await_time,
                                                                                                             message=message
                                                                                                             ))

            await bot.send_message(message.chat.id,
                                   f'Отлично! Уведомления о курсе доллара будут приходить вам ежедневно в '
                                   f'{message.text} по МСК.',
                                   reply_markup=default_markup)
            self.user.info[message.chat.id]['setting the time for notifications once a day'] = False
            bot.update_everyday_time(message.chat.id, message.text)
            bot.update_time_interval(message.chat.id, '86400')
        else:
            await bot.send_message(message.chat.id, 'Время введено некорректно. '
                                                    'Повторите ввод в соответствии с форматом')

    async def process_data_when_setting_notifications_with_own_interval(self, bot, message):
        """
        Обработка введённых пользователем данных при установке временных уведомлений с собственным интервалом
        """
        if await self.validator.validate_the_number_of_minutes(message.text):
            time_interval = int(message.text) * 60
            self.user.info[message.chat.id]['setting the time for notifications by own configuration'] = False
            await self.task_setter.set_a_task_for_time_reminders(bot, message, time_interval, f'раз в '
                                                                                       f'{int(message.text)} мин.')
        else:
            await bot.send_message(message.chat.id, 'Интервал введен некорректно. Введите целое положительное число')

    async def process_data_when_setting_own_delta(self, bot, message):
        """
        Обработка введённых пользователем данных при установке уведомлений об изменении курса с собственной
        величиной изменения
        """
        if await self.validator.validate_own_delta(message.text):
            self.user.info[message.chat.id]['setting own delta'] = False

            delta = float(message.text)
            await self.task_setter.set_a_task_for_delta_reminders(bot, message, delta, delete=False)
        else:
            await bot.send_message(message.chat.id, 'Величина введена некорректно. Повторите попытку, учитывая, что '
                                                    'введённая величина должна быть положительным числом с плавающей '
                                                    'точкой и входить в диапазон от 0.001 до 1.0 '
                                                    '(например: 0.22, 0.885)')

    async def process_any_other_message(self, bot, message):
        """
        Обработка введённых пользователем данных, что не удовлетворяют ни одному из вышеперечисленных условий
        """
        self.user.info[message.chat.id]['setting the time for notifications once a day'] = False
        await bot.send_message(message.chat.id, ':)', reply_markup=self.markup_creator.create_default_markup())


