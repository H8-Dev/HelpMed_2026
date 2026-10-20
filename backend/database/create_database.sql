drop database helpmed_db;
create database if not exists helpmed_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

use helpmed_db;

create table if not exists pacientes(
cpf varchar(14) primary key not null,
senha varchar(50) not null,
nome varchar(50) not null,
sobrenome varchar(80) not null,
email varchar(120) not null unique,
data_create timestamp default current_timestamp not null,
ativo boolean default true not null
) engine = InnoDB;

create table if not exists  medicos(
crm varchar(9) primary key not null,
cpf varchar(14) not null,
senha varchar(50) not null,
nome varchar(50) not null,
sobrenome varchar(50) not null,
email varchar(120) not null unique,
formacao varchar(100) not null,
data_create timestamp default current_timestamp not null,
ativo boolean default true not null
) engine = InnoDB;

create table if not exists  chat(
chat_id int primary key auto_increment not null,
dados JSON not null,
c_pac_id varchar(14) not null,
c_med_id varchar(9),
constraint c_pac_id
	foreign key (c_pac_id) references pacientes(cpf),
constraint c_med_id
	foreign key (c_med_id) references medicos(crm),
last_update timestamp default current_timestamp not null
) engine = InnoDB;

create table if not exists  arquivos(
arq_id int primary key auto_increment not null,
type varchar(20) not null,
nome_arq varchar(100) not null,
dados LONGBLOB not null,
a_pac_id varchar(14),
a_med_id varchar(9),
constraint a_pac_id
	foreign key (a_pac_id) references pacientes(cpf),
constraint a_med_id
	foreign key (a_med_id) references medicos(crm),
last_update timestamp default current_timestamp not null
) engine = InnoDB;

create table if not exists  pagamentos(
pag_id int primary key auto_increment not null,
total decimal(10,2) not null,
p_pac_id varchar(14) not null,
p_med_id varchar(9) not null,
constraint p_pac_id
	foreign key (p_pac_id) references pacientes(cpf),
constraint p_med_id
	foreign key (p_med_id) references medicos(crm),
data_hora timestamp default current_timestamp not null
) engine = InnoDB;


DROP PROCEDURE IF EXISTS sp_login_medico;
DROP PROCEDURE IF EXISTS sp_login_paciente;
DROP PROCEDURE IF EXISTS sp_buscar_chats;
DROP PROCEDURE IF EXISTS sp_atend_previo;

DELIMITER $
CREATE PROCEDURE sp_login_medico(in param_crm varchar(15), in param_senha varchar(50))
BEGIN
	DECLARE var_senha_check varchar(50);

	SELECT senha INTO var_senha_check
	FROM medicos
	WHERE crm = param_crm;

	IF var_senha_check = param_senha THEN
		SELECT TRUE AS check1;
	ELSE
		SELECT FALSE AS check1;
	END IF;

END $

CREATE PROCEDURE sp_login_paciente(in param_cpf varchar(15), in param_senha varchar(50))
BEGIN
	DECLARE var_senha_check varchar(50);

	SELECT senha INTO var_senha_check
	FROM pacientes
	WHERE cpf = param_cpf;

	IF var_senha_check = param_senha THEN
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
	DECLARE var_check varchar(14);
	DECLARE var_name varchar(50);

    START TRANSACTION;

	SELECT cpf, nome INTO var_check, var_name
	FROM pacientes
	WHERE CAST(REGEXP_REPLACE(cpf, '[^0-9]', '') AS SIGNED) = param_id;

	INSERT INTO chat (dados, c_pac_id) VALUES ( JSON_OBJECT('id', NULL, 'pat_name', var_name, 'doc_name', NULL, 'avatar', 'P', 'avatarClass', '', 'messages', JSON_ARRAY(JSON_OBJECT()) ), var_check);

	IF var_check IS NULL THEN
		ROLLBACK;
	ELSE
		UPDATE CHAT
        SET dados = json_set(dados, '$.id', last_insert_id())
        WHERE chat_id = last_insert_id();
		COMMIT;
	END IF;

END $
DELIMITER ;