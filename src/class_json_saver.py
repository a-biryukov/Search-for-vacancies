import os
import json

from src.abstract_classes import AbstractSaver


class JSONSaver(AbstractSaver):
    """ Класс для работы с данными в JSON файлах """
    def __init__(self):
        self.file_path = self.get_file_path()

    def add_vacancy(self, vacancy_object) -> None:
        """ Сохраняет вакансию в JSON файл"""

        if os.path.isfile(self.file_path) and os.stat(self.file_path).st_size != 0:
            data = self.load_file()
            data.append(vars(vacancy_object))

            self.write_file(data)
        else:
            self.write_file([vars(vacancy_object)])

    def delete_vacancy(self, vacancy_object) -> None:
        """
        Удаляет вакансию
        :param vacancy_object: Объект вакансии
        """
        data = self.load_file()
        for item in data:
            if item.get("url") == vacancy_object.url:
                data.remove(item)
                self.write_file(data)

    def load_file(self) -> list:
        """
        Получает данные из файла
        :return: список с данными
        """
        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def write_file(self, data: list) -> None:
        """
        Записывает данные в файл
        :param data: Список с данными
        """
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

    @staticmethod
    def get_file_path():
        """
        :return: Путь к файлу vacancies.json
        """
        current_file_path = os.path.abspath(__file__)
        parent_dir_path = os.path.dirname(os.path.dirname(current_file_path))
        return os.path.join(parent_dir_path, "data", "vacancies.json")