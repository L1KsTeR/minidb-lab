# MiniDB — собственная файловая мини-СУБД

## Запуск

```bash
python main.py


Программа создаёт базу данных в папке `mydb/`, выполняет CRUD-операции и показывает результат.

## Архитектура

main.py — точка входа, демонстрация всех операций
├── database.py — MiniDB: управление таблицами, сохранение/загрузка
├── table.py — Table: строки, CRUD-операции в памяти
└── storage.py — файловый формат .mdb


## Реализованные функции

CREATE TABLE
INSERT
SELECT (все записи и с фильтром)
UPDATE
DELETE
PRIMARY KEY, запрет дубликатов
Типы INT, STRING, FLOAT
Файловое хранение (собственный формат)
Сохранность данных при перезапуске

## Формат хранения

Файлы `.mdb` — собственный текстовый формат:
MINIDB|1.0
SCHEMA|id:INT|name:STRING|task:STRING|size:INT|pk:id
DATA|1|dataset_1|classification|1000
DATA|2|dataset_2|classification|2000