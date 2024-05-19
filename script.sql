-- Aqui vai criar um banco de dados se ele não existir
-- SCHEMA e DATABASE são sinônimos
CREATE DATABASE IF NOT EXISTS banco_python; 

-- Aqui vai abrir o banco de dados criado
USE banco_python;

-- Aqui vai deletar o banco de dados se ele existir
DROP DATABASE IF EXISTS banco_naldo;

-- Aqui vai criar a tabela se ela não existir
CREATE TABLE IF NOT EXISTS alunos (
    id INT(7) AUTO_INCREMENT PRIMARY KEY,
    aluno VARCHAR(100) NOT NULL,
    cpf_ra VARCHAR(11) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Aqui vai criar a tabela se ela não existir
CREATE TABLE IF NOT EXISTS pesquisa (
    id INT(7) AUTO_INCREMENT PRIMARY KEY,
    cpf_ra VARCHAR(11) NOT NULL,
    id_aluno INT(7),
    urlChegada VARCHAR(50),
    status_chegada VARCHAR(20),
    time_chegada VARCHAR(30),
    urlSaida VARCHAR(50),
    status_saida VARCHAR(20),
    time_saida VARCHAR(30),
    atividades_gostou VARCHAR(250),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_aluno FOREIGN KEY (id_aluno) REFERENCES alunos (id)
);

-- Removendo uma tabela se ela existir
DROP TABLE IF EXISTS tbl_alunos;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

-- Renomear uma tabela se ela existir
-- ALTER TABLE tbl_alunos RENAME TO alunos;

-- Definição da primeira tabela: users
CREATE TABLE IF NOT EXISTS usuarios (
    id INT(5) AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(100) NOT NULL,
    status VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Definição da segunda tabela: posts
CREATE TABLE IF NOT EXISTS atividades (
    id INT(7) AUTO_INCREMENT PRIMARY KEY,
    atividade VARCHAR(150) NOT NULL,
    data_evento VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserindo dados nas tabelas
-- INSERT INTO alunos (aluno, cpf_ra) VALUES
-- ('Joao Ferreira', '12345678901'),
-- ('Maria Lima', '45678912303'),
-- ('Aline Pereira', '78936914725');

-- INSERT INTO usuarios (nome, cpf, email, senha, status) VALUES
-- ('Administrador do Sistema', '12345678901','adm@email.com', '', 'Ativo'),
-- ('Diretora da Escola', '45678912303', 'diretora@email.com', '', 'Inativo');

INSERT INTO atividades (atividade, data_evento) VALUES
('Seminario IA', '19/05/2024'),
-- ('Semana do Esporte na escola', '21/04/2024'),
-- ('Semana da leitura', '21/04/2024'),
('Torneio de Programacao', '19/05/2024');