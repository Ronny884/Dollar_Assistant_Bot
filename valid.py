import re
import asyncio
from decimal import Decimal
from datetime import datetime, timedelta


class Validator:
    @staticmethod
    async def validate_input_time_by_format(input_time):
        """
        Валидация введённого пользователем времени для ежедневных уведомлений
        """
        time_pattern = r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'
        if re.match(time_pattern, input_time):
            return True
        else:
            return False

    @staticmethod
    async def validate_the_number_of_minutes(input_time):
        """
        Валидация введённого пользователем количества минут
        """
        try:
            minutes = int(input_time)
            if minutes < 0:
                return False
            return True
        except ValueError:
            return False

    @staticmethod
    async def validate_own_delta(own_delta):
        """
        Валидация введённой пользователем величины изменения курса
        """
        try:
            value = Decimal(own_delta)
            if 0.001 <= value <= 1.0:
                return True
            else:
                return False
        except ValueError:
            return False
