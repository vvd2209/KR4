# -*- coding: utf-8 -*-
from src.json_keeping import JSONKeeping
from src.vacancy import Vacancy
from src.vacancy_handler import VacancyHandler
from utils import user_interaction


def main():
    # Создаём экземпляр класса для работы с JSON
    json_saver = JSONKeeping('vacancies.json')
    # Записываем все полученные вакансии в JSON
    user_interaction.get_search_query_json_data(json_saver)
    # Удаляем из JSON вакансии без зарплаты
    user_interaction.remove_muddy_vacancies(json_saver)

    # Дальше работаем с экземплярами класса Vacancy
    all_vacancies_list = json_saver.json_to_instances(Vacancy)
    # Создаём экземпляр класса-обработчика сущностей вакансий
    vacancies_handler = VacancyHandler(all_vacancies_list)

    # Выводим топ N вакансий
    top_vacancies_list = user_interaction.show_top_vacancies_by_salary(vacancies_handler, all_vacancies_list)
    # Предлагаем отфильтровать топ вакансий и записываем результат в файл
    user_interaction.filter_and_save_vacancies(vacancies_handler, top_vacancies_list)

    # Очищаем файл JSON с вакансиями
    print('\nВыход из программы.')
    json_saver.clear_json_with_vacancies()


if __name__ == '__main__':
    main()