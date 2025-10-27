## Задача №1. Проверка надёжности пароля
# Напишите функцию `is_password_good(password)`, которая проверяет, 
# является ли пароль надёжным.

## Аргументы функции
# - `password` — строка (пароль), которую нужно проверить.

## Условия надёжного пароля
# Пароль считается надёжным, если выполняются все условия:

# 1. Длина пароля **не менее 8 символов**.
# 2. Пароль содержит **как минимум одну заглавную букву** (A–Z).
# 3. Пароль содержит **как минимум одну строчную букву** (a–z).
# 4. Пароль содержит **как минимум одну цифру** (0–9).

## Возвращаемое значение
# - `True` — если пароль надёжный.
# - `False` — если хотя бы одно из условий не выполняется.

## Примеры использования
# ```python
# print(is_password_good('aabbCC11OP'))  # True
# print(is_password_good('abC1pu'))      # False
# ```

# **Подсказки:**
# 1. Используем `len(password)` для проверки длины пароля.  
# 2. Проверяем наличие заглавных, строчных букв и цифр через методы строк: `isupper()`, `islower()` и `isdigit()`.  
# 3. Пароль надёжный только если все условия одновременно выполнены.

_ENG_ALPHABET_UPPER = 'abcdefghijklmnopqrstuvwxyz'
_ENG_ALPHABET_LOWER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
_NUMS = '0123456789'

# Ищет хотя бы одно совпадение символа word с 
# перечнем list
def is_letter_in_list(word: str, list: str) -> bool:
    for i in word:
        if i in list:
            return True
    else:
        return False

# В подсказке - требование использовать `isupper()`, `islower()` и `isdigit()`.
# Эта проверка избыточна, т.к. проверка принадлежности к алфавиту заглавных
# или строчных букв в функции is_letter_in_list уже её охватывает.
# А не проверять принадлежность к алфавиту нельзя, т.к. есть требование
# о наличии букв в диапазоне (A–Z) и (a–z).
# Цифры можно было бы проверить через isdigit(), но они тоже хорошо вписываются 
# в логику is_letter_in_list, так что рискну отойти от требования.
def is_password_good(password):
    if len(password) < 8:
        return False
    
    if not is_letter_in_list(password, _ENG_ALPHABET_UPPER):
        return False
    
    if not is_letter_in_list(password, _ENG_ALPHABET_LOWER):
        return False
    
    if not is_letter_in_list(password, _NUMS):
        return False
    
    return True


def main():
    print(is_password_good('aabbCC11OP'))  # True
    print(is_password_good('abC1pu'))      # False

if __name__ == "__main__":
	main() 
    

    

    
    
