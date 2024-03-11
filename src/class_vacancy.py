import json


class Vacancy:
    """Класс для представления вакансий"""

    def __init__(self, name: str, url: str,  salary: dict, requirement: str, data: str):
        self.name = name
        self.url = url
        self.salary = salary
        self.requirement = requirement
        self.data = data

    @classmethod
    def cast_to_object_list(cls):
        """Преобразование набора данных из JSON в список объектов"""

        with open("vacancies.json", encoding="utf-8") as f:
            data = json.load(f)

        vacancy_objects = []

        for vacancy in data:
            name = vacancy.get("name")
            url = vacancy.get("alternate_url")
            salary = vacancy.get("salary")
            requirement = vacancy.get("snippet").get("requirement")
            data = vacancy.get("published_at")

            vacancy_object = cls(name, url, salary, requirement, data)
            vacancy_objects.append(vacancy_object)

        return vacancy_objects
