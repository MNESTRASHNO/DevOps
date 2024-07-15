-- Создание таблицы "phone"
CREATE TABLE IF NOT EXISTS phone (
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR(20)
);

-- Вставка данных в таблицу "phone"
INSERT INTO phone (phone_number) VALUES ('81234567890');

-- Создание таблицы email"
CREATE TABLE IF NOT EXISTS email (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100)
);

INSERT INTO mail (email) VALUES ('test1@example.com');

CREATE USER repl_user REPLICATION LOGIN PASSWORD '12345';


