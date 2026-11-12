CREATE DATABASE IF NOT EXISTS fablab_db;
USE fablab_db;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS kit_items;
DROP TABLE IF EXISTS machine_sessions;
DROP TABLE IF EXISTS repairs;
DROP TABLE IF EXISTS rentals;
DROP TABLE IF EXISTS equipment;
DROP TABLE IF EXISTS equipment_kits;
DROP TABLE IF EXISTS equipment_info;
DROP TABLE IF EXISTS equipment_statuses;
DROP TABLE IF EXISTS equipment_categories;
DROP TABLE IF EXISTS labs;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS users;

SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(45) NOT NULL,
    last_name VARCHAR(45) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(45)
) ENGINE = InnoDB;

CREATE TABLE projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT
) ENGINE = InnoDB;

CREATE TABLE labs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lab_name VARCHAR(45) NOT NULL,
    course_name VARCHAR(100) NOT NULL
) ENGINE = InnoDB;

CREATE TABLE equipment_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(45) NOT NULL
) ENGINE = InnoDB;

CREATE TABLE equipment_statuses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    status_name VARCHAR(45) NOT NULL
) ENGINE = InnoDB;

CREATE TABLE equipment_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    instruction TEXT NOT NULL
) ENGINE = InnoDB;

CREATE TABLE equipment_kits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kit_name VARCHAR(45) NOT NULL,
    description TEXT
) ENGINE = InnoDB;

CREATE TABLE equipment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    inventory_number VARCHAR(45) NOT NULL,
    name VARCHAR(45) NOT NULL,
    status_id INT NOT NULL,
    category_id INT NOT NULL,
    equipment_info_id INT,
    CONSTRAINT fk_equipment_status FOREIGN KEY (status_id) REFERENCES equipment_statuses(id),
    CONSTRAINT fk_equipment_category FOREIGN KEY (category_id) REFERENCES equipment_categories(id),
    CONSTRAINT fk_equipment_info FOREIGN KEY (equipment_info_id) REFERENCES equipment_info(id)
) ENGINE = InnoDB;

CREATE TABLE kit_items (
    equipment_id INT NOT NULL,
    kit_id INT NOT NULL,
    PRIMARY KEY (equipment_id, kit_id),
    CONSTRAINT fk_kit_items_equipment FOREIGN KEY (equipment_id) REFERENCES equipment(id),
    CONSTRAINT fk_kit_items_kit FOREIGN KEY (kit_id) REFERENCES equipment_kits(id)
) ENGINE = InnoDB;

CREATE TABLE rentals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    checkout_time DATETIME NOT NULL,
    return_time DATETIME,
    user_id INT NOT NULL,
    equipment_id INT NOT NULL,
    project_id INT,
    lab_id INT,
    CONSTRAINT fk_rentals_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_rentals_equipment FOREIGN KEY (equipment_id) REFERENCES equipment(id),
    CONSTRAINT fk_rentals_project FOREIGN KEY (project_id) REFERENCES projects(id),
    CONSTRAINT fk_rentals_lab FOREIGN KEY (lab_id) REFERENCES labs(id)
) ENGINE = InnoDB;

CREATE TABLE repairs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    issue_description TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    equipment_id INT NOT NULL,
    CONSTRAINT fk_repairs_equipment FOREIGN KEY (equipment_id) REFERENCES equipment(id)
) ENGINE = InnoDB;

CREATE TABLE machine_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_start DATETIME NOT NULL,
    duration_minutes INT NOT NULL,
    equipment_id INT NOT NULL,
    user_id INT NOT NULL,
    CONSTRAINT fk_sessions_equipment FOREIGN KEY (equipment_id) REFERENCES equipment(id),
    CONSTRAINT fk_sessions_user FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE = InnoDB;

CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE UNIQUE INDEX idx_equipment_inventory ON equipment(inventory_number);
CREATE INDEX idx_rentals_checkout ON rentals(checkout_time);

