import re
import pandas as pd

"""
Функции для работы с данными
	- extract_emails(text) — находит все email-адреса в строке. 
   Поиск нужно реализовать через регулярные выражения.

	- read_csv_to_df(file_path)  — работает с pd.DataFrame: 
   читает CSV-файл и удаляет строки с пропущенными значениями.
"""

_PATTERN_EMAIL = re.compile('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$')

def extract_emails(text: str):
   return re.fullmatch(_PATTERN_EMAIL, text) is not None

def read_csv_to_df(file_path: str) -> pd.DataFrame:
   return pd.read_csv(file_path).dropna()
