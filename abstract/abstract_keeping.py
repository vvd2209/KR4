# -*- coding: utf-8 -*-
from abc import abstractmethod, ABC


class VacancyKeeping(ABC):
    @abstractmethod
    def save_vacancies_to_json(self, vacancy_list):
        """
        Сохраняет вакансии в JSON-файл
        :param vacancy_list: список с вакансиями
        """
        pass

    @abstractmethod
    def load_vacancies(self):
        """Загружает данные из файла с вакансиями"""
        pass

    @abstractmethod
    def json_to_instances(self, class_name):
        """
        Преобразует словари из файла в экземпляры класса
        :param class_name: Имя класса, в экземпляры которого будут преобразованы словари
        """
        pass

    @abstractmethod
    def clear_json_with_vacancies(self):
        """
        Очищает файл с вакансиями
        """
        pass