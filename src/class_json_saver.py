import os
import json

from src.abstract_classes import AbstractSaver


class JSONSaver(AbstractSaver):
    """ Класс для работы с данными в JSON файлах"""

    @staticmethod
    def add_vacancy(vacancy):
        current_file_path = os.path.abspath(__file__)
        parent_dir_path = os.path.dirname(os.path.dirname(current_file_path))
        file_path = os.path.join(parent_dir_path, "data", "vacancies.json")

        with open(file_path, "w") as file:
            json.dump(vacancy, file, indent=2)

    @staticmethod
    def delete_vacancy(vacancy):
        pass
