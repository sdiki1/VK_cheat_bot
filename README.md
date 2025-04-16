
# Bot TG by cheating likes, reposts, comments
[![Docker](https://img.shields.io/badge/Docker-✓-blue?logo=docker)](https://www.docker.com/)
[![SQLite](https://img.shields.io/badge/SQLite-✓-green?logo=sqlite)](https://sqlite.org)
[![Aiogram](https://img.shields.io/badge/Aiogram-2.25.1-blueviolet)](https://docs.aiogram.dev/)

Бот для автоматизации взаимодействия с постами ВКонтакте через Telegram интерфейс

### Используемые технологии и библиотеки:
- aiogram (2.7 mostly)
- sqlite3
- sqlalchemy (ORM for work with database)


### Функционал:
- Админ-меню с добавлением аккаунтов
- Работа с апи в вк в отдельном контейнере
  - Запуск и выполнение задач в асинхронном режиме

- Юзер-меню
  - Добавление отзывов на пост в ВК
  - Добаление лайков и репостов на пост

- Постхантер
  - Создание заявки
  - Добавление лайков, комментариев, репостов и ключевого слова в комментариях к посту
  - Мониторинг заявок
  - Удаление заявки


### Запуск
1. Создать .env:
```
BOT_NAME=
BOT_TOKEN=7114206945:AAGDcp9-Pqjc3FPfsAFO-A4G7LBefUHvobA
ADMINS=
```
2. Запустить docker-container:
```
docker-compose up --build -d
```


// Made by sdiki1. All rights not reserved.