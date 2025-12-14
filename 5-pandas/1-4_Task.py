"""
1. Загрузите набор данных из файла train.csv с помощью библиотеки Pandas.
Вывести:
- первые 5 строк
- общую информацию (info())

2.  Посчитать количество пропусков по каждому столбцу.
и вывести долю пропусков в процентах

3. Вывести, используя print количество:
- всех выживших женщин;
- всех мужчин старше 50 лет;
- пассажиров 1 класса, заплативших больше 100 (Fare).

4*. Создайте новый столбец "age_group", который заполняется по следующим правилам:
- "child" — age < 18
- "adult" — 18–60
- "senior" — > 60

Можно заполнить с помощью функции
"""

import pandas as pd
import numpy as np

# 1. 
df = pd.read_csv('5-pandas/train.csv')
print('1.1. Первые 5 строк:')
print(df.head(5), '\n')
print('1.2. Общая информация:') 
print(df.info(), '\n')

# 2. 
print('2.1. Количество пропусков по каждому столбцу:') 
miss = df.isna().sum()
print(miss, '\n')
print('2.2. Доля пропусков в процентах:') 
print((miss/len(df)*100).round(2), '\n')

# 3.
print('3.1. Количество всех выживших женщин:', 
      ((df['Survived'] == 1) & (df['Sex'] == 'female')).sum(), '\n') 

print('3.2. Количество всех мужчин старше 50 лет:', 
      ((df['Sex'] == 'male') & (df['Age'] > 50)).sum(), '\n') 

print('3.3. Количество пассажиров 1 класса, заплативших больше 100 (Fare):', 
      ((df['Pclass'] == 1) & (df['Fare'] > 100)).sum(), '\n') 

# 4.
def get_age_category(age):
  if age < 18:
    return 'child'
  elif age >= 18 and age <= 60:
    return 'adult'
  elif age > 60:
    return "senior"
  else:
    return np.nan # Не нашла NaN в pandas

df['age_group'] = df['Age'].apply(get_age_category)
print('4. Добавлен новый столбец:')
print(df.sample(10))
