# frog_cafe

## Запуск БД
- На компьютере заходишь в терминал по папке проекта
- В терминале docker compose up -d
- В DBeaver создаешь новое соединение Postgre с параметрами из env
- В SQL редакторе запускаешь скрипт из sql_code/InitDB.sql

## API
Menu:
GET /api/menu - получение списка блюд
POST /api/menu - создание нового блюда
GET /api/menu/{id} - получение записи блюда
PUT /api/menu/{id} - редактирование записи блюда
DELETE /api/menu/{id} - удаление записи блюда

Users:
GET /api/users - получение списка пользователей
POST /api/users - создание новой записи пользователя
GET /api/users/{id} - получение записи пользователя
PUT /api/users/{id} - редактирование записи пользователя
DELETE /api/users/{id} - удаление записи пользователя

Roles:
GET /api/roles - получение списка ролей
POST /api/roles - создание роли
GET /api/roles/{id} - получение роли
PUT /api/roles/{id} - редактирование роли
DELETE /api/roles/{id} - удаление роли

Order_statuses:
GET /api/order_statuses - получение списка статусов заказов
POST /api/order_statuses - создание нового статуса
GET /api/order_statuses/{id} - получение статуса
PUT /api/order_statuses/{id} - редактирование статуса
DELETE /api/order_statuses/{id} - удаление статуса

Toads:
GET /api/toads - получение списка жабок
POST /api/toads - создание жабки
GET /api/toads/{id} - получение жабки
PUT /api/toads/{id} - редактирование жабки
DELETE /api/toads/{id} - удаление жабки

Orders:
GET /api/orders - получение списка заказов
POST /api/orders - создание заказа
GET /api/orders/{id} - получение данных заказа

Cart: 
GET /api/cart/{order_id} - получение списка блюд в заказе

------------------------------------------------------------------------------------------
POST /api/orders:
При создании заказа с фронта должен передаваться список выбранных блюд на указанный эндпоинт. При поступлении POST запроса в таблице Orders создается запись заказа, в таблицу Cart записываются заказанные блюда с привязкой к id заказа

GET /api/cart/{order_id}:
В запросе обязательно должен передаваться ИД заказа для фильтрации. В ответе должны передаваться только записи с ИД указанного заказа в поле Order_id