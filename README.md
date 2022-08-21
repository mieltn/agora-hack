# Как запустить проект

Перед работой нжно иметь установленный python. 

Создание виртуального окружения (в корневой папке репозитория):

`python3 -m venv env`

`source env/bin/activate`

Для установки библиотек необходимо выполнить:

`pip install -r requirements.txt --no-dir-cache`

Для работы проекта нужны следующие сервисы:
1. бд маркетплейса - postgres, запускать проще из контейнера postgres
2. маркетплейс - папка marketplace, django
3. бд для промежуточного хранения данных до запроса на микросервисе - mongodb, запускать проще из контейнера mongo
4. микросервис - папка procserv, django
5. скрипт sendtest.py - симулирует отправку xml-пакета на микросервис

### postgres
Необходимо иметь установленный docker

`docker pull postgres`

`docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=secretpassword --name postgres postgres`

Затем создать бд, пароль secretpassword

`psql -h localhost -U postgres`

`CREATE DATABASE marketplace;`

`\q`

### Маркетплейс
Из папки marketplace выполнить

`python3 manage.py runserver`

### mongodb

`docker pull mongo`

`docker run -d -p 27017:27017 --name mongo mongo`

### Микросервис
Из папки procserv выполнить

`python3 manage.py runserver 1234`

### Отправка тестового запроса, симулирующего erp

`python3 sendtest.py`

### Подгрузка данных с микросервиса по запросу маркетплейса

Зайти на localhost:8000 и кнопка get xml
