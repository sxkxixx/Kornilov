import pandas as pd
import numpy as np


# class Converter:
# 	def __init__(self, file_to_convert, exchange_rate):
# 		self.source_file = pd.read_csv(file_to_convert)
# 		self.exchange_rate = pd.read_csv(exchange_rate)
#
# 	def get_converted_dataframe(self, head=False, save=False):
# 		df = self.source_file.copy()
# 		if head:
# 			df = df.head(100)
# 		df['salary'] = df.apply(lambda x: self.transform_row(x), axis=1)
# 		df = df[['name', 'salary', 'area_name', 'published_at']]
# 		if save:
# 			df.to_csv('converted_dif_currencies.csv', index=False)
# 		return df
#
# 	def transform_row(self, row):
# 		salary_from, salary_to, salary_currency = row['salary_from'], row['salary_to'], row['salary_currency']
# 		if np.isnan(salary_from) and np.isnan(salary_to) or pd.isnull(salary_currency):
# 			return None
# 		exchange_value = self.get_converted_salary(row['published_at'], salary_currency)
# 		if not exchange_value:
# 			return None
# 		salary_from = 0 if np.isnan(salary_from) else salary_from
# 		salary_to = 0 if np.isnan(salary_to) else salary_to
# 		result = max(salary_from, salary_to) if salary_to == 0 or salary_from == 0 else 0.5 * (
# 				salary_from + salary_to)
# 		return round(result * exchange_value, 0)
#
# 	def get_converted_salary(self, date, currency):
# 		try:
# 			exchange_value = self.exchange_rate[self.exchange_rate['date'] == date[:7]][currency].values
# 		except:
# 			return 1
# 		return exchange_value[0] if len(exchange_value) > 0 else None
#
#
# converter = Converter('filtered_dif_currencies.csv', 'currency_value.csv')
# converted_dataframe = converter.get_converted_dataframe(save=True)
# converted_dataframe = pd.read_csv('converted_dif_currencies.csv')


# class Analytic:
# 	def __init__(self, file_name, vacancy_name):
# 		self.frame = pd.read_csv(file_name)
# 		self.chosen_vacancy = vacancy_name
#
# 	def get_file_analytic(self):
# 		self.frame['year'] = self.frame['published_at'].apply(lambda x: x[:4])
# 		groups = self.frame.groupby(['year'])
# 		salary, vacancies_amount, this_vacancy_salary, this_vacancy_amount = {}, {}, {}, {}
# 		for year, df in groups:
# 			amount, avg_salary, chosen_vacancy_amount, chosen_vacancy_avg_salary = self.get_year_analytic(df)
# 			salary[year] = avg_salary
# 			vacancies_amount[year] = amount
# 			this_vacancy_salary[year] = chosen_vacancy_avg_salary
# 			this_vacancy_amount[year] = chosen_vacancy_amount
# 		return salary, vacancies_amount, this_vacancy_salary, this_vacancy_amount, *self.get_city_analytics()
#
#
# 	def get_year_analytic(self, df: pd.DataFrame):
# 		df_chosen_vacancy = df[df['name'].str.contains(self.chosen_vacancy)]
# 		average_salary = round(df.apply(lambda x: x['salary'] * 0.5, axis=1).mean())
# 		this_vacancy_salary_average = round(
# 			df_chosen_vacancy.apply(lambda x: x['salary'] * 0.5, axis=1).mean())
# 		return df.shape[0], average_salary, df_chosen_vacancy.shape[0], this_vacancy_salary_average
#
# 	def get_city_analytics(self):
# 		rows = self.frame.shape[0]
# 		cities_count = self.frame['area_name'].value_counts().to_dict()
# 		cities_share = dict(filter(lambda x: x[-1] > 0.01, [(key, round(value / rows, 4)) for key, value in cities_count.items()]))
# 		groups = self.frame.groupby(['area_name'])
# 		salary_city = {}
# 		for city, df in groups:
# 			if city not in cities_share:
# 				continue
# 			salary_city[city] = round(df['salary'].mean())
# 		return dict(sorted(salary_city.items(), key=lambda x: x[-1], reverse=True)), cities_share
#
#
# analytic = Analytic('converted_dif_currencies.csv', 'Системный инженер')
# titles = ['Динамика уровня зарплат по годам: ',
#           'Динамика количества вакансий по годам: ',
#           'Динамика уровня зарплат по годам для выбранной профессии: ',
#           'Динамика количества вакансий по годам для выбранной профессии: ',
#           'ровень зарплат по городам (в порядке убывания): ',
#           'Доля вакансий по городам (в порядке убывания):']
# print(*zip(titles, *analytic.get_file_analytic()), sep='\n')
