import requests
import json
import os

from src.abstract_classes import AbstractAPI


class HeadHunterAPI(AbstractAPI):
    """ Класс для работы с API """

    search_query: str
    salary_list: list
    search_area: str
    only_with_salary: str

    def __init__(self, search_query: str, salary_list: list, search_area: str, only_with_salary: str) -> None:
        """
        Метод для инициализации экземпляра класса. Задаем значения атрибутам экземпляра.
        :param search_query: Поисковой запрос (название вакансии)
        :param salary: Желаемая зарплата
        :param search_area: Область поиска (Страна, область или город)
        :param only_with_salary: Запрос вакансий только с зарплатой (true or false)
        """
        self.search_query = search_query
        self.salary = salary_list
        self.search_area = search_area.title()
        if only_with_salary.lower() == "да":
            self.only_with_salary = "false"
        else:
            self.only_with_salary = "true"

    def get_vacancies(self) -> list:
        """
        Получение данных о вакансиях с hh.ru в формате JSON
        :return: Список с информацией о вакансиях
        """

        params = self.__get_params()

        url = "https://api.hh.ru/vacancies"
        response = requests.get(url, params)
        data = response.json()

        vacancy_list = data.get("items")
        if not vacancy_list:
            raise AttributeError("\nПо вашему запросу вакансии не найдены.")

        pages = data.get("pages")
        if pages is not None:
            for num in range(1, pages):
                params["page"] = num
                response = requests.get(url, params).json()
                vacancy_list.extend(response.get("items"))

        return vacancy_list

    def __get_params(self) -> dict:
        """
        Подготовка параметров для запроса вакансий с hh.ru
        :return: Параметры для запроса
        """
        params = {
            "text": self.search_query,
            "per_page": "100",
            "only_with_salary": self.only_with_salary
        }

        current_file_path = os.path.abspath(__file__)
        parent_dir_path = os.path.dirname(os.path.dirname(current_file_path))
        file_path = os.path.join(parent_dir_path, "data", "areas.json")

        with open(file_path, "r", encoding="utf-8") as file:
            areas = json.load(file)

            if areas.get(self.search_area):
                area = areas.get(self.search_area)
            elif not areas.get(self.search_area):
                for k, v in areas.items():
                    if self.search_area in k:
                        area = v
                    else:
                        area = None

        if area:
            params["area"] = area
        else:
            print(f"Область поиска {self.search_area} не найдена. Поиск будет производиться по всем регионам.")

        if self.salary:
            params["salary"] = self.salary[0].strip()

        return params
