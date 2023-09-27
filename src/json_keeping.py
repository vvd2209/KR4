# -*- coding: utf-8 -*-
import os.path
import json
from abstract.abstract_keeping import VacancyKeeping
from config import JSON_DATA_DIR


class JSONKeeping(VacancyKeeping):
    """Класс для работы с файлом JSON"""

    def __init__(self, filename: str) -> None:
        """"Экземпляр класса инициализируется именем файла"""
        self.filename = os.path.join(JSON_DATA_DIR, filename)

    def save_vacancies_to_json(self, vacancy_list):
        """
        Сохраняет вакансии в JSON-файл
        :param vacancy_list: список с вакансиями
        """
        directory = os.path.dirname(self.filename)
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except OSError as e:
                print(f"Ошибка при создании директории: {e}")
                return

        try:
            with open(self.filename, 'w') as file:
                json.dump(vacancy_list, file, indent=2, ensure_ascii=False)
            print(f"Данные успешно записаны в файл: {self.filename}")
        except Exception as e:
            print(f"Ошибка при записи данных в файл: {e}")

    def load_vacancies(self):
        """Загружает данные из файла с вакансиями"""
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
            return data

        except FileNotFoundError:
            print("Файл не найден.")

        except json.JSONDecodeError:
            print("Некорректный формат JSON-файла.")

    def remove_zero_salary_vacancies(self):
        """Оставляет в файле только вакансии с зарплатой"""
        try:
            data = self.load_vacancies()

            filtered_data = [item for item in data if item['salary_from'] != 0 or item['salary_to'] != 0]

            self.save_vacancies_to_json(filtered_data)

            print(f"Вакансии с нулевой зарплатой успешно удалены. Осталось вакансий: {len(filtered_data)}")

        except FileNotFoundError:
            print("Файл не найден.")

        except json.JSONDecodeError:
            print("Некорректный формат JSON-файла.")

    def json_to_instances(self, class_name) -> list:
        """
         Преобразует словари из файла в экземпляры класса
         :param class_name: имя класса, в экземпляры которого будут преобразованы словари
         :return: список экземпляров указанного класса
         """
        instances = []

        try:
            data = self.load_vacancies()

            for item in data:
                instance = class_name(item)
                instances.append(instance)

        except FileNotFoundError:
            print("Файл не найден.")

        except json.JSONDecodeError:
            print("Некорректный формат JSON-файла.")

        return instances

    def clear_json_with_vacancies(self):
        """
        Очищает файл с вакансиями
        """
        try:
            with open(self.filename, 'w') as file:
                file.write('')
            print("Данные успешно удалены из временного файла.")
        except Exception as e:
            print(f"Ошибка при удалении данных из файла: {e}")