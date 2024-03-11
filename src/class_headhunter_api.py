import requests

from src.abstract_classes import AbstractAPI


class HeadHunterAPI(AbstractAPI):
    """ Класс для работы с API"""

    def get_vacancies(self, text: str, salary: str):
        """ Получение данных о вакансиях с hh.ru в формате JSON """

        url = "https://api.hh.ru/vacancies"

        params = {
            "text": text,
            "per_page": "100",
            "only_with_salary": "true",
            "salary": salary
        }

        response = requests.get(url, params).json()

        data = response.get("items")

        pages = response.get("pages")
        if pages > 1:
            for num in range(1, pages):
                params["page"] = num
                response = requests.get(url, params).json()
                data.extend(response.get("items"))

        return data

