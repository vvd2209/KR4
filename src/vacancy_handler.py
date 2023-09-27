# -*- coding: utf-8 -*-
import os.path
import xlwt
import csv
from src.vacancy import Vacancy
from config import USER_FILE_DIR


class VacancyHandler(Vacancy):
    """Класс для работы со списком экземпляров класса Vacancy"""

    def __init__(self, vacancies_list):
        """Инициализируем экземпляр класса списком экземпляров класса Vacancy"""
        self.vacancies_list = vacancies_list

    def remove_without_salary(self) -> list:
        """
        Возвращает только вакансии с зарплатой
        """
        vacancies_with_salary = [vacancy for vacancy in self.vacancies_list
                                 if vacancy.get_avg_salary() != 0]

        return vacancies_with_salary

    def sort_vacancies_by_salary(self) -> list:
        """
        Сортирует вакансии по зарплате в порядке от большей к меньшей
        :return: отсортированный список экземпляров класса
        """
        return sorted(self.vacancies_list,
                      key=lambda x: x.get_avg_salary(), reverse=True)

    @staticmethod
    def search_instances_by_keywords(list_vacancies: list, keywords: list) -> list:
        """
        Ищет вакансии по ключевым словам
        :param list_vacancies: экземпляров класса Vacancy
        :param keywords: ключевые слова
        :return: список экземпляров класса Vacancy, в которых есть хотя бы одно из ключевых слов
        """
        matching_instances = []

        for instance in list_vacancies:
            for key, value in instance.__dict__.items():
                if any(keyword.lower() in str(value).lower() for keyword in keywords):
                    matching_instances.append(instance)
                    break

        return matching_instances

    @staticmethod
    def create_directory(directory_path):
        """
        Создаёт директорию для файлов пользователя
        :param directory_path: название директории
        """
        if not os.path.exists(directory_path):
            try:
                os.makedirs(directory_path)
            except OSError as e:
                print(f"Ошибка при создании директории {directory_path}: {e}")

    def write_vacancies_to_csv(self, filename: str, list_vacancies: list) -> None:
        """
        Записывает данные о вакансиях в файл csv
        :param filename: имя файла (без расширения)
        :param list_vacancies: список экземпляров класса Vacancy
        """
        self.create_directory(USER_FILE_DIR)
        filename = filename + '.csv'
        file_path = os.path.join(USER_FILE_DIR, filename)

        fieldnames = ['vacancy_title', 'vacancy_area', 'vacancy_url',
                      '_salary_from', '_salary_to', 'currency',
                      'experience', 'requirements']

        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for vacancy in list_vacancies:
                writer.writerow(vars(vacancy))
        print(f'Данные успешно записаны в файл CSV. Путь к файлу: {file_path}')

    def write_vacancies_to_xls(self, filename: str, list_vacancies: list) -> None:
        """
        Записывает данные о вакансиях в файл xls
        :param filename: имя файла (без расширения)
        :param list_vacancies: список экземпляров класса Vacancy
        """
        self.create_directory(USER_FILE_DIR)
        filename = filename + '.xls'
        file_path = os.path.join(USER_FILE_DIR, filename)

        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('Vacancies')

        fieldnames = ['vacancy_title', 'vacancy_area', 'vacancy_url',
                      'salary_from', 'salary_to', 'currency',
                      'experience', 'requirements']

        # Записываем заголовки полей
        for i, fieldname in enumerate(fieldnames):
            sheet.write(0, i, fieldname)

        # Записываем данные вакансий
        for row, vacancy in enumerate(list_vacancies, start=1):
            for col, fieldname in enumerate(fieldnames):
                value = getattr(vacancy, fieldname, '')
                sheet.write(row, col, value)

        workbook.save(file_path)
        print(f'Данные успешно записаны в файл XLS. Путь к файлу: {file_path}')