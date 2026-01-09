Установка и использование
=========================

1. Клонируйте репозиторий:

.. code-block:: bash

   git clone https://github.com/DaryaHom/python-for-beginners.git
   cd 12-final_certification

2. Создайте виртуальное окружение:

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate

3. Установите зависимости:

.. code-block:: bash

   pip install -r requirements.txt

4. Запустить PostgreSQL.
.. code-block:: bash

   cd deploy
   make up-db

5. Накатить миграцию БД.
.. code-block:: bash

   make up-db

6. Запустить приложение из директории проекта.
.. code-block:: bash

   cd ..
   python main.py

6. Открыть в браузере. Адрес по умолчанию - http://127.0.0.1:8081
