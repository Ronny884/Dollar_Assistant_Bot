from datetime import datetime, timedelta


class Calculator:

    @staticmethod
    def calculate_wait(target_time):
        """
        Высчитываем время, которое необходимо выждать, прежде чем запускать таску для ежедневных уведомлений
        в том виде, как она представлена в TaskSetter
        """
        current_time = datetime.now()
        hours, minutes = map(int, target_time.split(':'))
        target_datetime = current_time.replace(hour=hours, minute=minutes)
        if target_datetime < current_time:
            target_datetime += timedelta(days=1)
        time_difference = (target_datetime - current_time).total_seconds()
        return int(time_difference)
