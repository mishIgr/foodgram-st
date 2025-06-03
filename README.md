## Клонирование проекта

Клонируйте репозиторий на вашу локальную машину:

```sh
git clone https://github.com/mishIgr/foodgram-st
````

После выполнения этой команды появится директория `foodgram-st`, содержащая весь проект.

---

## Запуск проекта

Создайте файл `.env` на основе примера:

```sh
cp .env.example .env
```

Пример содержимого `.env`:

```env
DB_NAME=posgresql
DB_PASSWORD=posgresql
DB_USER=posgresql

DB_HOST=db
DB_PORT=5432

DJANGO_SECRET_KEY='django-insecure-9m10r-@y+mdz+rnnxjeuj+o#t3@5$-w*m&4ew@x5(1)czfq2k('
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS='localhost;127.0.0.1'
```

Запустите контейнеры:

```sh
docker compose up -d --build
```

Вы должны увидеть запуск всех необходимых сервисов. Проверить их можно с помощью команды:

```sh
docker ps
```

---

## Доступ к приложению

Приложение будет доступно по адресу:

**[http://localhost](http://localhost)**

---

## Демо-аккаунты

### Администратор

* **Email**: `admin@example.com`
* **Пароль**: `admin`

### Обычные пользователи

| Email                                                 | Пароль           |
| ----------------------------------------------------- | ---------------- |
| [vivanov@yandex.ru](mailto:vivanov@yandex.ru)         | MySecretPas$word |
| [second_user@email.org](mailto:second_user@email.org) | MySecretPas$word |
| [third-user@user.ru](mailto:nikitos@gmail.com)        | MySecretPas$word |


указанные пароли верны только с `DJANGO_SECRET_KEY` указанном в примере `.env.example` 

---

##  Документация

Документация к api доступна по ссылке:

```sh
docker compose down -v
```

---

##  Остановка проекта

Чтобы остановить и удалить все контейнеры и тома, выполните:

**[http://localhost/api/docs](http://localhost/api/docs)**

---

## Стек технологий

* Python / Django / Django REST Framework
* PostgreSQL
* Docker / Docker Compose
* Gunicorn / Nginx
* React
