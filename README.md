# Foodgram «Продуктовый помощник»
![example workflow](https://github.com/Tar8117/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

«Foodgram» - это очень удобный и полезный сервис, где пользователи могут публиковать разные рецепты, подписываться на публикации других польователей и добавлять понравившиеся рецепты в избранное.
Самой главной особенностью Foodgram является возможность добавлять рецепты в «Список покупок» и скачать список продуктов для нужного рецепта в формате PDF .
Foodgram включает в себя онлайн-сервис и API для него.

## Стек:
- PostgreSQL
- Nginx
- Python
- Django
- Git
- Docker
- И так далее (более подробно можно ознакомиться здесь `foodgram-project-react/requirements.txt`)

## Руководство по запуску проекта:
Склонировать репозиторий:

```bash
https://github.com/Tar8117/foodgram-project-react.git
```

Либо, если используете доступ к Github через SSH:
```bash
git@github.com:Tar8117/foodgram-project-react.git
```

На сервере проекта установить `doker` и `docker-compose`:
```bash 
sudo apt install docker.io 
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Скопировать содержимое из файлов `infra/docker-compose.yaml` и `infra/nginx.conf` на сервер в `home/<ваш_username>/docker-compose.yaml` и `home/<ваш_username>/nginx/default.conf` соответственно.
Не забудьте на вашем сервере предварительно создать файлы `docker-compose.yaml` и `nginx/default.conf` с помощью команды `touch`.
Также создайте файл `.env` со своими переменными окружения в `home/<ваш_username>/.env`

Пример заполнения `.env`:
```bash 
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
DB_HOST=db
DB_PORT=5432
```
Запуск `docker-compose`:
```bash
docker-compose up -d --build
docker-compose exec backend python manage.py makemigrations --noinput
docker-compose exec backend python manage.py migrate --noinput
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic --no-input 
```
---


Доступно по адресу  178.154.198.108


Автор:
github.com/Tar8117
---
