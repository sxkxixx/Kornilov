import csv
from datetime import datetime
from dateutil.parser import parse
import cProfile

example = []
with open('data/vacancies_by_year.csv', 'r', encoding='utf-8-sig') as file:
	example = [row[5] for row in csv.reader(file) if row[5] != 'published_at']


def profile_it(func):
	def wrapper(date_list):
		profile = cProfile.Profile()
		profile.enable()
		f = [func(arg) for arg in date_list]
		profile.disable()
		print('Статистика по функции', func.__name__)
		profile.print_stats(0)

	return wrapper


def test_datetime_strptime(date):
	date = datetime.strptime(date[:10], '%Y-%m-%d').date()
	return f'{date.day}.{date.month}.{date.year}'


def test_parsing_with_slices(date):
	return f'{date[8:10]}.{date[5:7]}.{date[:4]}'


def test_parsing_with_format(date):
	return '{0[2]}.{0[1]}.{0[0]}'.format(date[:10].split('-'))


def test_parsing_dateutil_parse(date):
	date = parse(date)
	return f'{date.day}.{date.month}.{date.year}'


def test_parsing_with_split(date):
	date = date.split('T')[0].split('-')
	return f'{date[-1]}.{date[1]}.{date[0]}'


pr = profile_it(test_parsing_with_split)
pr(example)
