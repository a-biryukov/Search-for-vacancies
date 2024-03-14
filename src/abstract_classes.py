from abc import ABC, abstractmethod


class AbstractAPI(ABC):
    """ Абстрактный класс для работы с API """

    @abstractmethod
    def get_vacancies(self):
        pass


class AbstractSaver(ABC):
    """ Абстрактный класс для работы с файлами """

    @staticmethod
    @abstractmethod
    def add_vacancy(vacancy):
        pass

    @staticmethod
    @abstractmethod
    def delete_vacancy(vacancy):
        pass
