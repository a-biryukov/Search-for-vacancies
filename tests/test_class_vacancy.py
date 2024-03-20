from src.class_vacancy import Vacancy


def test_cast_to_object_list(vacancy_info, currency_rates):
    assert len(Vacancy.cast_to_object_list(vacancy_info, currency_rates)) == 4
    assert Vacancy.cast_to_object_list(vacancy_info, currency_rates)[0].name == "Программист С++"


def test_filtered_vacancies(vacancy_objects, filter_words):
    assert len(Vacancy.filtered_vacancies(vacancy_objects,filter_words)) == 1
    assert len(Vacancy.filtered_vacancies(vacancy_objects, [])) == 4


def test_sort_vacancies_by_salary(vacancy_objects, salary_1, salary_2):
    assert Vacancy.sort_vacancies_by_salary(vacancy_objects, salary_1) == [vacancy_objects[3],
                                                                           vacancy_objects[1],
                                                                           vacancy_objects[0]]
    assert Vacancy.sort_vacancies_by_salary(vacancy_objects, salary_2) == [vacancy_objects[2],
                                                                           vacancy_objects[1],
                                                                           vacancy_objects[0]]


def test_get_top_vacancies(vacancy_objects, top_n_1, top_n_2):
    assert len(Vacancy.get_top_vacancies(vacancy_objects, top_n_2)) == 4
    assert len(Vacancy.get_top_vacancies(vacancy_objects, top_n_1)) == 2


def test_str(vacancy_objects, vacancy_str):
    assert str(vacancy_objects[3]) == vacancy_str


def test_of_comparison_methods(comparison_lt, comparison_le, comparison_eq):
    assert comparison_lt is True
    assert comparison_le is True
    assert comparison_eq is False