INSERT INTO users (first_name, last_name, email, phone) VALUES
('Олександр', 'Іванов', 'o.ivanov@mail.com', '+380501112233'),
('Марія', 'Коваленко', 'm.kovalenko@mail.com', '+380671112233'),
('Іван', 'Петренко', 'i.petrenko@mail.com', '+380631112233'),
('Олена', 'Сидоренко', 'o.sydorenko@mail.com', '+380991112233'),
('Дмитро', 'Ткаченко', 'd.tkachenko@mail.com', '+380931112233'),
('Анна', 'Шевченко', 'a.shevchenko@mail.com', '+380502223344'),
('Василь', 'Бойко', 'v.boyko@mail.com', '+380672223344'),
('Наталія', 'Гриценко', 'n.hrytsenko@mail.com', '+380632223344'),
('Сергій', 'Лисенко', 's.lysenko@mail.com', '+380992223344'),
('Юлія', 'Мельник', 'y.melnyk@mail.com', '+380932223344');

INSERT INTO projects (title, description) VALUES
('Роботизована рука', 'Створення маніпулятора для збірки деталей'),
('Метеостанція IoT', 'Збір погодних даних на базі ESP32'),
('Дрон-доставщик', 'Розробка рами та ПЗ для квадрокоптера'),
('Розумний дім', 'Система автоматизації освітлення'),
('Електроскутер', 'Модифікація батарейного блоку'),
('ЧПУ верстат', 'Збірка міні-фрезера для друкованих плат'),
('3D модель корпусу', 'Друк корпусу для медичного приладу'),
('Агро-бот', 'Робот для поливу рослин'),
('Система розпізнавання облич', 'Камера з AI модулем'),
('Лазерний гравер', 'Проект з відновлення старого гравера');

INSERT INTO labs (lab_name, course_name) VALUES
('Лабораторія електроніки', 'Основи IoT'),
('Лабораторія 3D друку', 'Прототипування'),
('Механічна майстерня', 'Основи мехатроніки'),
('Лабораторія ЧПУ', 'Промисловий дизайн'),
('Робототехніка', 'Автономні системи'),
('Зона пайки', 'Мікроелектроніка'),
('Компютерний клас', 'Програмування C++'),
('Слюсарна зона', 'Обробка металів'),
('Лабораторія вимірювань', 'Метрологія'),
('Зона тестування', 'Контроль якості');

INSERT INTO equipment_categories (name) VALUES
('3D Принтери'),
('Паяльне обладнання'),
('Вимірювальні прилади'),
('Мікроконтролери'),
('Електроінструмент'),
('Лазерні верстати'),
('ЧПУ фрезери'),
('Ручний інструмент'),
('Комплектуючі'),
('Витратні матеріали');

INSERT INTO equipment_statuses (status_name) VALUES
('Доступно'),
('В оренді'),
('На ремонті'),
('Списано'),
('Заброньовано'),
('Налаштовується'),
('Загублено'),
('В дорозі'),
('Очікує деталей'),
('Обслуговується');

INSERT INTO equipment_info (instruction) VALUES
('Перед використанням прогріти екструдер до 200 градусів.'),
('Не залишати увімкненим без нагляду. Використовувати витяжку.'),
('Перевіряти калібрування перед кожним вимірюванням.'),
('Живлення строго 5V. Не подавати 12V на плату!'),
('Використовувати захисні окуляри та рукавиці.'),
('Обов’язково вмикати водяне охолодження трубки.'),
('Фіксувати заготовку на столі мінімум 4 затискачами.'),
('Очищати після кожного використання.'),
('Зберігати в сухому місці.'),
('Утилізувати згідно з правилами екологічної безпеки.');

INSERT INTO equipment_kits (kit_name, description) VALUES
('Стартовий набір Arduino', 'Базовий набір для початківців з електроніки'),
('Набір для пайки', 'Паяльник, припій, флюс, пінцети'),
('Набір викруток', 'Прецизійні викрутки для розбирання електроніки'),
('Кіт для дрона', 'Мотори, пропелери, контролер польоту'),
('Набір датчиків IoT', 'Датчики температури, вологості, руху'),
('Механічний набір', 'Шестерні, підшипники, вали'),
('Вимірювальний набір', 'Мультиметр, осцилограф, щупи'),
('Набір інструментів ЧПУ', 'Фрези різних діаметрів'),
('Набір для 3D друку', 'Шпатель, пінцет, клей для столу'),
('Кіт розумного дому', 'Реле, модулі Wi-Fi, датчики відкриття');

