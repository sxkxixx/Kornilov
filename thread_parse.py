import pandas as pd
import threading


class Parser:
	def __init__(self, file_name):
		self.file_name = file_name
		self.__data__ = pd.read_csv(self.file_name)

	@property
	def years(self):
		return self.__data__['published_at'].apply(lambda x: x[:4]).unique()

	def write_to_csv(self):
		thread_pool = []
		for year in self.years:
			filtered_data = self.__data__[self.__data__['published_at'].str.contains(year)]
			thread = threading.Thread(target=self.write_chunk_to_csv, args=(filtered_data, f'parsed_data/vacancies_by_{year}.csv',))
			thread.start()
			thread_pool.append(thread)
		for thread in thread_pool:
			thread.join()

	@staticmethod
	def write_chunk_to_csv(data_frame: pd.DataFrame, file_name):
		data_frame.to_csv(path_or_buf=file_name, index=False, encoding='utf-8-sig')


parser = Parser('data/vacancies_by_year.csv')
parser.write_to_csv()
