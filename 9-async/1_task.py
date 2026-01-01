"""
Задача 1: "Базовая корутина"
Напишите асинхронную программу, которая выводит на экран одну единственную строку: "Асинхронность - это просто!".
"""

import asyncio, random

# Добавлен счётчик корутин и sleep для визуализации асинхронности:
async def print_async_is_simple(i):
    await asyncio.sleep(random.uniform(1,10))
    print(i, ': ', 'Асинхронность - это просто!')

async def main():
    tasks = [print_async_is_simple(i) for i in range(10)]
    await asyncio.gather(*tasks)

asyncio.run(main())
