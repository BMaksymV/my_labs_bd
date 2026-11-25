USE fablab_db;

CREATE TABLE IF NOT EXISTS equipment_notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    equipment_id INT NOT NULL,
    note_text VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS rentals_delete_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rental_id INT NOT NULL,
    user_id INT NOT NULL,
    equipment_id INT NOT NULL,
    checkout_time DATETIME NOT NULL,
    return_time DATETIME,
    deleted_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB;

DROP TRIGGER IF EXISTS trg_equipment_notes_before_insert;
DROP TRIGGER IF EXISTS trg_equipment_notes_before_update;
DROP TRIGGER IF EXISTS trg_equipment_before_delete_notes_integrity;
DROP TRIGGER IF EXISTS trg_equipment_before_update_notes_integrity;
DROP TRIGGER IF EXISTS trg_equipment_no_double_zero_insert;
DROP TRIGGER IF EXISTS trg_equipment_no_double_zero_update;
DROP TRIGGER IF EXISTS trg_equipment_statuses_min_cardinality;
DROP TRIGGER IF EXISTS trg_rentals_after_delete_log;

DROP PROCEDURE IF EXISTS sp_insert_project;
DROP PROCEDURE IF EXISTS sp_add_equipment_to_kit;
DROP PROCEDURE IF EXISTS sp_insert_10_noname_categories;
DROP PROCEDURE IF EXISTS sp_get_session_duration_stats;
DROP PROCEDURE IF EXISTS sp_split_projects_random;
DROP FUNCTION IF EXISTS fn_session_duration_stat;

DELIMITER //

CREATE TRIGGER trg_equipment_notes_before_insert
BEFORE INSERT ON equipment_notes
FOR EACH ROW
BEGIN
    IF NOT EXISTS (SELECT 1 FROM equipment WHERE id = NEW.equipment_id) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Integrity error: equipment_id does not exist in equipment table';
    END IF;
END //

CREATE TRIGGER trg_equipment_notes_before_update
BEFORE UPDATE ON equipment_notes
FOR EACH ROW
BEGIN
    IF NOT EXISTS (SELECT 1 FROM equipment WHERE id = NEW.equipment_id) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Integrity error: equipment_id does not exist in equipment table';
    END IF;
END //

CREATE TRIGGER trg_equipment_before_delete_notes_integrity
BEFORE DELETE ON equipment
FOR EACH ROW
BEGIN
    IF EXISTS (SELECT 1 FROM equipment_notes WHERE equipment_id = OLD.id) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Integrity error: cannot delete equipment because related rows exist in equipment_notes';
    END IF;
END //

CREATE TRIGGER trg_equipment_before_update_notes_integrity
BEFORE UPDATE ON equipment
FOR EACH ROW
BEGIN
    IF OLD.id <> NEW.id AND EXISTS (SELECT 1 FROM equipment_notes WHERE equipment_id = OLD.id) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Integrity error: cannot change equipment id because related rows exist in equipment_notes';
    END IF;
END //

CREATE PROCEDURE sp_insert_project(
    IN p_title VARCHAR(100),
    IN p_description TEXT
)
BEGIN
    IF p_title IS NULL OR TRIM(p_title) = '' THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Validation error: project title cannot be empty';
    END IF;

    INSERT INTO projects (title, description)
    VALUES (TRIM(p_title), p_description);

    SELECT id, title, description
    FROM projects
    WHERE id = LAST_INSERT_ID();
END //

