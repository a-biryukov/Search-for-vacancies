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

    @classmethod
    def cast_to_object_list(cls, data: list) -> list:
        """
        Преобразует набор данных из JSON в список объектов
        :param data: Список с данными о вакансиях
        :return: Список объектов класса Vacancy
        """
        vacancy_objects = []

        for vacancy in data:
            name = vacancy.get("name")
            url = vacancy.get("alternate_url")
            date = vacancy.get("published_at")
            area = vacancy.get("area").get("name")
            req = vacancy.get("snippet").get("requirement")
            try:
                requirement = req.replace("<highlighttext>", "").replace("</highlighttext>", "")
            except AttributeError:
                requirement = "Требования не указаны"
            try:
                del vacancy.get("salary")["gross"]
            except TypeError:
                continue
            salary = vacancy.get("salary")

            vacancy_object = cls(name, url, salary, requirement, date, area)
            vacancy_objects.append(vacancy_object)

        return vacancy_objects

