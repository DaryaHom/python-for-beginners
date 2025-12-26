import tkinter as tk
from tkinter import W, ttk, messagebox
import psycopg2
import pandas as pd


# ===== Подключение к базе =====
conn = psycopg2.connect(
    host="localhost",
    database="te1",  # имя вашей базы
    user="postgres",
    password="1234",
    port=5432
)

cur = conn.cursor()


# ===== Главное окно =====
root = tk.Tk()
root.title("CRUD с PostgreSQL")
root.geometry("500x400")


# ===== Поля ввода =====
ttk.Label(root, text="Имя:").pack(pady=5)
name_entry = ttk.Entry(root)
name_entry.pack(fill="x", padx=10)

ttk.Label(root, text="Возраст:").pack(pady=5)
age_entry = ttk.Entry(root)
age_entry.pack(fill="x", padx=10)

filter_frame = ttk.Frame(root)
filter_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(filter_frame, text="Возраст от:").pack(side="left", padx=(0, 5))
age_from_entry = ttk.Entry(filter_frame, width=10)
age_from_entry.pack(side="left", padx=(0, 10))

ttk.Label(filter_frame, text="до:").pack(side="left", padx=(0, 5))
age_to_entry = ttk.Entry(filter_frame, width=10)
age_to_entry.pack(side="left", padx=(0, 10))


# ===== Функции =====
def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)

def refresh_table():
    """Обновляем таблицу, загружая данные из базы"""
    for row in table.get_children():
        table.delete(row)
    cur.execute("SELECT * FROM users ORDER BY id")
    for row in cur.fetchall():
        table.insert("", "end", values=row)

def add_data():
    name = name_entry.get()
    age = age_entry.get()
    if name == "" or age == "":
        messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля")
        return
    cur.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
    conn.commit()
    refresh_table()
    clear_fields()

"""
Задание №1. Пропишите реализацию функции "update_data" (она аналогична функции удаления)
Пользователь выбирает строку в таблице. Вводит новые значения "Имя" и "Возраст".
Нажимает кнопку «Обновить». Приложение должно проверить, что строка выбрана; проверить, что поля не пусты.
"""
def update_data():
    selected = table.focus()
    if not selected:
        messagebox.showerror("Ошибка", "Выберите строку для обновления")
        return
    row_id = table.item(selected, "values")[0]
    name = name_entry.get()
    if not name:
        messagebox.showerror("Ошибка", "Введите новое имя")
        return
    age = age_entry.get()
    if not age:
        messagebox.showerror("Ошибка", "Введите новый возраст")
        return
    cur.execute("UPDATE users SET name = %s, age = %s WHERE id=%s", (name, age, row_id))
    conn.commit()
    refresh_table()
    clear_fields()

def delete_data():
    selected = table.focus()
    if not selected:
        messagebox.showwarning("Ошибка", "Выберите строку для удаления")
        return
    row_id = table.item(selected, "values")[0]
    cur.execute("DELETE FROM users WHERE id=%s", (row_id,))
    conn.commit()
    refresh_table()
    clear_fields()

def export_to_excel():
    """Выгрузка данных в Excel"""
    cur.execute("SELECT * FROM users ORDER BY id")
    rows = cur.fetchall()
    df = pd.DataFrame(rows, columns=["ID", "Имя", "Возраст"])
    df.to_excel("users.xlsx", index=False)
    messagebox.showinfo("Успех", "Данные успешно экспортированы в users.xlsx")

def top_5():
    """Показать ТОП-5 самых "пожилых" пользователей"""
    cur.execute("SELECT name, age FROM users ORDER BY age DESC LIMIT 5")
    rows = cur.fetchall()
    if not rows:
        messagebox.showerror("Ошибка", "Нет данных в таблице.")
        return
    message = ''
    for row in rows:
        message += f"Имя: {row[0]}, Возраст: {row[1]}\n"

    messagebox.showinfo("ТОП-5", message)

