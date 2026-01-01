"""
Дополнительные задачи.
Вам нужно написать программу, которая реализует конвейер.

1. Компоненты
Вы должны создать три асинхронные функции (корутины):

- generate_data(output_queue, items_count) (Генератор)
Принимает на вход очередь output_queue для отправки данных 
и количество items_count элементов для генерации.
В цикле от 1 до items_count создает "сырые данные". 
Данные — это словарь, например: {'id': i, 'status': 'raw'}.
Перед тем как положить данные в очередь, имитирует задержку поступления 
с помощью await asyncio.sleep(random.uniform(0, 0.5)).
Выводит сообщение о том, какой элемент был сгенерирован, например: 
    [ГЕНЕРАТОР] Сгенерированы данные: {'id': 1, ...}.
Асинхронно кладет созданный словарь в output_queue.

- process_data(worker_id, input_queue, output_queue) (Обработчик)
Принимает номер воркера worker_id и две очереди: input_queue 
для получения данных и output_queue для отправки результата.
В бесконечном цикле (while True) асинхронно пытается забрать данные из input_queue.
Имитирует долгую I/O-операцию обработки с помощью await asyncio.sleep(random.uniform(0.1, 1.0)).
"Обрабатывает" данные: меняет в словаре статус с 'raw' на 'processed'.
Выводит сообщение о том, какой воркер какие данные обработал, например: 
    [ВОРКЕР {id}] Обработаны данные: {'id': 1, 'status': 'processed'}.
Асинхронно кладет обработанный словарь в output_queue.

- aggregate_results(input_queue, items_count) (Агрегатор)
Принимает на вход очередь input_queue и общее количество 
items_count элементов, которые нужно получить.
В цикле for _ in range(items_count) асинхронно забирает данные из input_queue.
Выводит сообщение о том, что данные сагрегированы, например: 
    [АГРЕГАТОР] Получен результат: {'id': 1, ...}.

2. Технические требования
Использование asyncio.Queue: 
Для передачи данных между корутинами необходимо использовать два экземпляра asyncio.Queue.

Конкурентность: 
Должно быть запущено три задачи-обработчика (process_data), работающих конкурентно.

Управление задачами: 
Главная корутина main должна правильно создавать и запускать все компоненты конвейера.

Корректное завершение: 
Программа должна завершаться автоматически после того, 
как Агрегатор получит все items_count обработанных элементов. 
Зависшие задачи-воркеры должны быть отменены.
"""

import asyncio, random

MAX_PROCS = 3

async def generate_data(
    output_queue: asyncio.Queue,
    items_count: int,
):
    for i in range(1, items_count+1):
        data = {'id': i, 'status': 'raw'}
        await asyncio.sleep(random.uniform(0, 0.5))
        print(f'[ГЕНЕРАТОР] Сгенерированы данные: {data}.')
        await output_queue.put(data)

# Рука не поднялась завершать воркеры через cancel
# https://docs.python.org/3/library/asyncio-queue.html#examples
# Имхо, завершение работы через shutdown очередей выигрывает, т.к.:
# - выглядит лаконичнее;
# - не требует грубого прерывания работы функций из main.
    output_queue.shutdown()
    

async def process_data(
    worker_id: int, 
    input_queue: asyncio.Queue, 
    output_queue: asyncio.Queue,
):
    while True:
        try:
            data = await input_queue.get()
        except asyncio.QueueShutDown:
            print(f'[ВОРКЕР {worker_id}] Завершение работы.')
            break

        await asyncio.sleep(random.uniform(0.1, 1.0))
        data['status'] = 'processed'
        print(f'[ВОРКЕР {worker_id}] Обработаны данные: {data}.')
        await output_queue.put(data)

async def aggregate_results(
    input_queue: asyncio.Queue, 
    items_count: int,
):
    for _ in range(items_count):
        data = await input_queue.get()
        print(f'[АГРЕГАТОР] Получен результат: {data}.')  


async def main():
    queue_1 = asyncio.Queue()
    queue_2 = asyncio.Queue()

    items_count = 10

    tasks = []
    tasks.append(asyncio.create_task(generate_data(queue_1, items_count)))
    tasks.append(asyncio.create_task(aggregate_results(queue_2, items_count)))
    for i in range(MAX_PROCS):
        task = asyncio.create_task(process_data(i+1, queue_1, queue_2))
        tasks.append(task)

    await asyncio.gather(*tasks, return_exceptions=True)


asyncio.run(main())
