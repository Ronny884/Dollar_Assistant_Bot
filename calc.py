from datetime import datetime, timedelta


class Calculator:

    @staticmethod
    def calculate_wait(target_time):
        # Получаем текущую дату и время
        current_time = datetime.now()

        # Разбиваем время пользователя на часы и минуты
        hours, minutes = map(int, target_time.split(':'))

        # Получаем целевую дату и время, устанавливая часы и минуты
        target_datetime = current_time.replace(hour=hours, minute=minutes)

        # Если целевое время уже прошло, увеличиваем дату на 1 день
        if target_datetime < current_time:
            target_datetime += timedelta(days=1)

        # Вычисляем разницу между текущим временем и целевым временем в секундах
        time_difference = (target_datetime - current_time).total_seconds()

        return int(time_difference)
