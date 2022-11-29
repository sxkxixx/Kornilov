from unittest import TestCase, main
from main import Salary, Vacancy, DataSet, Report


class SalaryTest(TestCase):
	def test_salary_type(self):
		self.assertEqual(type(Salary(10, 20, 'RUR')).__name__, 'Salary')

	def test_salary_from(self):
		self.assertEqual(Salary(10, 20, 'RUR').salary_from, 10)

	def test_salary_to(self):
		self.assertEqual(Salary(10, 20, 'RUR').salary_to, 20)

	def test_float_salary_from(self):
		self.assertEqual(Salary(10.1, 20.1, 'RUR').salary_from, 10)

	def test_str_salary_from(self):
		self.assertEqual(Salary('10.1', 20.1, 'RUR').salary_from, 10)

	def test_float_salary_to(self):
		self.assertEqual(Salary(10, 20.1, 'RUR').salary_to, 20)

	def test_str_salary_to(self):
		self.assertEqual(Salary(10, '20.1', 'RUR').salary_to, 20)

	def test_salary_currency(self):
		self.assertEqual(Salary(10, 20, 'RUR').salary_currency, 'RUR')

	def test_simple_salary_get_average(self):
		self.assertEqual(Salary(10, 20, 'RUR').get_average(), 15.0)

	def test_float_salary_get_average(self):
		self.assertEqual(Salary(10.1, 20.1, 'RUR').get_average(), 15.0)

	def test_euro_float_salary_get_average(self):
		self.assertEqual(Salary(10.1, 20.1, 'EUR').get_average(), 898.5)

	def test_kzt_str_salary_get_average(self):
		self.assertEqual(Salary('130', '260', 'KZT').get_average(), 25.35)


vacancy_dct = {'name': 'Программист', 'salary_from': '10', 'salary_to': '20', 'salary_currency': 'RUR',
               'area_name': 'Екатеринбург', 'published_at': '2007-12-03T17:40:09+0300'}


class VacancyTest(TestCase):
	def test_vacancy_type(self):
		self.assertEqual(type(Vacancy(vacancy_dct)).__name__, 'Vacancy')

	def test_vacancy_name(self):
		self.assertEqual(Vacancy(vacancy_dct).name, 'Программист')

	def test_vacancy_salary_to(self):
		self.assertEqual(Vacancy(vacancy_dct).salary.salary_to, 20)

	def test_vacancy_salary_from(self):
		self.assertEqual(Vacancy(vacancy_dct).salary.salary_from, 10)

	def test_vacancy_salary_currency(self):
		self.assertEqual(Vacancy(vacancy_dct).salary.salary_currency, 'RUR')

	def test_vacancy_average_salary(self):
		self.assertEqual(Vacancy(vacancy_dct).salary.get_average(), 15.0)

	def test_vacancy_published_year(self):
		self.assertEqual(Vacancy(vacancy_dct).get_year(), 2007)


if __name__ == '__main__':
	main()
