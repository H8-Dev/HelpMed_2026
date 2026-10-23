DROP DATABASE helpmed_db;
CREATE DATABASE IF NOT EXISTS helpmed_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

use helpmed_db;

CREATE TABLE IF NOT EXISTS pacientes(
cpf VARCHAR(14) PRIMARY KEY NOT NULL,
senha VARCHAR(50) NOT NULL,
nome VARCHAR(50) NOT NULL,
sobrenome VARCHAR(80) NOT NULL,
email VARCHAR(120) NOT NULL unique,
data_CREATE TIMESTAMP DEFAULT current_timestamp NOT NULL,
ativo BOOLEAN DEFAULT true NOT NULL
) engine = InnoDB;

CREATE TABLE IF NOT EXISTS  medicos(
crm VARCHAR(9) PRIMARY KEY NOT NULL,
cpf VARCHAR(14) NOT NULL,
senha VARCHAR(50) NOT NULL,
nome VARCHAR(50) NOT NULL,
sobrenome VARCHAR(50) NOT NULL,
email VARCHAR(120) NOT NULL unique,
formacao VARCHAR(100) NOT NULL,
data_CREATE TIMESTAMP DEFAULT current_timestamp NOT NULL,
ativo BOOLEAN DEFAULT true NOT NULL
) engine = InnoDB;

CREATE TABLE IF NOT EXISTS  chats(
chat_id int PRIMARY KEY auto_increment NOT NULL,
dados JSON NOT NULL,
c_pac_id VARCHAR(14) NOT NULL,
c_med_id VARCHAR(9),
ativo BOOLEAN DEFAULT true NOT NULL,
constraint c_pac_id
	foreign key (c_pac_id) references pacientes(cpf),
constraint c_med_id
	foreign key (c_med_id) references medicos(crm),
last_update TIMESTAMP DEFAULT current_timestamp NOT NULL
) engine = InnoDB;

CREATE TABLE IF NOT EXISTS  arquivos(
arq_id int PRIMARY KEY auto_increment NOT NULL,
type VARCHAR(20) NOT NULL,
nome_arq VARCHAR(100) NOT NULL,
dados LONGBLOB NOT NULL,
a_pac_id VARCHAR(14),
a_med_id VARCHAR(9),
ativo BOOLEAN DEFAULT true NOT NULL,
constraint a_pac_id
	foreign key (a_pac_id) references pacientes(cpf),
constraint a_med_id
	foreign key (a_med_id) references medicos(crm),
last_update TIMESTAMP DEFAULT current_timestamp NOT NULL
) engine = InnoDB;

CREATE TABLE IF NOT EXISTS  pagamentos(
pag_id int PRIMARY KEY auto_increment NOT NULL,
total decimal(10,2) NOT NULL,
p_pac_id VARCHAR(14) NOT NULL,
p_med_id VARCHAR(9) NOT NULL,
constraint p_pac_id
	foreign key (p_pac_id) references pacientes(cpf),
constraint p_med_id
	foreign key (p_med_id) references medicos(crm),
data_hora TIMESTAMP DEFAULT current_timestamp NOT NULL
) engine = InnoDB;


DROP PROCEDURE IF EXISTS sp_login_medico;
DROP PROCEDURE IF EXISTS sp_login_paciente;
DROP PROCEDURE IF EXISTS sp_buscar_chats;
DROP PROCEDURE IF EXISTS sp_atend_previo;

DELIMITER $
CREATE PROCEDURE sp_login_medico(IN param_crm VARCHAR(15), IN param_senha VARCHAR(50))
BEGIN
	DECLARE var_senha_check VARCHAR(50);

	SELECT senha, ativo INTO var_senha_check, var_ativo_check
	FROM medicos
	WHERE crm = param_crm;

	IF var_senha_check = param_senha AND var_ativo_check = 1 THEN
		SELECT TRUE AS check1;
	ELSE
		SELECT FALSE AS check1;
	END IF;

END $

CREATE PROCEDURE sp_login_paciente(IN param_cpf VARCHAR(15), IN param_senha VARCHAR(50))
BEGIN
	DECLARE var_senha_check VARCHAR(50);
	DECLARE var_ativo_check BOOLEAN

	SELECT senha, ativo INTO var_senha_check, var_ativo_check
	FROM pacientes
	WHERE cpf = param_cpf;

	IF var_senha_check = param_senha AND var_ativo_check = 1 THEN
		SELECT TRUE AS check1;
	ELSE
		SELECT FALSE AS check1;
	END IF;
	
END $

CREATE PROCEDURE sp_buscar_chats(IN param_id BIGINT)
BEGIN
	
	SELECT * FROM chat
	WHERE CAST(REGEXP_REPLACE(c_pac_id, '[^0-9]', '') AS SIGNED) = param_id OR CAST(REGEXP_REPLACE(c_med_id, '[^0-9]', '') AS SIGNED) = param_id;

END $

CREATE PROCEDURE sp_atend_previo(IN param_id BIGINT)
BEGIN
	DECLARE var_check VARCHAR(14);
	DECLARE var_name VARCHAR(50);

    START TRANSACTION;

	SELECT cpf, nome INTO var_check, var_name
	FROM pacientes
	WHERE CAST(REGEXP_REPLACE(cpf, '[^0-9]', '') AS SIGNED) = param_id;

	INSERT INTO chats (dados, c_pac_id) VALUES ( JSON_OBJECT('id', NULL, 'pat_name', var_name, 'doc_name', NULL, 'avatar', 'P', 'avatarClass', '', 'messages', JSON_ARRAY(JSON_OBJECT()) ), var_check);

	IF var_check IS NULL THEN
		ROLLBACK;
	ELSE
		UPDATE chats
        SET dados = json_set(dados, '$.id', last_insert_id())
        WHERE chat_id = last_insert_id();
		COMMIT;
	END IF;

END $
DELIMITER ;