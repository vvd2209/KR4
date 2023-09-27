# -*- coding: utf-8 -*-
from abstract.abstract_api import VacancyByAPI
import requests
import os


class SuperJobAPI(VacancyByAPI):
    """Класс для работы с API SuperJob"""

    _base_url = 'https://api.superjob.ru/2.0/vacancies'
    _API_KEY: str = os.getenv('API_KEY_SJOB')

    def __init__(self, page=0, per_page=1) -> None:
        """
        Инициализатор экземпляров класса для работы с API
        :param page: страница поиска (по умолчанию)
        :param per_page: количество вакансий
        """
        self.page = page
        self.per_page = per_page

    def __str__(self):
        return 'SuperJob'

    def get_vacancies_by_api(self, vacancy_title: str) -> list[dict] or list:
        """
        Выполняет сбор вакансий через API
        :param vacancy_title: название вакансии
        :return: список вакансий для создания экземпляров класса Vacancy
        """
        headers = {'X-Api-App-Id': self._API_KEY}
        params = {
            'keyword': vacancy_title,
            'page': self.page,
            'count': self.per_page
        }
        response = requests.get(self._base_url, headers=headers, params=params)
        if response.status_code == 200:
            vacancies = response.json()['objects']

            if vacancies:
                list_vacancies = self.__class__.organize_vacancy_info(vacancies)
                return list_vacancies
            return []

        else:
            print(f'Ошибка {response.status_code} при выполнении запроса')
            return []

    @staticmethod
    def organize_vacancy_info(vacancy_data: list) -> list:
        """
        Организует данные о вакансиях в определённом виде
        :param vacancy_data: список вакансий, полученный через API
        :return: организованный список вакансий
        """

        organized_vacancy_list = []

        for vacancy in vacancy_data:
            vacancy_title = vacancy.get('profession')
            vacancy_area = vacancy.get('town')['title']
            vacancy_url = vacancy.get('link')
            salary_from = vacancy.get('payment_from')
            salary_to = vacancy.get('payment_to')
            if not salary_from:
                salary_from = salary_to
            if not salary_to:
                salary_to = salary_from
            currency = vacancy.get('currency')
            experience = vacancy.get('experience')['title']
            requirements = vacancy.get('candidat')
            if requirements:
                requirements = requirements.strip().replace('\n', '')

            vacancy_info = {
                'vacancy_title': vacancy_title,
                'vacancy_area': vacancy_area,
                'vacancy_url': vacancy_url,
                'salary_from': salary_from,
                'salary_to': salary_to,
                'currency': currency,
                'experience': experience,
                'requirements': requirements,
            }

            organized_vacancy_list.append(vacancy_info)

        return organized_vacancy_list