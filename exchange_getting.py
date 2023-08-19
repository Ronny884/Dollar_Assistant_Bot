import asyncio
import aiohttp
import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup


class ExchangeGetter:

    @staticmethod
    async def aiohttp_parsing():
        """
        Асинхронный парсинг сайта Минфина РБ
        """
        URL = 'https://myfin.by/currency/usd'
        async with aiohttp.ClientSession() as session:
            async with session.get(URL) as resp:
                response = await resp.read()
                soup = BeautifulSoup(response, 'html.parser')
                convert = soup.findAll('span', {'class': 'accent'})
                return convert[0].text, convert[1].text

    @staticmethod
    def parsing():
        """
        Синхронный парсинг сайта Минфина РБ (в случае ошибок при асинхронном парсинге)
        """
        URL = 'https://myfin.by/currency/usd'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                 ' Chrome/115.0.0.0 Safari/537.36'}
        full_page = requests.get(URL, headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        convert = soup.findAll('span', {'class': 'accent'})
        return convert[0].text, convert[1].text

    @staticmethod
    def get_json():
        """
        Синхронный гет-запрос на сайт Беларусбанка
        """
        URL = 'https://belarusbank.by/api/kursExchange'
        answer = requests.get(URL)
        exchange = json.loads(answer.text)[0]['USD_in'], json.loads(answer.text)[0]['USD_out']
        return exchange

    async def get_exchange(self, for_delta=False):
        if for_delta:
            try:
                result = await self.aiohttp_parsing()
                return result
            except:
                result = self.parsing()
                return result
        else:
            try:
                result = await self.aiohttp_parsing(), 'по данным Минфина РБ'
            except:
                try:
                    result = self.parsing(), 'по данным Минфина РБ'
                except:
                    result = self.get_json(), 'по данным Беларусбанка'

            return result

    async def set_exchange(self, bot, target_id, default_markup, change=None):
        """
        Вызов необходимых методов и вывод результата пользователю
        """
        if change is None:
            result = await self.get_exchange()
            text = (f'💸 В настоящий момент времени {result[1]} курс доллара составляет:'
                                                f'\nпродажа: <b>{result[0][0]} BYN</b>'
                                                f'\nпокупка: <b>{result[0][1]} BYN</b>')
        else:
            result = await self.get_exchange(for_delta=True)
            if change > 0:
                event_characteristic = 'повышение'
            else:
                event_characteristic = 'понижение'

            text = (f'🤑 Произошло {event_characteristic} курса доллара (покупка) на {abs(change)} BYN. ' 
                   f'На данный момент он составляет:' 
                   f'\nпродажа: <b>{result[0]} BYN</b>' 
                   f'\nпокупка: <b>{result[1]} BYN</b>')

        await bot.send_message(target_id, text, reply_markup=default_markup, parse_mode='HTML')



