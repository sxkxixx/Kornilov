import pandas as pd
import numpy as np


class Converter:
	"""Класс для конвертирования в рубли оклада вакансий и преобразования столбцов salary_from, salary_to, salary_currency в столбец salary
	Attributes:
		source_file (DataFrame): Преобразуемый DataFrame
		exchange_rate (DataFrame): DataFrame, с помощью которого преобразуется исходный файл
	"""
	def __init__(self, file_to_convert, exchange_rate):
		"""Инициализатор класса Converter

		:argument:
			file_to_convert (str): Файл, который нужно преобразовать
			exchange_rate (str): Файл с валюта, который преобразует исходный файл
		"""
		self.source_file = pd.read_csv(file_to_convert)
		self.exchange_rate = pd.read_csv(exchange_rate)

	def get_converted_csv(self, head=True):
		"""Конвертирует исходный csv-файл и сохраняет его в converted_dif_currencies.csv

		:argument:
			head (bool): Флаг для вывода первых 100 значений или весь исходный файл
		"""
		df = self.source_file.copy()
		if head:
			df = df.head(100)
		df['salary'] = df.apply(lambda x: self.transform_row(x), axis=1)
		df[['name', 'salary', 'area_name', 'published_at']].to_csv('converted_dif_currencies.csv', index=False)

	def transform_row(self, row):
		"""Получает и преобразует строку из исходного файла
		:argument:
			row: строка DataFrame
		"""
		salary_from, salary_to, salary_currency = row['salary_from'], row['salary_to'], row['salary_currency']
		if np.isnan(salary_from) and np.isnan(salary_to) or pd.isnull(salary_currency):
			return None
		exchange_value = self.get_converted_salary(row['published_at'], salary_currency)
		if not exchange_value:
			return None
		salary_from = 0 if np.isnan(salary_from) else salary_from
		salary_to = 0 if np.isnan(salary_to) else salary_to
		result = max(salary_from, salary_to) if salary_to == 0 or salary_from == 0 else 0.5 * (
				salary_from + salary_to)
		return round(result * exchange_value, 0)

	def get_converted_salary(self, date, currency):
		"""Берет и возвращает курс по текущей валюте в указанной дате
		:argument:
			date (str): Дата в формате 'YY-mm'
			currency (str): Код валюты
		"""
		try:
			exchange_value = self.exchange_rate[self.exchange_rate['date'] == date[:7]][currency].values
		except:
			return 1
		return exchange_value[0] if len(exchange_value) > 0 else None


converter = Converter('data/vacancies_dif_currencies.csv', 'currency_value.csv')
converter.get_converted_csv()