class Vacancy:
    """ Класс для представления вакансий """
    name: str
    url: str
    salary: dict
    requirement: str
    date: str
    area: str

    number_of_vacancies = 0

    def __init__(self, name: str, url: str,  salary: dict, requirement: str, date: str, area: str):
        """
        Метод для инициализации экземпляра класса. Задаем значения атрибутам экземпляра.
        :param name: Название вакансии
        :param url: Ссылка на вакансию
        :param salary: Зарплата
        :param requirement: Требования
        :param date: Дата публикации
        :param area: Страна, область или город
        """
        self.name = name
        self.url = url
        self.salary = salary
        self.requirement = requirement
        self.date = date
        self.area = area

        Vacancy.number_of_vacancies += 1

    def __lt__(self, other):
        """ Метод < (меньше) для сравнения двух вакансий  """
        other_verified = self.__verify_data(other)
        self_salary, other_salary = self.__get_salary_for_comparison(other_verified)
        return self_salary < other_salary

    def __le__(self, other):
        """ Метод <= (меньше либо равно) для сравнения двух вакансий  """
        other_verified = self.__verify_data(other)
        self_salary, other_salary = self.__get_salary_for_comparison(other_verified)
        return self_salary <= other_salary

    def __eq__(self, other):
        """ Метод == (равно) для сравнения двух вакансий  """
        other_verified = self.__verify_data(other)
        self_salary, other_salary = self.__get_salary_for_comparison(other_verified)
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
            date = vacancy.get("published_at")
            area = vacancy.get("area").get("name")
            req = vacancy.get("snippet").get("requirement")

            try:
                requirement = req.replace("<highlighttext>", "").replace("</highlighttext>", "")
            except AttributeError:
                requirement = "Требования не указаны"

            if vacancy.get("salary"):
                # Получаем зарплату и переводим её в рубли, если она указана в другой валюте
                if vacancy.get("salary").get("currency") != "RUR":
                    currency_rate = currency_rates.get(vacancy.get("salary").get("currency"))

                    salary = {}
                    if vacancy.get("salary").get("from"):
                        salary_from = vacancy.get("salary").get("from") * currency_rate
                        salary["from"] = round(salary_from)
                    if vacancy.get("salary").get("to"):
                        salary_to = vacancy.get("salary").get("to") * currency_rate
                        salary["to"] = round(salary_to)
                else:
                    salary = {}
                    if vacancy.get("salary").get("from"):
                        salary_from = vacancy.get("salary").get("from")
                        salary["from"] = salary_from
                    if vacancy.get("salary").get("to"):
                        salary_to = vacancy.get("salary").get("to")
                        salary["to"] = salary_to

                vacancy_object = cls(name, url, salary, requirement, date, area)
                vacancy_objects.append(vacancy_object)

            else:
                salary = {"to": 0}

                vacancy_object = cls(name, url, salary, requirement, date, area)
                vacancy_objects.append(vacancy_object)

        return vacancy_objects

    def __get_salary_for_comparison(self, other) -> tuple:
        self_salary_set = set(self.salary)
        other_salary_set = set(other.salary)
        intersection = list(self_salary_set & other_salary_set)
        if len(intersection) == 1:
            self_salary = self.salary.get(intersection[0])
            other_salary = other.salary.get(intersection[0])
        else:
            self_salary = (self.salary.get("to") + self.salary.get("from")) // 2
            other_salary = (other.salary.get("to") + other.salary.get("from")) // 2

        return self_salary, other_salary

    @classmethod
    def __verify_data(cls, other):
        if not isinstance(other, cls):
            raise TypeError("Операнд справа должен иметь тип int или быть объектом класса Vacancy")

        return other
