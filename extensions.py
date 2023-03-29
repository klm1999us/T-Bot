import requests
import json
from config import currency, url, headers, payload


class APIException(Exception):      # Класс исключений при ошибке пользователя.
    pass


# Класс обработки данных (и ошибок) от пользователя, и отправки запроса к стороннему API.
# Метод get_price() делает парсинг и возвращает результат конвертации двух валют.
class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base not in currency.keys() and base not in currency.values():
            raise APIException(f'С валютой "{base}" мы не работаем!\n Для справки наберите /help')
        if quote not in currency.keys() and quote not in currency.values():
            raise APIException(f'С валютой "{quote}" мы не работаем!\n Для справки наберите /help')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать число "{amount}".')

        if base == quote:
            raise APIException('Для конвертации нужны две разные валюты!\n Для справки наберите /help')

        r = requests.get(f"{url}to={currency[quote]}&from={currency[base]}&amount={amount}", headers=headers, data=payload)
        final_price = json.loads(r.content)['result']

        return final_price
