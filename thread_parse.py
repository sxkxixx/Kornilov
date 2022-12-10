import pandas as pd
import threading
from time import time

start = time()


class Parser:
	def __init__(self, file_name):
		self.file_name = file_name
		self.__data__ = pd.read_csv(self.file_name)

	def parse_to_files(self):
		thread_pool = []
		self.__data__['year'] = self.__data__['published_at'].apply(lambda x: x[:4])
		groups = self.__data__.groupby(['year'])
		for group, year in zip(groups, self.__data__['year'].unique()):
			thread = threading.Thread(target=self.write_chunk_to_csv, args=(group[1].loc[:, :'published_at'], f'parsed_data/vacancies_by_{year}.csv'))
			thread.start()
			thread_pool.append(thread)
		for thread in thread_pool:
			thread.join()

	@staticmethod
	def write_chunk_to_csv(data_frame: pd.DataFrame, file_name):
		data_frame.to_csv(path_or_buf=file_name, index=False, encoding='utf-8-sig')


parser = Parser('data/vacancies_by_year.csv')
parser.parse_to_files()
print(time() - start)
# 24с - парсинг с фильтром
# 15с - groupby