def filter_by_age():
    """Фильтр по возрасту"""
    from_val = age_from_entry.get().strip()
    to_val = age_to_entry.get().strip()

    if not from_val and not to_val:  # Если оба поля пустые, показываем всё
        refresh_table()
        return

    try:
        min_age = int(from_val) if from_val else 0
        max_age = int(to_val) if to_val else 1000
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные числа в поля возраста") 
        return

    cur.execute("SELECT * FROM users WHERE age >= %s AND age <= %s ORDER BY age", (min_age, max_age))
    rows = cur.fetchall()

    for item in table.get_children():
        table.delete(item)
    for row in rows:
        table.insert("", "end", values=row)

def show_stat():
    """Статистика"""
    cur.execute("SELECT COUNT(*) FROM users")
    cnt = cur.fetchone()

    cur.execute("SELECT ROUND(AVG(age), 2) FROM users")
    avg_age = cur.fetchone()

    cur.execute("SELECT name FROM users ORDER BY age LIMIT 1")
    youngest = cur.fetchone()

    cur.execute("SELECT name FROM users ORDER BY age DESC LIMIT 1")
    oldest = cur.fetchone()

    message = f'Кол-во пользователей: {cnt[0]},\n \
    Средний возраст: {avg_age[0]}\n \
    Самый младший: {youngest[0]}\n \
    Самый старший: {oldest[0]}'

    messagebox.showinfo("Статистика", message)

def sort(table, col, descending):
    """Сортировка по клику по колонке"""
    data = [(table.set(item, col), item) for item in table.get_children("")]
    data.sort(key=lambda x: int(x[0]), reverse=descending)
    for index,  (_, item) in enumerate(data):
        table.move(item, "", index)
    table.heading(col, command=lambda: sort(table, col, not descending))


# ===== Кнопки =====
tk.Button(root, text="Добавить", command=add_data, bg="lightgreen", fg="black").pack(fill="x", padx=10, pady=5)
tk.Button(root, text="Удалить", command=delete_data, bg="lightcoral", fg="black").pack(fill="x", padx=10, pady=5)
tk.Button(root, text="Обновить", command=update_data, bg="lightblue", fg="black").pack(fill="x", padx=10, pady=5)
tk.Button(root, text="Очистить поля", command=clear_fields).pack(fill="x", padx=10, pady=5)
tk.Button(root, text="Экспорт в Excel", command=export_to_excel).pack(fill="x", padx=10, pady=5)
"""
Задание №2. 
Создать кнопку, при нажатии которой таблица должна показать ТОП-5 самых "пожилых" пользователей 
(Отобразить только эти 5 записей, для теста добавить свыше 10 значений).
"""
tk.Button(root, text="ТОП-5 самых 'пожилых' пользователей", command=top_5).pack(fill="x", padx=10, pady=5)
"""
Дополнительные задачи: сделать фильтр по возрасту, 
предоставив возможность искать в промежутке от и до (пример: от 0 до 18 лет, диапазоном)
"""
ttk.Button(filter_frame, text="Фильтр", command=filter_by_age).pack(side="left", padx=10, pady=5)
"""
Кнопка "Статистика", выводит messagebox:
- Количество пользователей
- Средний возраст
- Самый младший
- Самый старший
"""
tk.Button(root, text="Статистика", command=show_stat).pack(fill="x", padx=10, pady=5)

# ===== Таблица =====
table = ttk.Treeview(root, columns=("id", "name", "age"), show="headings")
table.heading("id", text="ID")
table.heading("name", text="Имя")
"""Сортировка по клику по колонке: если нажали на заголовок "Возраст", то сортируем по возрасту."""
table.heading("age", text="Возраст", command=lambda: sort(table, "age", False))
table.pack(fill="both", expand=True, padx=10, pady=10)


# ===== Загрузка данных при старте =====
refresh_table()


# ===== Запуск окна =====
root.mainloop()
