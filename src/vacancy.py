# -*- coding: utf-8 -*-
class Vacancy:
    """Класс для работы с вакансиями"""

    def __init__(self, vacancy_info: dict) -> None:
        """
        Инициализируем экземпляр класса со следующими атрибутам
        vacancy_title: название вакансии
        vacancy_area: город/регион
        vacancy_url: ссылка на вакансию
        salary_from: нижний уровень зарплаты
        salary_to: верхний уровень зарплаты
        currency: валюта зарплаты
        experience: требуемый опыт работы
        requirements: требования к вакансии
        """
        self.vacancy_title = vacancy_info.get('vacancy_title')
        self.vacancy_area = vacancy_info.get('vacancy_area')
        self.vacancy_url = vacancy_info.get('vacancy_url')
        self.salary_from = vacancy_info.get('salary_from')
        self.salary_to = vacancy_info.get('salary_to')
        self.currency = vacancy_info.get('currency')
        self.experience = vacancy_info.get('experience', 'Не указано')
        self.requirements = vacancy_info.get('requirements', 'Не указано')

    def __str__(self) -> str:
        """Строковое представление вакансии"""
        return (
            f'Вакансия: {self.vacancy_title}\n'
            f'Город/регион: {self.vacancy_area}\n'
            f'Зарплата: {self.get_salary_string()}\n'
            f'Опыт работы: {self.experience}\n'
            f'Требования: {self.requirements}\n'
            f'Ссылка на вакансию: {self.vacancy_url}\n'
        )

    def __sub__(self, other) -> int or str:
        """Показывает разницу зарплат двух вакансий"""
        if isinstance(other, Vacancy):
            return self.get_avg_salary() - other.get_avg_salary()
        else:
            return '<Неизвестно>'

    def get_currency_info(self) -> str:
        """Преобразуем отображение рублей для зарплаты"""
        if self.currency.lower() in ('rur', 'rub', ''):
            self.currency = 'руб.'
        return self.currency

    def get_salary_string(self) -> str:
        """Формируем строку с зарплатой для метода __str__"""
        if self.get_avg_salary() == 0:
            return 'не указана'
        elif self.salary_to == self.salary_from:
            return f'{self.salary_to} {self.get_currency_info()}'
        else:
            return f'{self.salary_from} - {self.salary_to} {self.get_currency_info()}'

    def get_avg_salary(self) -> int:
        """Получаем среднее значение зарплаты для вакансии"""
        avg_salary = int((self.salary_from + self.salary_to) / 2)
        return avg_salary

    @property
    def salary_from(self):
        return self._salary_from

    @salary_from.setter
    def salary_from(self, value):
        self._salary_from = value

    @property
    def salary_to(self):
        return self._salary_to

    @salary_to.setter
    def salary_to(self, value):
        self._salary_to = value