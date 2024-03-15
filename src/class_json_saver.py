import os
import json

from src.abstract_classes import AbstractSaver


class JSONSaver(AbstractSaver):
    """ Класс для работы с данными в JSON файлах """

    @staticmethod
    def add_vacancy(vacancy_object):
        """ Сохраняет вакансию в JSON файл"""
        current_file_path = os.path.abspath(__file__)
        parent_dir_path = os.path.dirname(os.path.dirname(current_file_path))
        file_path = os.path.join(parent_dir_path, "data", "vacancies.json")

        if os.path.isfile(file_path) and os.stat(file_path).st_size != 0:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                data.append(vars(vacancy_object))

            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=2)
        else:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump([vars(vacancy_object)], file, indent=2)

    @staticmethod
    def delete_vacancy(vacancy):
        pass


