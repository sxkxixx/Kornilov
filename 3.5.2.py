import pandas as pd
import numpy as np
import sqlite3

con = sqlite3.connect('currency_rate.db')
cursor = con.cursor()
df = pd.read_csv('data/vacancies_dif_currencies.csv')


def get_db_rate(currency_code, date):
	"""Функция достает курс указанной валюты в указанную дату
	:argument:
		currency_code (str): Код валюты
		date (str): Дата в формате YYYY-MM
	:returns:
		(float): Курс валюты
	"""
	if currency_code == 'RUR':
		return 1
	try:
		result = cursor.execute(f'SELECT {currency_code} FROM currency_rate WHERE date=?', (date,)).fetchone()
	except:
		return None
	return None if result is None else result[0]


def transform_row(row):
	"""Функция для получения столбца salary и строки DataFrame
	:argument:
		row: Строка DataFrame
	:returns:
		float / None: Результат ячейки в столбце salary
	"""
	salary_from, salary_to, salary_currency = row['salary_from'], row['salary_to'], row['salary_currency']
	if np.isnan(salary_from) and np.isnan(salary_to) or pd.isnull(salary_currency):
		return None
	date = row['published_at'][:7]
	exchange_value = get_db_rate(salary_currency, date)
	if not exchange_value:
		return None
	salary_from = 0 if np.isnan(salary_from) else salary_from
	salary_to = 0 if np.isnan(salary_to) else salary_to
	result = max(salary_from, salary_to) if salary_to == 0 or salary_from == 0 else 0.5 * (salary_from + salary_to)
	return round(result * exchange_value, 0)



df['salary'] = df.apply(lambda x: transform_row(x), axis=1)
df = df[['name', 'salary', 'area_name', 'published_at']]
df.to_sql('KORNILOV', con=con, index=False)
