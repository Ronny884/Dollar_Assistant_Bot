import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup


class ExchangeGetter:

    @staticmethod
    def parsing():
        URL = 'https://myfin.by/currency/usd'
        # URL = 'fg'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                 ' Chrome/115.0.0.0 Safari/537.36'}

        full_page = requests.get(URL, headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        convert = soup.findAll('span', {'class': 'accent'})
        return convert[0].text, convert[1].text

    @staticmethod
    def get_json():
        URL = 'https://belarusbank.by/api/kursExchange'
        answer = requests.get(URL)
        exchange = json.loads(answer.text)[0]['USD_in'], json.loads(answer.text)[0]['USD_out']
        return exchange

    def get_exchange(self, for_delta=False):
        if for_delta:
            result = self.parsing()
            return result
        else:
            try:
                result = self.parsing(), 'по данным Минфина РБ'
            except:
                result = self.get_json(), 'по данным Беларусбанка'
            return result

    async def set_exchange(self, bot, message, default_markup, change=None):
        if change is None:
            result = self.get_exchange()
            text = (f'💸 В настоящий момент времени {result[1]} курс доллара составляет:'
                                                f'\nпродажа: <b>{result[0][0]} BYN</b>'
                                                f'\nпокупка: <b>{result[0][1]} BYN</b>')
        else:
            result = self.get_exchange(for_delta=True)
            if change > 0:
                event_characteristic = 'повышение'
            else:
                event_characteristic = 'понижение'

            text = (f'🤑 Произошло {event_characteristic} курса доллара (покупка) на {abs(change)} BYN. ' 
                   f'На данный момент он составляет:' 
                   f'\nпродажа: <b>{result[0]} BYN</b>' 
                   f'\nпокупка: <b>{result[1]} BYN</b>')

        await bot.send_message(message.chat.id, text, reply_markup=default_markup, parse_mode='HTML')


