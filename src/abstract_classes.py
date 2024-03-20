from abc import ABC, abstractmethod


class AbstractAPI(ABC):
    """ Абстрактный класс для работы с API """

    @abstractmethod
    def get_vacancies(self):
        """ Получение данных о вакансиях формате JSON """
        pass


class AbstractSaver(ABC):
    """ Абстрактный класс для работы с файлами """

    @staticmethod
    @abstractmethod
    def add_vacancy(vacancy):
        """ Сохраняет вакансию в JSON файл """
        pass

    @staticmethod
    @abstractmethod
    def delete_vacancy(vacancy):
        """ Удаляет вакансию """
        pass

    @abstractmethod
    def load_file(self):
        """ Получает данные из файла """
        pass

    @abstractmethod
    def write_file(self, data: list):
        """ Записывает данные в файл """
        pass

    @staticmethod
    @abstractmethod
    def get_file_path():
        """ Получает путь к файлу """
        pass


class AbstractVacancy:

    @abstractmethod
    def __str__(self):
        """ :return: Строка с информацией о вакансии """
        pass

    @abstractmethod
    def __lt__(self, other) -> bool:
        """ Метод < (меньше) для сравнения двух вакансий  """
        pass

    @abstractmethod
    def __le__(self, other) -> bool:
        """ Метод <= (меньше либо равно) для сравнения двух вакансий  """
        pass

    @abstractmethod
    def __eq__(self, other) -> bool:
        """ Метод == (равно) для сравнения двух вакансий  """
        pass

    @classmethod
    @abstractmethod
    def cast_to_object_list(cls, vacancy_list: list, currency_rates: dict):
        """ Преобразует данные полученные с headhunter из JSON в список объектов """
        pass

    @staticmethod
    @abstractmethod
    def filtered_vacancies(vacancy_objects: list, filter_words: list):
        """ Фильтрует вакансии по ключевым словам """
        pass

    @staticmethod
    @abstractmethod
    def sort_vacancies_by_salary(vacancy_objects: list, salary_list: list):
        """ Сортирует вакансии по зарплате """
        pass

    @staticmethod
    @abstractmethod
    def get_top_vacancies(vacancy_objects: list, top_n: str):
        """ Получаем нужное количество вакансий в списке """
        pass
