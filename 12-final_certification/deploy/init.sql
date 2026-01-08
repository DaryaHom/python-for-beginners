CREATE DATABASE subscriptions;

CREATE TYPE subscription_category AS ENUM (
    'Музыка', 
    'Видео и стриминг', 
    'Подкасты',
    'Игры',
    'Облачное хранилище',
    'Хостинг и домены',
    'Программное обеспечение',
    'Образование',
    'СМИ',
    'Фитнес и здоровье',
    'Косметика и салоны красоты',
    'Шоппинг и доставка',
    'Транспорт и такси',
    'Благотворительность',
    'Финансы и инвестиции',
    'Телеком, связь и общение',
    'Продуктивность',
    'Путешествия',
    'Еда и доставка',
    'Уход за животными',
    'Это другоэ'
);

CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    title text NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL, 
    category subscription_category NOT NULL,
    price NUMERIC NOT NULL,
    price_daily NUMERIC NOT NULL,
    descr text NULL,
    creation_date TIMESTAMP DEFAULT now(),
    CONSTRAINT unique_username_title_start UNIQUE(username, title, start_date)
);
