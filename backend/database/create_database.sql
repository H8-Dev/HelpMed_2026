create database helpmed;
use helpmed;

create table pacientes(
CPF varchar(14) primary key not null,
senha varchar(50) not null,
nome varchar(50) not null,
sobrenome varchar(80) not null,
email varchar(120) not null unique,
data_create timestamp default current_timestamp not null
) engine = InnoDB;

create table medicos(
CRM varchar(15) primary key not null,
CPF varchar(14) not null,
senha varchar(50) not null,
nome varchar(50) not null,
sobrenome varchar(80) not null,
email varchar(120) not null unique,
data_create timestamp default current_timestamp not null
) engine = InnoDB;

create table chat(
chat_id int primary key not null,
url varchar(2083) not null,
last_update timestamp default current_timestamp not null
) engine = InnoDB;

create table arquivos(
arq_id int primary key not null,
type varchar(20) not null,
url varchar(2083) not null,
last_update timestamp default current_timestamp not null
) engine = InnoDB;

create table pagamentos(
pag_id int primary key not null,
total decimal(10,2) not null,
data_hora timestamp default current_timestamp not null
) engine = InnoDB;