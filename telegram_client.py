import requests


class TelegramClient:
    def __init__(self, token, base_url):
        self.token = token
        self.base_url = base_url

    def prepare_url(self, method):
        result_url = f'{self.base_url}/bot{self.token}/'
        if method is not None:
            result_url += method
        return result_url

    def post(self, method=None, params=None, body=None):
        url = self.prepare_url(method)
        resp = requests.post(url, params=params, data=body)
        return resp.json()


