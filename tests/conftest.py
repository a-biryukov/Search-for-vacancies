import pytest

from src.class_vacancy import Vacancy

VACANCY_INFO = [
  {
    "name": "Программист С++",
    "url": "https://hh.ru/vacancy/92363385",
    "salary": None,
    "salary_indicated": True,
    "snippet": {
      "requirement": "Знание принципов работы ОС (Linux). Опыт разработки многопоточных высоконагруженных приложений."
                     " Опыт разработки приложений с использованием DPDK. Умение оптимизировать код с...",
      "responsibility": "Разработка модулей обработчика сетевых пакетов. Исследование и оптимизация производительности "
                        "приложения. Участие в code review, контроль качества кода. Работа в команде..."
    },
    "the_date": "01.03.2024",
    "area": "Москва"
  },
  {
    "name": "Python-разработчик",
    "url": "https://hh.ru/vacancy/93914138",
    "salary": {
      "from": 425000,
      "currency": "RUR"
    },
    "salary_indicated": True,
    "snippet": {
      "requirement": None,
      "responsibility": "Участвовать в развитии и запуске продуктов на Python. Писать код на </highlighttext> Python,"
                        " который легко читать, поддерживать и развивать."
    },
    "the_date": "13.03.2024",
    "area": "Москва"
  },
  {
    "name": "Middle Python Developer",
    "url": "https://hh.ru/vacancy/94747936",
    "salary": {
      "to": 5500,
      "currency": "EUR"
    },
    "salary_indicated": True,
    "snippet": {
      "requirement": "Опыт от 5 лет в разработке. <highlighttext> Хорошее знание Python, Django, Flask, Asyncio,"
                     " Celery, Selenium. Умении проектировать структуру SQL и NoSQL...",
      "responsibility": None
    },
    "the_date": "24.02.2024",
    "area": "Москва"
  },
  {
    "name": "Продуктовый аналитик",
    "url": "https://hh.ru/vacancy/94619501",
    "salary": {
      "from": 250000,
      "to": 350000
    },
    "salary_indicated": None,
    "snippet": {},
    "the_date": "18.03.2024",
    "area": "Москва"
  }
]

CURRENCY_RATES = {
    "USD": 90,
    "EUR": 100
}

FILTER_WORDS = ["продукт", "Умение", "Знание"]

SALARY_1 = ["250000", "460000"]

SALARY_2 = ["400000"]


VACANCY_STR = """Вакансия: Продуктовый аналитик
Москва
Требования: не указаны
Обязанности: не указаны
Зарплата от 250000 до 350000 рублей
Дата публикации: 18.03.2024
Ссылка на вакансию: https://hh.ru/vacancy/94619501
"""


@pytest.fixture
def vacancy_info():
    return VACANCY_INFO


@pytest.fixture
def currency_rates():
    return CURRENCY_RATES


@pytest.fixture
def vacancy_objects():
    return Vacancy.cast_to_object_list(VACANCY_INFO, CURRENCY_RATES)


@pytest.fixture
def filter_words():
    return FILTER_WORDS


@pytest.fixture
def salary_1():
    return SALARY_1


@pytest.fixture
def salary_2():
    return SALARY_2


@pytest.fixture
def vacancy_str():
    return VACANCY_STR


@pytest.fixture
def comparison_lt():
    vacancy_objects = Vacancy.cast_to_object_list(VACANCY_INFO, CURRENCY_RATES)
    return vacancy_objects[2] > vacancy_objects[3]


@pytest.fixture
def comparison_le():
    vacancy_objects = Vacancy.cast_to_object_list(VACANCY_INFO, CURRENCY_RATES)
    return vacancy_objects[1] >= vacancy_objects[3]


@pytest.fixture
def comparison_eq():
    vacancy_objects = Vacancy.cast_to_object_list(VACANCY_INFO, CURRENCY_RATES)
    return vacancy_objects[3] == vacancy_objects[2]
