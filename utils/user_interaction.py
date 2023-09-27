# -*- coding: utf-8 -*-
from src.hh import HeadHunterAPI
from src.sjob import SuperJobAPI
from config import MAX_VACANCIES


def get_search_query_json_data(json_instance):
    """
    Выполняет поиск по сайтам вакансий и записывает результаты в файл JSON
    """
    search_query = input('Введите базовый запрос для поиска вакансии: ')
    number_of_vacancies = input(f'Сколько вакансий необходимо получить с каждого сайта (не более {MAX_VACANCIES}): ')

    try:
        number_of_vacancies = int(number_of_vacancies)
        if number_of_vacancies <= 0 or number_of_vacancies > MAX_VACANCIES:
            number_of_vacancies = MAX_VACANCIES
    except ValueError:
        number_of_vacancies = MAX_VACANCIES

    # Создаём экземпляры классов для работы с API сайтов с вакансиями
    hh_provider = HeadHunterAPI(per_page=number_of_vacancies)
    sj_provider = SuperJobAPI(per_page=number_of_vacancies)

    # Создаём список экземпляров классов для работы с API сайтов с вакансиями
    platforms = [hh_provider, sj_provider]

    # Получаем список с вакансиями
    vacancies_data = []
    for provider in platforms:
        vacancies_data += provider.get_vacancies_by_api(search_query)

    if not vacancies_data:
        print('К сожалению, не удалось найти вакансии по вашему запросу')
        exit(0)
    else:
        print(f'Получено {len(vacancies_data)} вакансий с сайтов {[str(i) for i in platforms]}\n')
        json_instance.save_vacancies_to_json(vacancies_data)


def remove_muddy_vacancies(json_instance):
    """
    Удаляет из JSON-файла записи о вакансиях, в которых не указана зарплата
    :param json_instance: экземпляр класса для работы с JSON
    """
    while True:
        choice = input('Удалить вакансии с ненулевой зарплатой. 0 - нет, 1 - да ')
        if choice == '0':
            break
        elif choice == '1':
            json_instance.remove_zero_salary_vacancies()
            break
        else:
            print('Некорректный ввод')


def show_top_vacancies_by_salary(handler, vacancies_list: list) -> list:
    """
    Выводит топ вакансий по зарплате
    :param handler: экземпляр класса-обработчика вакансий
    :param vacancies_list: список вакансий
    :return: список вакансий, отсортированных по зарплате или пустой список
    """
    while True:
        choice = input(f'\nВведите количество вакансий для вывода в топ N - от 1 до {len(vacancies_list)}: ')
        if choice == '0' or choice == '':
            print(f'Число должно быть больше 0 и меньше {len(vacancies_list)}')
        else:
            try:
                choice = int(choice)
                if 0 < choice < len(vacancies_list):
                    sorted_vacancies = handler.sort_vacancies_by_salary()[:choice]
                else:
                    sorted_vacancies = handler.sort_vacancies_by_salary()

                highest_paid = sorted_vacancies[0]
                lowest_paid = sorted_vacancies[-1]

                print(f'\nРазбег усреднённых зарплат в этом диапазоне вакансий равен '
                      f'{highest_paid - lowest_paid} руб.\n')

                for vacancy in sorted_vacancies:
                    print(vacancy)
                    print()

                return sorted_vacancies

            except TypeError:
                print('Некорректный ввод. Вакансии не будут показаны.')
                return []


def filter_and_save_vacancies(handler, top_vacancies: list) -> None:
    """
    Выводит на экран или сохраняет вакансии по заданным критериям
    :param json_instance: экземпляр класса для работы с JSON
    :param handler: экземпляр класса-обработчика вакансий
    :param top_vacancies: список из вакансий топ N по зарплате
    """
    filter_words = input('Введите ключевые слова через пробел для фильтрации в топе вакансий\n'
                         'или Enter, чтобы пропустить этот шаг: ').split()

    if filter_words:
        filtered_list = handler.search_instances_by_keywords(top_vacancies, filter_words)
        if filtered_list:
            print(f'\nОтобрано {len(filtered_list)} вакансий, в которых есть хотя бы одно из ключевых слов\n')
            while True:
                choice = input('Выберите действие: 0 - выйти, 1 - показать вакансии, 2 - записать вакансии в файл ')
                if choice == '0':
                    print('Всего доброго!')
                    exit(0)
                if choice == '1':
                    for vacancy in filtered_list:
                        print(vacancy)
                    break
                elif choice == '2':
                    save_to_file(handler, filtered_list)
                    break
                else:
                    print('Некорректный ввод.')
        else:
            print('Нет вакансий, соответствующих заданным критериям.')
    else:
        print('Вы не ввели слова для фильтрации. Сохранить топ N вакансий в файл?\n')

        while True:
            choice = input('Выберите действие: 0 - выйти из программы, 1 - записать вакансии в файл ')
            if choice == '0':
                print('Всего доброго!')
                break
            elif choice == '1':
                save_to_file(handler, top_vacancies)
                break
            else:
                print('Некорректный ввод.')


def save_to_file(handler, vacancies_list: list):
    """
    Сохраняет вакансии в файл csv или xls c заданным именем
    :param handler: экземпляр класса-обработчика вакансий
    :param vacancies_list: список вакансий
    """
    while True:
        file_format = input('Выберите формат файла: 0 - csv, 1 - xls ')
        if file_format not in ('0', '1'):
            print('Некорректный ввод')
            continue
        filename = input('Введите имя файла (без расширения): ')
        if filename == '':
            filename = 'vacancies'
        if file_format == '0':
            handler.write_vacancies_to_csv(filename, vacancies_list)
            break
        elif file_format == '1':
            handler.write_vacancies_to_xls(filename, vacancies_list)
            break
        else:
            print('Некорректный ввод')