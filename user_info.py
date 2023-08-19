class User:
    def __init__(self):
        self.info = {}

    def set_default_info(self, user_id):
        """
        Создание в словаре поля для нового пользователя или же возвращение поля для уже существующего
        пользователя к дефолтному виду
        """
        self.info[user_id] = {'task_2_object': None,
                              'task_3_object': None,

                              'time_interval_str': None,
                              'delta_str': None,

                              'setting the time for notifications once a day': False,
                              'setting the time for notifications by own configuration': False,
                              'setting own delta': False
                              }
