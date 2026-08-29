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
data_create timestamp default current_timestamp not null
) engine = InnoDB;

create table if not exists  medicos(
crm varchar(9) primary key not null,
cpf varchar(14) not null,
senha varchar(50) not null,
nome varchar(50) not null,
sobrenome varchar(50) not null,
email varchar(120) not null unique,
formacao varchar(100) not null,
data_create timestamp default current_timestamp not null
) engine = InnoDB;

create table if not exists  chat(
chat_id int primary key not null,
url varchar(2083) not null,
last_update timestamp default current_timestamp not null
) engine = InnoDB;

create table if not exists  arquivos(
arq_id int primary key not null,
type varchar(20) not null,
url varchar(2083) not null,
a_pac_id varchar(14) not null,
a_med_id varchar(9) not null,
constraint a_pac_id
	foreign key (a_pac_id) references pacientes(cpf),
constraint a_med_id
	foreign key (a_med_id) references medicos(crm),
last_update timestamp default current_timestamp not null
) engine = InnoDB;

create table if not exists  pagamentos(
pag_id int primary key not null,
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

DELIMITER $
CREATE PROCEDURE sp_login_medico(in param_crm varchar(15), in param_senha varchar(50))
BEGIN
	DECLARE var_senha_check varchar(50);

	select senha into var_senha_check
	from medicos
	where crm = param_crm;

	if var_senha_check = param_senha then
		SELECT TRUE as check1;
	else
		SELECT FALSE as check1;
	end if;

END $
DELIMITER ;


DROP PROCEDURE IF EXISTS sp_login_paciente;

DELIMITER $
CREATE PROCEDURE sp_login_paciente(in param_cpf varchar(15), in param_senha varchar(50))
BEGIN
	DECLARE var_senha_check varchar(50);

	select senha into var_senha_check
	from pacientes
	where cpf = param_cpf;

	if var_senha_check = param_senha then
		SELECT TRUE as check1;
	else
		SELECT FALSE as check1;
	end if;
	
END $
DELIMITER ;