from datetime import date


class Vacancy:
    """ Класс для представления вакансий """
    name: str
    url: str
    salary: dict
    salary_indicated: bool
    snippet: dict
    publication_date: str
    area: str

    number_of_vacancies = 0

    def __init__(self, name: str, url: str,  salary: dict, snippet: dict, publication_date: str, area: str) -> None:
        """
        Метод для инициализации экземпляра класса. Задаем значения атрибутам экземпляра.
        :param name: Название вакансии
        :param url: Ссылка на вакансию
        :param salary: Зарплата
        :param snippet: Требования и обязанности
        :param publication_date: Дата публикации
        :param area: Страна, область или город
        """
        self.name = name
        self.url = url
        self.__salary = salary
        self.salary_indicated = bool(salary)
        self.snippet = snippet
        self.publication_date = publication_date
        self.area = area

        Vacancy.number_of_vacancies += 1

    def __str__(self):
        """
        :return: Строка с информацией о вакансии
        """
        salary_list = []
        if self.salary_indicated:
            if self.__salary.get("from"):
                salary_from = self.__salary.get("from")
                salary_from_str = f"от {salary_from}"
                salary_list.append(salary_from_str)
            if self.__salary.get("to"):
                salary_to = self.__salary.get("to")
                salary_to_str = f"до {salary_to}"
                salary_list.append(salary_to_str)
        else:
            salary_list.append("не указана")

        salary = " ".join(salary_list)

        return f"""Вакансия: {self.name}
{self.area}
Требования: {self.snippet.get("requirement")}
Обязанности: {self.snippet.get("responsibility")}
Зарплата {salary}
Дата публикации {self.publication_date}
Ссылка на вакансию: {self.url}
"""

    def __lt__(self, other) -> bool:
        """ Метод < (меньше) для сравнения двух вакансий  """
        try:
            other_verified = self.__verify_data(other)
        except TypeError as te:
            print(te)
        else:
            try:
                self_salary, other_salary = self.__get_salary_for_comparison(other_verified)
            except ValueError as ve:
                print(ve)
            else:
                return self_salary < other_salary

    def __le__(self, other) -> bool:
        """ Метод <= (меньше либо равно) для сравнения двух вакансий  """
        try:
            other_verified = self.__verify_data(other)
        except TypeError as te:
            print(te)
        else:
            try:
                self_salary, other_salary = self.__get_salary_for_comparison(other_verified)
            except ValueError as ve:
                print(ve)
            else:
                return self_salary <= other_salary

    def __eq__(self, other) -> bool:
        """ Метод == (равно) для сравнения двух вакансий  """
        try:
            other_verified = self.__verify_data(other)
        except TypeError as te:
            print(te)
        else:
            try:
                self_salary, other_salary = self.__get_salary_for_comparison(other_verified)
            except ValueError as ve:
                print(ve)
            else:
                return self_salary == other_salary

    @classmethod
    def cast_to_object_list(cls, vacancy_list: list, currency_rates: dict) -> list:
        """
        Преобразует данные полученные с headhunter из JSON в список объектов
        :param vacancy_list: Список с данными о вакансиях
        :param currency_rates: Словарь с курсами валют
        :return: Список объектов класса Vacancy
        """
        vacancy_objects = []

        for vacancy in vacancy_list:
            name = vacancy.get("name")
            url = vacancy.get("alternate_url")
            the_date = date.fromisoformat(vacancy.get("published_at").split("T")[0])
            publication_date = date.strftime(the_date, "%d.%m.%Y")
            area = vacancy.get("area").get("name")
            snippet = vacancy.get("snippet")
            for item in ["requirement", "responsibility"]:
                try:
                    snippet[item] = snippet.get(item).replace("<highlighttext>", "").replace("</highlighttext>", "")
                except AttributeError:
                    snippet[item] = "не указаны"

            salary = cls.__get_salary_info(vacancy, currency_rates)

            vacancy_object = cls(name, url, salary, snippet, publication_date, area)
            vacancy_objects.append(vacancy_object)

        if not vacancy_objects:
            raise AttributeError("\nПо вашему запросу вакансии не найдены.")

        return vacancy_objects

    @staticmethod
    def filtered_vacancies(vacancy_objects: list, filter_words: list) -> list:
        """
        Фильтрует вакансии по ключевым словам
        :param vacancy_objects: Список с объектами вакансий
        :param filter_words: Список с ключевыми словами
        :return: Отфильтрованный список с объектами вакансий
        """
        if len(filter_words) == 0:
            return vacancy_objects

        filtered_vacancies = []
        for vacancy in vacancy_objects:
            vacancy_words = []
            vacancy_words.extend(vacancy.name.split())
            for item in ["requirement", "responsibility"]:
                try:
                    vacancy_words.extend(vacancy.snippet.get(item).split())
                except AttributeError:
                    continue

            for word in filter_words:
                if word in vacancy_words:
                    filtered_vacancies.append(vacancy)

        if not filtered_vacancies:
            raise AttributeError("\nПо вашему запросу вакансии не найдены.")

        return filtered_vacancies

    @staticmethod
    def sort_vacancies_by_salary(vacancy_objects: list, salary_list: list):
        """
        Сортирует вакансии по зарплате
        :param vacancy_objects: Список с объектами вакансий
        :param salary_list: Строка с желаемой зарплатой
        :return: Отсортированный по зарплате список с объектами вакансий
        """
        sorted_vacancies = []
        vacancies_without_salary = []
        vacancies_salary_to = []
        vacancies_salary_from = []

        for vacancy in vacancy_objects:
            if not vacancy.salary_indicated:
                vacancies_without_salary.append(vacancy)
            elif vacancy.salary.get("to"):
                if len(salary_list) == 2:
                    if vacancy.salary.get("to") <= int(salary_list[1].strip()):
                        vacancies_salary_to.append(vacancy)
                else:
                    vacancies_salary_to.append(vacancy)
            elif vacancy.salary.get("from") and vacancy.salary.get("from") >= int(salary_list[0].strip()):
                vacancies_salary_from.append(vacancy)

        vacancies_to = sorted(vacancies_salary_to, key=lambda x: x.salary.get("to"), reverse=True)
        vacancies_from = sorted(vacancies_salary_from, key=lambda x: x.salary.get("from"), reverse=True)

        sorted_vacancies.extend(vacancies_to)
        sorted_vacancies.extend(vacancies_from)
        sorted_vacancies.extend(vacancies_without_salary)

        if not sorted_vacancies:
            raise AttributeError("\nПо вашему запросу вакансии не найдены.")

        return sorted_vacancies

    @staticmethod
    def get_top_vacancies(vacancy_objects: list, top_n: str):
        """
        Получаем нужное количество вакансий в списке
        :param vacancy_objects: Список с объектами вакансий
        :param top_n: Строка с количеством вакансий
        :return: Список с нужным количеством вакансий
        """
        if top_n != "":
            top_n_int = int(top_n)
            if len(vacancy_objects) >= top_n_int:
                return vacancy_objects[:top_n_int]
            else:
                return vacancy_objects
        else:
            return vacancy_objects

    @property
    def salary(self):
        return self.__salary

    def __get_salary_for_comparison(self, other) -> tuple:
        """
        Получение зарплаты из объектов класса Vacancy для сравнения
        :param other: Объект класса Vacancy
        :return: Кортеж с данными о зарплате типа int объектов класса Vacancy
        """
        if not self.salary_indicated:
            raise ValueError("В вакансии слева не указана зарплата")
        if not other.salary_indicated:
            raise ValueError("В вакансии справа не указана зарплата")

        self_salary_set = set(self.__salary)
        other_salary_set = set(other.salary)
        intersection = list(self_salary_set & other_salary_set)

        if len(intersection) == 1:
            self_salary = self.__salary.get(intersection[0])
            other_salary = other.salary.get(intersection[0])
            return self_salary, other_salary
        elif len(intersection) == 2:
            self_salary = (self.__salary.get("to") + self.__salary.get("from")) // 2
            other_salary = (other.salary.get("to") + other.salary.get("from")) // 2
            return self_salary, other_salary
        elif len(intersection) == 0:
            raise ValueError("Вакансии нельзя сравнить, в одной указано зарплата 'от', а в другой 'до'")

    @classmethod
    def __verify_data(cls, other):
        """
        Проверка на принадлежность к классу Vacancy
        :return: объект класса Vacancy
        """
        if not isinstance(other, cls):
            raise TypeError("Операнд справа должен быть объектом класса Vacancy")
        else:
            return other

    @staticmethod
    def __get_salary_info(vacancy: dict, currency_rates: dict) -> dict:
        """
        Получение информации о зарплате из словаря с информацией о вакансии,
        переводит зарплату в рубли, если она указана в другой валюте
        :param vacancy: Словарь с информацией о вакансии
        :param currency_rates: Словарь с курсами валют
        :return: Словарь с информацией о зарплате
        """
        salary_dict = vacancy.get("salary")

        if salary_dict:
            salary = {}
            currency_rate = currency_rates.get(salary_dict.get("currency"))

            if salary_dict.get("currency") != "RUR" and currency_rate:
                if salary_dict.get("from"):
                    salary_from = salary_dict.get("from") * currency_rate
                    salary["from"] = round(salary_from)
                if salary_dict.get("to"):
                    salary_to = salary_dict.get("to") * currency_rate
                    salary["to"] = round(salary_to)
            elif salary_dict.get("currency") != "RUR" and not currency_rate:
                salary = None
            else:
                if salary_dict.get("from"):
                    salary_from = salary_dict.get("from")
                    salary["from"] = salary_from
                if salary_dict.get("to"):
                    salary_to = salary_dict.get("to")
                    salary["to"] = salary_to
        else:
            salary = None

        return salary
