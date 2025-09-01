# Тестирование

## Бытовая химия

### Выполните запуск приложения(описано в README.md)

### Загрузить данные с test-fixture.json:

```bash
docker compose exec web python manage.py loaddata tests/all_data.json
```

### Использование:
+ http://localhost/admin/ (логин: admin, пароль: admin) - админ-панель
+ http://localhost/api/household_chemicals/ - список продуктов бытовой химии
+ http://localhost/api/household_chemicals/<int:pk>/ - детальная информация о продукте

## Корзина и заказы (если нужно, тестируйте без Postman или с другим тестовым клиентом)

### Загрузите Postman. Это можно сделать здесь: https://www.postman.com/downloads/

### Импортируйте коллекцию Fast-Canada.postman_collection.json:

Вам будет предоставлен набор запросов с готовыми входными данными.

