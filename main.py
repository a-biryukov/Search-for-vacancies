from src.class_headhunter_api import HeadHunterAPI
from src.class_vacancy import Vacancy
from src.class_exchange_rates import ExchangeRates
from src.class_json_saver import JSONSaver


def user_interaction():
    while True:
        search_query = input("Введите поисковый запрос: ")

        area_search = input("Введите страну, область или город: ").strip()

        while True:
            salary = input("Введите желаемую зарплату в рублях: ")
            salary_list = salary.split("-") if "-" in salary else salary.split(" ")
            if len(salary_list) == 2:
                if not salary_list[0].strip().isdigit() or not salary_list[1].strip().isdigit():
                    print("Вводить можно только цифры. В качестве разделителя можно использовать '-' или пробел")
                    print("Пример: 10000 или 10000 - 50000")
                    print("Попробуйте еще раз")
                    continue
                else:
                    break
            elif len(salary_list) == 1:
                if not salary_list[0].strip().isdigit():
                    print("Вводить можно только цифры. В качестве разделителя можно использовать '-' или пробел")
                    print("Пример: 10000 или 10000 - 50000")
                    print("Попробуйте еще раз")
                    continue
                else:
                    break
            else:
                print("Вводить можно только цифры. В качестве разделителя можно использовать '-' или пробел")
                print("Пример: 10000 или 10000 - 50000")
                print("Попробуйте еще раз")
                continue

        only_with_salary = input("Показывать вакансии в которых не указана зарплата? (да/нет): ").strip()

        filter_words = input("Можете указать через пробел ключевые слова для фильтрации вакансий: ").split()

        while True:
            top_n = input("Введите количество вакансий для вывода в топ N: ").strip()
            if top_n == "":
                break
            elif not top_n.isdigit():
                print("Вводить можно только цифры, попробуйте еще раз")
                continue
            else:
                break

        hh_api = HeadHunterAPI(search_query, salary_list, area_search, only_with_salary)

        er = ExchangeRates()

        exchange_rates = er.get_exchange_rates()

        try:
            vacancy_list = hh_api.get_vacancies()

            vacancy_objects = Vacancy.cast_to_object_list(vacancy_list, exchange_rates)

            filtered_vacancies = Vacancy.filtered_vacancies(vacancy_objects, filter_words)

            sorted_vacancies = Vacancy.sort_vacancies_by_salary(filtered_vacancies, salary_list)

            top_vacancies = Vacancy.get_top_vacancies(sorted_vacancies, top_n)
        except AttributeError as ae:
            print(ae, end=" ")
            print("Попробуйте ещё раз.\n")
            continue
        else:
            json_save = JSONSaver()

            print(f"\nПо вашему запросу найдено вакансий: {len(top_vacancies)}\n")

            for vacancy in top_vacancies:
                json_save.add_vacancy(vacancy)
                print(vacancy)

            new_search = input("Желаете сделать новый запрос? (да/нет): \n").strip()
            if new_search == "да":
                continue
            else:
                break


if __name__ == "__main__":
    user_interaction()
