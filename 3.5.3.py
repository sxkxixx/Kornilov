import sqlite3
import pandas as pd

# vacancy_name = input('Введите название профессии: ')
vacancy_name = 'Аналитик'
con = sqlite3.connect('currency_rate.db')
con.execute('delete from KORNILOV where salary is null')
cursor = con.cursor()


def get_salary_year_statistic():
	df = pd.read_sql(
		f"SELECT SUBSTRING(published_at, 0, 5) as year, ROUND(AVG(salary)) as avg_sal FROM KORNILOV GROUP BY year", con)
	return df.set_index('year')


def get_amount_year_statistic():
	df = pd.read_sql(f"SELECT SUBSTRING(published_at, 0, 5) as year, COUNT(*) as amount FROM KORNILOV GROUP BY year",
	                 con)
	return df.set_index('year')


def get_salary_vacancy_statistic():
	df = pd.read_sql(
		f"SELECT SUBSTRING(published_at, 0, 5) as year, ROUND(AVG(salary)) as avg_sal FROM KORNILOV WHERE name LIKE '%{vacancy_name}%' GROUP BY year",
		con)
	return df.set_index('year')


def get_amount_vacancy_statistic():
	df = pd.read_sql(
		f"SELECT SUBSTRING(published_at, 0, 5) as year, COUNT(*) as amount FROM KORNILOV WHERE name LIKE '%{vacancy_name}%' GROUP BY year",
		con)
	return df.set_index('year')


def get_city_salary_statistic():
	df = pd.read_sql(f"""SELECT area_name, ROUND(AVG(salary), 2) AS salary
        FROM KORNILOV
        GROUP BY area_name
        HAVING COUNT(*) >= (SELECT COUNT(*) FROM KORNILOV) / 100
        ORDER BY ROUND(AVG(salary), 2) DESC 
        LIMIT 10
        """, con)
	return df


def get_city_share():
	df = pd.read_sql(f"""SELECT area_name, 
        100 * COUNT(*) / (select COUNT(*) from KORNILOV) AS share 
        FROM KORNILOV
        GROUP BY area_name
        HAVING COUNT(*) >= (SELECT COUNT(*) FROM KORNILOV) / 100
        ORDER BY COUNT(*) DESC 
        LIMIT 10
        """, con)
	return df


print(get_city_salary_statistic())
print()
print(get_amount_year_statistic())
print()
print(get_salary_vacancy_statistic())
print()
print(get_amount_vacancy_statistic())
print()
print(get_city_salary_statistic())
print()
print(get_city_share())
