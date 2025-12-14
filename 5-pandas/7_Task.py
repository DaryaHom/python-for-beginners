"""
7. На основе полученных данных определить, в каком классе пассажиры выживали чаще.
Можно применить barplot:
- Ось X — класс (Pclass), 
- Ось Y — доля выживших.
На основе графика определить, в каком классе наибольшее количество выживших пассажиров.
"""

import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt 

matplotlib.use("TkAgg") # Указываю бэкенд, чтобы избежать конфликта версий со средой

df = pd.read_csv('5-pandas/train.csv')

survived = df.groupby('Pclass')['Survived'].sum()
ax = sns.barplot(data=survived)

ax.set_title("Распределение выживших пассажиров по классам")
ax.set_xlabel("Класс")
ax.set_ylabel("Количество выживших")

plt.show() # В VsCode диаграмма не отображается без явной команды вывода 
# Наибольшее количество выживших пассажиров - в 1-м классе.