INSERT INTO equipment (inventory_number, name, status_id, category_id, equipment_info_id) VALUES
('INV-1001', 'Prusa i3 MK3', 1, 1, 1),
('INV-1002', 'Паяльна станція Hakko', 2, 2, 2),
('INV-1003', 'Мультиметр Fluke', 1, 3, 3),
('INV-1004', 'Arduino Mega', 1, 4, 4),
('INV-1005', 'Дриль Bosch', 3, 5, 5),
('INV-1006', 'Лазер CO2 40W', 1, 6, 6),
('INV-1007', 'Міні-фрезер CNC', 1, 7, 7),
('INV-1008', 'Шуруповерт Makita', 2, 5, 5),
('INV-1009', 'Осцилограф Rigol', 1, 3, 3),
('INV-1010', 'Ender 3 Pro', 4, 1, 1);

INSERT INTO kit_items (equipment_id, kit_id) VALUES
(4, 1),
(2, 2),
(3, 7),
(9, 7),
(5, 8),
(8, 8),
(1, 9),
(10, 9),
(7, 8),
(6, 8);

INSERT INTO rentals (checkout_time, return_time, user_id, equipment_id, project_id, lab_id) VALUES
('2023-10-01 10:00:00', '2023-10-01 14:00:00', 1, 1, 7, 2),
('2023-10-02 11:30:00', NULL, 2, 2, 1, 6),
('2023-10-03 09:00:00', '2023-10-05 18:00:00', 3, 4, 2, 1),
('2023-10-04 12:00:00', '2023-10-04 16:00:00', 4, 6, 10, 4),
('2023-10-05 14:00:00', NULL, 5, 8, 4, 3),
('2023-10-06 10:15:00', '2023-10-06 12:15:00', 6, 3, 5, 9),
('2023-10-07 15:30:00', '2023-10-08 15:30:00', 7, 9, 9, 1),
('2023-10-08 08:45:00', '2023-10-08 17:00:00', 8, 7, 6, 4),
('2023-10-09 11:00:00', '2023-10-10 11:00:00', 9, 1, 3, 2),
('2023-10-10 13:20:00', NULL, 10, 2, 8, 6),
('2023-10-11 09:30:00', NULL, 1, 3, 7, 2); 

INSERT INTO repairs (issue_description, start_date, end_date, equipment_id) VALUES
('Забилося сопло', '2023-09-01', '2023-09-02', 1),
('Перегорів нагрівальний елемент', '2023-09-05', '2023-09-10', 2),
('Заміна батарейки', '2023-09-12', '2023-09-12', 3),
('Замикання на платі', '2023-09-15', '2023-09-18', 4),
('Іскрять щітки двигуна', '2023-09-20', NULL, 5),
('Юстирування дзеркал', '2023-09-22', '2023-09-23', 6),
('Заміна шпинделя', '2023-09-25', '2023-09-28', 7),
('Зламаний патрон', '2023-09-28', '2023-09-30', 8),
('Калібрування щупів', '2023-10-01', '2023-10-01', 9),
('Згоріла материнська плата', '2023-10-02', NULL, 10);

INSERT INTO machine_sessions (session_start, duration_minutes, equipment_id, user_id) VALUES
('2023-10-01 10:00:00', 240, 1, 1),
('2023-10-02 11:30:00', 120, 2, 2),
('2023-10-03 14:00:00', 60, 6, 4),
('2023-10-04 09:15:00', 180, 7, 8),
('2023-10-05 16:00:00', 90, 1, 9),
('2023-10-06 13:00:00', 45, 2, 10),
('2023-10-07 10:30:00', 300, 6, 4),
('2023-10-08 11:00:00', 150, 7, 8),
('2023-10-09 15:45:00', 60, 1, 1),
('2023-10-10 09:30:00', 210, 2, 2);

SELECT * FROM users;
SELECT * FROM projects;
SELECT * FROM labs;
SELECT * FROM equipment_categories;
SELECT * FROM equipment_statuses;
SELECT * FROM equipment_info;
SELECT * FROM equipment_kits;
SELECT * FROM equipment;
SELECT * FROM kit_items;
SELECT * FROM rentals;
SELECT * FROM repairs;
SELECT * FROM machine_sessions;