CREATE PROCEDURE sp_add_equipment_to_kit(
    IN p_equipment_name VARCHAR(45),
    IN p_kit_name VARCHAR(45)
)
BEGIN
    DECLARE v_equipment_id INT DEFAULT NULL;
    DECLARE v_kit_id INT DEFAULT NULL;

    IF p_equipment_name IS NULL OR TRIM(p_equipment_name) = '' THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Validation error: equipment_name is required';
    END IF;

    IF p_kit_name IS NULL OR TRIM(p_kit_name) = '' THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Validation error: kit_name is required';
    END IF;

    SELECT id INTO v_equipment_id
    FROM equipment
    WHERE name = p_equipment_name
    LIMIT 1;

    IF v_equipment_id IS NULL THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Not found: equipment with the specified name does not exist';
    END IF;

    SELECT id INTO v_kit_id
    FROM equipment_kits
    WHERE kit_name = p_kit_name
    LIMIT 1;

    IF v_kit_id IS NULL THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Not found: equipment kit with the specified kit_name does not exist';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM kit_items
        WHERE equipment_id = v_equipment_id AND kit_id = v_kit_id
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Duplicate entry: this equipment is already assigned to the specified kit';
    END IF;

    INSERT INTO kit_items (equipment_id, kit_id)
    VALUES (v_equipment_id, v_kit_id);

    SELECT
        v_equipment_id AS equipment_id,
        p_equipment_name AS equipment_name,
        v_kit_id AS kit_id,
        p_kit_name AS kit_name;
END //

CREATE PROCEDURE sp_insert_10_noname_categories(
    IN p_start_num INT
)
BEGIN
    DECLARE v_i INT DEFAULT 0;
    DECLARE v_start INT;
    DECLARE v_first_id INT DEFAULT NULL;

    SET v_start = IFNULL(p_start_num, 1);

    IF v_start < 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Validation error: start_num must be a non-negative integer';
    END IF;

    WHILE v_i < 10 DO
        INSERT INTO equipment_categories (name)
        VALUES (CONCAT('Noname', v_start + v_i));

        IF v_i = 0 THEN
            SET v_first_id = LAST_INSERT_ID();
        END IF;

        SET v_i = v_i + 1;
    END WHILE;

    SELECT id, name
    FROM equipment_categories
    WHERE id >= v_first_id
    ORDER BY id ASC
    LIMIT 10;
END //

CREATE FUNCTION fn_session_duration_stat(p_operation VARCHAR(10))
RETURNS DECIMAL(12, 2)
READS SQL DATA
BEGIN
    DECLARE v_result DECIMAL(12, 2);
    DECLARE v_op VARCHAR(10);

    SET v_op = UPPER(TRIM(IFNULL(p_operation, 'AVG')));

    IF v_op = 'MAX' THEN
        SELECT MAX(duration_minutes) INTO v_result FROM machine_sessions;
    ELSEIF v_op = 'MIN' THEN
        SELECT MIN(duration_minutes) INTO v_result FROM machine_sessions;
    ELSEIF v_op = 'SUM' THEN
        SELECT SUM(duration_minutes) INTO v_result FROM machine_sessions;
    ELSEIF v_op = 'AVG' THEN
        SELECT AVG(duration_minutes) INTO v_result FROM machine_sessions;
    ELSE
        RETURN NULL;
    END IF;

    RETURN v_result;
END //

CREATE PROCEDURE sp_get_session_duration_stats(
    IN p_operation VARCHAR(10)
)
BEGIN
    DECLARE v_op VARCHAR(10);
    SET v_op = UPPER(TRIM(IFNULL(p_operation, 'ALL')));

    IF v_op = 'ALL' THEN
        SELECT
            fn_session_duration_stat('MIN') AS min_duration,
            fn_session_duration_stat('MAX') AS max_duration,
            fn_session_duration_stat('SUM') AS sum_duration,
            fn_session_duration_stat('AVG') AS avg_duration;
    ELSEIF v_op IN ('MIN', 'MAX', 'SUM', 'AVG') THEN
        SELECT
            v_op AS operation,
            fn_session_duration_stat(v_op) AS value;
    ELSE
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Validation error: operation must be one of MIN, MAX, SUM, AVG, ALL';
    END IF;
END //

