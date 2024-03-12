import requests
import json
import os

from src.abstract_classes import AbstractAPI


class HeadHunterAPI(AbstractAPI):
    """ Класс для работы с API"""

    def get_vacancies(self, search_query: str, salary: str, search_area: str):
        """ Получение данных о вакансиях с hh.ru в формате JSON """

        params = self.get_params(search_query, salary, search_area)

        url = "https://api.hh.ru/vacancies"

        response = requests.get(url, params).json()

        data = response.get("items")

        pages = response.get("pages")
        if pages > 1:
            for num in range(1, pages):
                params["page"] = num
                response = requests.get(url, params).json()
                data.extend(response.get("items"))

        return data

    @staticmethod
    def get_params(search_query: str, salary: str, search_area: str):
        current_file_path = os.path.abspath(__file__)
        parent_dir_path = os.path.dirname(os.path.dirname(current_file_path))
        file_path = os.path.join(parent_dir_path, "data", "areas.json")

        with open(file_path, "r", encoding="utf-8") as file:
            areas = json.load(file)

            search_area = search_area.lower()

            if areas.get(search_area):
                area = areas.get(search_area)
            else:
                for k, v in areas.items():
                    if search_area in k.lower():
                        area = v

        params = {
            "text": search_query,
            "per_page": "100",
            "only_with_salary": "true",
            "salary": salary,
            "area": area
        }

        return params
