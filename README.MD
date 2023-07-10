1) Запуск сервера локально на http://127.0.0.1:8080/ `docker-compose up`
2) Проверка `python client.py`. Результаты:
- 200
Пользователь 'Yura' создан
- 500
Пользователь 'Yura' уже существует
- 200
Пользователь 'Nastya' создан
- 200
[{'username': 'Yura', 'password': '$2b$12$uYL36f3C3HDaL4pTtytGsODD9MeluYH0LWDYYq41KR.PpIAhBtp8a', 'email': 'Yura@mail.ru'}, {'username': 'Nastya', 'password': '$2b$12$AFNRxH6xwZANqDcBbih9AeB98l/QrhfrZqalKwKp9QsVyAlQztq.S', 'email': 'Nastya@mail.ru'}]
- 200
Объявление создано
- 200
Объявление создано
- 401
Некорректный логин или пароль
- 200
[{"header": "Car", "description": "Buy a car", "author": "Yura"}, {"header": "House", "description": "Buy a house", "author": "Nastya"}]
- 409
Нельзя удалить чужое объявление
- 404
Объявления не существует
- 200
Объявление удалено