CREATE PROCEDURE sp_split_projects_random()
BEGIN
    DECLARE v_done INT DEFAULT 0;
    DECLARE v_id INT;
    DECLARE v_title VARCHAR(100);
    DECLARE v_description TEXT;
    DECLARE v_ts VARCHAR(32);
    DECLARE v_table1 VARCHAR(100);
    DECLARE v_table2 VARCHAR(100);
    DECLARE v_count1 INT DEFAULT 0;
    DECLARE v_count2 INT DEFAULT 0;

    DECLARE cur_projects CURSOR FOR
        SELECT id, title, description FROM projects;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_done = 1;

    SET v_ts = DATE_FORMAT(NOW(6), '%Y%m%d_%H%i%s_%f');
    SET v_table1 = CONCAT('projects_split_1_', v_ts);
    SET v_table2 = CONCAT('projects_split_2_', v_ts);

    SET @sql_create1 = CONCAT('CREATE TABLE `', v_table1, '` LIKE projects');
    PREPARE stmt_create1 FROM @sql_create1;
    EXECUTE stmt_create1;
    DEALLOCATE PREPARE stmt_create1;

    SET @sql_create2 = CONCAT('CREATE TABLE `', v_table2, '` LIKE projects');
    PREPARE stmt_create2 FROM @sql_create2;
    EXECUTE stmt_create2;
    DEALLOCATE PREPARE stmt_create2;

    OPEN cur_projects;
    read_loop: LOOP
        FETCH cur_projects INTO v_id, v_title, v_description;
        IF v_done = 1 THEN
            LEAVE read_loop;
        END IF;

        SET @row_id = v_id;
        SET @row_title = v_title;
        SET @row_description = v_description;

        IF RAND() < 0.5 THEN
            SET @sql_ins = CONCAT('INSERT INTO `', v_table1, '` (id, title, description) VALUES (?, ?, ?)');
            SET v_count1 = v_count1 + 1;
        ELSE
            SET @sql_ins = CONCAT('INSERT INTO `', v_table2, '` (id, title, description) VALUES (?, ?, ?)');
            SET v_count2 = v_count2 + 1;
        END IF;

        PREPARE stmt_ins FROM @sql_ins;
        EXECUTE stmt_ins USING @row_id, @row_title, @row_description;
        DEALLOCATE PREPARE stmt_ins;
    END LOOP;
    CLOSE cur_projects;

    SELECT
        v_table1 AS table_1,
        v_count1 AS table_1_rows,
        v_table2 AS table_2,
        v_count2 AS table_2_rows;
END //

CREATE TRIGGER trg_equipment_no_double_zero_insert
BEFORE INSERT ON equipment
FOR EACH ROW
BEGIN
    IF RIGHT(NEW.inventory_number, 2) = '00' THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Trigger violation: inventory_number cannot end with two zeros (00)';
    END IF;
END //

CREATE TRIGGER trg_equipment_no_double_zero_update
BEFORE UPDATE ON equipment
FOR EACH ROW
BEGIN
    IF RIGHT(NEW.inventory_number, 2) = '00' THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Trigger violation: inventory_number cannot end with two zeros (00)';
    END IF;
END //

CREATE TRIGGER trg_equipment_statuses_min_cardinality
BEFORE DELETE ON equipment_statuses
FOR EACH ROW
BEGIN
    DECLARE v_row_count INT;
    SELECT COUNT(*) INTO v_row_count FROM equipment_statuses;
    IF v_row_count <= 6 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Trigger violation: equipment_statuses must maintain a minimum cardinality of 6 rows';
    END IF;
END //

CREATE TRIGGER trg_rentals_after_delete_log
AFTER DELETE ON rentals
FOR EACH ROW
BEGIN
    INSERT INTO rentals_delete_log (
        rental_id,
        user_id,
        equipment_id,
        checkout_time,
        return_time,
        deleted_at
    ) VALUES (
        OLD.id,
        OLD.user_id,
        OLD.equipment_id,
        OLD.checkout_time,
        OLD.return_time,
        NOW()
    );
END //

DELIMITER ;
