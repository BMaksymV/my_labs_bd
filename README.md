# FabLab REST API + Stored Programs in MySQL

Бекенд на **Python (Flask + SQLAlchemy + Marshmallow + PyMySQL)** для бази даних `fablab_db` із повноцінним CRUD для всіх 14 таблиць, кастомними помилками та повним набором збережених програм у MySQL (тригери, процедури, функція, курсор).

## Запуск проєкту

1. Перевірте параметри підключення до MySQL у `config/app.yml`.
2. Ініціалізуйте базу даних і встановіть усі тригери, функції та збережені процедури:
   ```bash
   python init_db.py
   ```
   *(або послідовно виконайте `data.sql` та `stored_programs.sql` у MySQL Workbench)*
3. Запустіть Flask-сервер:
   ```bash
   python app.py
   ```
4. Перевірте список доступних ендпоінтів: `GET http://127.0.0.1:5000/api`

---

## Реалізовані завдання «Stored programs in MySQL» (`stored_programs.sql`)

### 1. Додаткова таблиця `equipment_notes` (1:M з `equipment`, цілісність через тригери без FK)
Таблиця `equipment_notes` не має фізичного `FOREIGN KEY`. Цілісність забезпечують 4 тригери:
- `trg_equipment_notes_before_insert` — забороняє вставку нотатки з неіснуючим `equipment_id`.
- `trg_equipment_notes_before_update` — забороняє оновлення `equipment_id` на неіснуюче значення.
- `trg_equipment_before_delete_notes_integrity` — забороняє видалення обладнання, якщо до нього прив’язані нотатки.
- `trg_equipment_before_update_notes_integrity` — забороняє зміну `equipment.id`, якщо існують пов’язані нотатки.

### 2. Збережені процедури, функція та курсор (виклик через контролери бекенду)
| Завдання | Об’єкт MySQL | Ендпоінт Flask | Приклад тіла / параметрів |
| :--- | :--- | :--- | :--- |
| **2a** | `sp_insert_project` | `POST /api/procedures/projects` | `{"title": "Новий проєкт", "description": "Опис"}` |
| **2b** | `sp_add_equipment_to_kit` | `POST /api/procedures/kit-items/by-name` | `{"equipment_name": "Prusa i3 MK3", "kit_name": "Набір для пайки"}` |
| **2c** | `sp_insert_10_noname_categories` | `POST /api/procedures/categories/noname-batch` | `{"start_num": 5}` *(вставить `Noname5`..`Noname14`)* |
| **2d** | `fn_session_duration_stat` + `sp_get_session_duration_stats` | `GET /api/procedures/machine-sessions/stats?operation=ALL` | `operation`: `MIN`, `MAX`, `SUM`, `AVG` або `ALL` |
| **2e (i)** | `sp_split_projects_random` (курсор) | `POST /api/procedures/projects/split-random` | Порожнє тіло; створює 2 таблиці з міткою часу і випадково розкидає рядки `projects` |

### 3. Три додаткові тригери для таблиць БД
- **3a (`trg_equipment_no_double_zero_insert` / `_update`)** — забороняє `equipment.inventory_number`, що закінчується на `'00'` (наприклад, `INV-9900`).
- **3d (`trg_equipment_statuses_min_cardinality`)** — забезпечує мінімальну кардинальність `>= 6` рядків у таблиці `equipment_statuses`.
- **3f (`trg_rentals_after_delete_log`)** — при видаленні рядка з `rentals` автоматично записує його дані та мітку часу `deleted_at` у таблицю-журнал `rentals_delete_log`.

---

## CRUD-ендпоінти (Create, Read, Update, Delete) для кожної таблиці

Усі ресурси підтримують `GET /api/<res>`, `GET /api/<res>/<id>`, `POST /api/<res>`, `PUT /api/<res>/<id>`, `DELETE /api/<res>/<id>`:
- `/api/users` *(+ `/rentals`, `/machine-sessions`)*
- `/api/projects` *(+ `/rentals`)*
- `/api/labs` *(+ `/rentals`)*
- `/api/equipment-categories` *(+ `/equipment`)*
- `/api/equipment-statuses` *(+ `/equipment`)*
- `/api/equipment-info`
- `/api/equipment-kits` *(+ `/equipment` — зв’язок M:M)*
- `/api/equipment` *(+ `/kits`, `/notes`, `/repairs`, `/rentals`)*
- `/api/kit-items` *(складений ПК: `/api/kit-items/<equipment_id>/<kit_id>`)*
- `/api/rentals` *(+ `/equipment`)*
- `/api/repairs`
- `/api/machine-sessions`
- `/api/equipment-notes`
- `/api/rentals-delete-log`

---

## Кастомні помилки

Усі помилки повертаються в єдиному JSON-форматі:
```json
{
  "error": {
    "code": "TRIGGER_OR_PROCEDURE_ERROR",
    "message": "Trigger violation: inventory_number cannot end with two zeros (00)",
    "status": 422,
    "details": { "mysql_errno": 1644 }
  }
}
```
Реалізовані класи в `my_project/utils/exceptions.py` та обробники в `my_project/utils/error_handlers.py`:
- `400 BAD_REQUEST` / `VALIDATION_ERROR` — некоректний JSON, відсутні/зайві поля, помилки форматів і бізнес-правил.
- `404 NOT_FOUND` — сутність або маршрут не знайдено.
- `409 CONFLICT` / `DUPLICATE_ENTRY` / `FOREIGN_KEY_CONSTRAINT` — дублювання унікальних полів або порушення зовнішніх ключів.
- `422 TRIGGER_OR_PROCEDURE_ERROR` — спрацювання `SIGNAL SQLSTATE '45000'` (`errno 1644`) із MySQL-тригера або збереженої процедури.
- `500 DATABASE_ERROR` / `INTERNAL_SERVER_ERROR` — непередбачувані помилки БД або сервера.

---

## Автотести

- Модульні тести CRUD і кастомних помилок (без потреби в MySQL):
  ```bash
  python -m unittest tests/test_api.py -v
  ```
- Інтеграційні тести з реальним MySQL (перевіряють усі тригери, процедури, функцію та курсор):
  ```bash
  python -m unittest tests/test_mysql_integration.py -v
  ```
