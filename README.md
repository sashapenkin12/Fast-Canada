<h1 align="center">Fast-Canada</h1>

## 📦 Установка

### 📰 Скопируйте проект

```
git clone https://github.com/sashapenkin12/Fast-Canada
```

## 🏃‍♂️ Запуск

### 💻 Объявите переменные окружения

#### 📝 Создайте файл .env

#### 📄 Скопируйте в него env.exemle

#### Заполните своими значениями (необязательно)

### Создайте миграции для базы данных

```bash
python manage.py makemigrations
```

### Скачайте Docker. (если не установлен)

#### Сделать это можно [здесь](https://www.docker.com/products/docker-desktop/)

### Затем:

```bash
docker compose up --build
```

### 🔴Использование

После запуска перейдите на:

http://localhost/api — API-интерфейс

http://localhost/admin — Admin-панель

http://localhost/media/ - Отдача всех медиафайлов из папки media


### 💻 Используемые технологии

#### Backend (Django)

- ⚡ Django — основной фреймворк

- 💾 PostgreSQL — реляционная база данных

- 🔍 DRF serializers — валидация входных данных и сериализация данных ответа

- 🧮 Django ORM — ORM для работы с БД

- ✅ Pytest — для тестирования

- 🐳 Docker — контейнеризация и изоляция

#### - 🐋Docker Compose: для разработки и производства.
