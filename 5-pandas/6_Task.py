"""
6.  С использованием Seaborn определить, сколько людей было в каждом классе (столбец: Pclass).
Можно применить гистограмму.
- Ось X — класс (Pclass), 
- Ось Y — количество пассажиров.
На основе графика определить, в каком классе наибольшее количество пассажиров.
"""

import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt 

matplotlib.use("TkAgg") # Указываю бэкенд, чтобы избежать конфликта версий со средой

df = pd.read_csv('5-pandas/train.csv')

ax = sns.histplot(
    df['Pclass'], 
    discrete=True,
    shrink=0.8)

ax.set_title("Распределение пассажиров по классам")
ax.set_xticks([1,2,3])
ax.set_xlabel("Класс")
ax.set_ylabel("Количество пассажиров")

plt.show() # В VsCode диаграмма не отображается без явной команды вывода 
# Наибольшее количество пассажиров в 3-м классе.
