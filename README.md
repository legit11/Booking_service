##Сервис бронирования


Сервис бронирования — это микросервис для управления бронированием отелей. Он предоставляет API для работы с операциями, такими как управление бронированиями, импорт данных через CSV, а также мониторинг с помощью Grafana и Prometheus. Сервис поддерживает выполнение фоновых задач с использованием Celery и мониторинг задач через Flower.



##Возможности


FastAPI бэкенд с полной функциональностью CRUD для управления бронированиями, отелями и номерами.


Возможность импорта данных через CSV-файлы.


Аутентификация и авторизация с использованием JWT.


Асинхронная обработка с помощью asyncio и FastAPI.


Celery для выполнения фоновых задач.


Flower для мониторинга и управления задачами Celery.


Админка SQLAdmin для удобной работы с Базой Данных


Мониторинг с помощью Grafana и Prometheus.


Контейнеризация с использованием Docker и Docker Compose.


Автоматическое форматирование кода с использованием black и isort.


### Содержание:


- Настройка проекта


- Запуск с Docker


- Тестирование


- Импорт данных


- Фоновые задачи


- Админка


- Мониторинг


- Форматирование кода


## Настройка проекта


Соберите и запустите контейнеры с помощью Docker Compose:


```bash
docker-compose up --build
```


Приложение будет доступно по адресу: `http://localhost:7777`.


## Flower для мониторинга Celery доступен по адресу: `http://localhost:5555`.


## Тестирование


Для запуска тестов используйте pytest


##Импорт данных


Чтобы загрузить данные через CSV, используйте следующий эндпоинт:


`POST /import/{table_name}`


Где {table_name} — это одна из следующих таблиц: hotels, rooms, или bookings.


Пример CSV для импорта:


Копировать код


`id,name,services,date_created
1,Hotel Sunshine,"['wifi', 'breakfast']",2023-09-21
2,Ocean View,"['wifi', 'pool']",2023-09-22`


## Фоновые задачи


Этот проект использует Celery для выполнения фоновых задач, таких как отправка уведомлений или обработка бронирований.


Запустите Celery воркеры с помощью Docker:


```bash
docker-compose up -d celery
```


## Для мониторинга задач используйте Flower, который будет доступен по адресу: `http://localhost:5555`.


Админка SQLAdmin доступна по адресу: `http://localhost:7777/admin`


## Мониторинг


Grafana доступна по адресу: `http://localhost:3000`


Prometheus доступен по адресу: `http://localhost:9090`


Форматирование кода


В проекте используются black и isort для автоматического форматирования кода.


### Проект задеплоен с помощью сервиса render.com.


Проект задеплоем не со всей функциональностью, а только с Redis и PostgreSQL.


Ссылка на работающий проект:


`https://booking-app-890j.onrender.com`
