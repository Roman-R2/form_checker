# form_checker

## О проекте

Выполненое [тестовое задание](https://docs.google.com/document/d/1fMFwPBs53xzcrltEFOpEG4GWTaQ-5jvVLrNT6_hmC7I/edit?usp=sharing) на вакансию [Junior Python разработчик](https://ufa.hh.ru/vacancy/74409375)

Что интересного в проекте:
1. Docker
2. Django 3.2.16
3. Python 3.10.9
4. Контейнер с MongoDB (данныя БД подключена к джанго с помощью djongo)
5. Сокрытие переменных окружения в .env файле (в данном случае .env расположен в репозитории, но это только в качестве удобства)
6. Используется poetry вместо pip
7. Работа с формами осуществляется наспямую с помощью pymongo
8. Код валидации пришедших форм вынесен в сервисный слой, реализован паттерн "цепочка ответственности"
9. Django команда для создания фейковых форм в БД
10. Тестовый скрипт на основе unittest в django
11. Используется линтер для поддержания кода в соответствии с PEP-8

## Установка

Для запуска прилодения локально необходимы docker и cli утилита make (либо можно без make, посмотрев порядок команд в Makefile)
Также нужно освободить порты 8000 и 8081

Все что нужно сделать - это выполнить команду в папке с Makefile:

```
make first-start
```
данная команда: 
- соберет docker образы, 
- поднимит docker контейнеры (web-app - контейнер с python django, mongo - БД MongoDB, mongo-express - web интерфейс для удобной работы с контейнером MongoDB)
- применит миграции
- создаст суперпользователя на основе переменных из .env
- добавит 10 фейковых форм в БД

Теперь проект доступен локально по адресу [http://localhost:8000/](http://localhost:8000/)

URL для работы с формами [http://localhost:8000/get_form/](http://localhost:8000/get_form/) (только POST запросы)

Также web интерфейс mongo express доступен по адресу [http://localhost:8081](http://localhost:8081)

## Тестирование

Для тестирования нужно выполнить:

```
make test
```

## Дополнительно

Также вы можете посмотреть [мое резюме](https://hh.ru/resume/0851fb64ff097b9c040039ed1f6c4770425865)