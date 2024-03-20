from bs4 import BeautifulSoup
import requests


class ExchangeRates:
    """ Класс для получения курсов валют """

    def get_exchange_rates(self) -> dict:
        """
        Фильтрует данные, отбирает код валюты и курс
        :return: Словарь с курсами валют
        """
        data = self.__get_data()

        exchange_rates = {}

        for item in data:
            currency = item.text.split("\n")[10:]

            for num in range(len(currency) // 7):
                del currency[0]
                currency_code = currency.pop(0)
                quantity = int(currency.pop(0))
                del currency[0]
                exchange_rate = float(currency.pop(0).replace(",", ".")) / quantity
                del currency[0]
                del currency[0]
                exchange_rates[currency_code] = exchange_rate

        return exchange_rates

    @staticmethod
    def __get_data() -> list:
        """ Получает данные с сайта ЦБ РФ """

        url = "https://cbr.ru/currency_base/daily/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        data = soup.find_all("table", class_="data")

        return data
