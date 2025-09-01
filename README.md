# Fast-Canada

Fast-Canada — это backend-платформа для интернет-магазина, написанная с использованием Django, DRF и PostgreSQL. Проект использует Docker для удобного развертывания и настройки окружения.

## 📦 Установка

### 📰 Клонирование проекта

```bash
git clone https://github.com/sashapenkin12/Fast-Canada
cd Fast-Canada
```
### 🧪 Установка зависимостей

```bash
pip install -r requirements.txt
```
## 🏃‍♂️ Запуск

### 🔧 Переменные окружения
1. Создайте файл .env
2. Скопируйте в него содержимое из env.example
3. (Опционально) Заполните SMTP-параметры для работы почты
### 🗃 Создание миграций

```bash
python manage.py makemigrations
```
---

### 🐳 Сборка и запуск с Docker

#### Убедитесь, что Docker установлен. Если нет — скачайте [отсюда](https://www.docker.com/products/docker-desktop/)

```bash
docker compose up --build
```

### 🔎 Использование

+ **API-интерфейс**: http://localhost/api/

+ **Админ-панель**: http://localhost/admin/

+ **Медиафайлы**: http://localhost/media/

## 🧪 Тестирование
### 📂 Загрузка данных

В проекте есть готовая фикстура с тестовыми продуктами:
```bash
docker compose exec web python manage.py loaddata tests/test-fixture.json
```
### 🛠 Доступ в админку

+ Логин: admin
+ Пароль: admin

### 🧪 Тестирование API

1. Установите [Postman](https://www.postman.com/downloads/)
2. Импортируйте коллекцию Fast-Canada.postman_collection.json (она есть в корне проекта)
3. Запустите запросы — все нужные входные данные уже подготовлены

### ⚙️ Используемые технологии

#### Backend

- ⚡ Django — основной фреймворк
- 🔍 Django REST Framework — API
- 💾 PostgreSQL — реляционная база данных
- 🧮 Django ORM — ORM для работы с БД
- 🐳 Docker / Docker Compose — контейнеризация

## 🛠 Возможные проблемы
| Проблема                  | Решение                                                                      |
| ------------------------- | ---------------------------------------------------------------------------- |
| ❌ Нет подключения к БД    | Убедитесь, что контейнеры `web` и `db` запущены                              |
| ❌ Нет статики             | Выполните `docker compose exec web python manage.py collectstatic --noinput` |
| ❌ Postman не видит сервер | Проверьте доступность `http://localhost`, отключите VPN/антивирус            |
