import sqlite3
import pandas as pd

"""
И какую документацию сюда надо писать?
"""

con = sqlite3.connect('currency_rate.db')
df = pd.read_csv('data/currency_value.csv')
df.to_sql(name='currency_rate', con=con, index=False)
