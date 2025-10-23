# Gerenciamento de Tarefas (CRUD Oracle + Python)

Este projeto implementa um sistema básico de Gerenciamento de Tarefas utilizando o **Python** para a camada de aplicação e o **Oracle Database (XE)** para persistência de dados. O sistema permite realizar operações CRUD (Create, Read, Update, Delete) nas entidades principais: Setores, Funcionários e Tarefas.

---

## Tecnologias Utilizadas

| Componente | Tecnologia/Padrão |
| :--- | :--- |
| **Banco de Dados** | Oracle Database (Schema `LABDATABASE`) |
| **Linguagem** | Python 3.x |
| **Driver de Conexão** | `cx-Oracle` (ou `oracledb`) |
| **Manipulação de Dados** | `pandas` (para exibição em *DataFrames*) |
| **Padrão de Código** | Orientação a Objetos (Pacotes `model`, `controller`) |

---

## Entidades do Modelo de Dados

O projeto gerencia três entidades principais, baseadas no Diagrama Entidade-Relacionamento fornecido:

| Tabela | Chave Primária | Tipo de Dados da PK/FK | Relacionamentos |
| :--- | :--- | :--- | :--- |
| **SETOR** | ID (NUMBER) | NUMBER | - |
| **FUNCIONARIO** | MATRICULA (VARCHAR2) | VARCHAR2 | FK para **SETOR** |
| **TAREFA** | ID (NUMBER) | NUMBER | FK para **FUNCIONARIO** |

---

## Estrutura do Projeto

A estrutura segue o padrão de pacotes Python para modularização:# Gerenciamento-de-Tarefas
gerenciamento_de_tarefas/ ├── conexion/ # Lógica de conexão com o Oracle e credenciais. ├── controller/ # Lógica de negócio (CRUD) para as entidades. ├── model/ # Classes Python (Objetos de Negócio): Setor, Funcionario, Tarefa. ├── reports/ # Módulo para execução de relatórios SQL. ├── sql/ # Arquivos SQL: DDL, DML e consultas de relatórios. ├── utils/ # Funções de utilidade e configuração (Menus, Contagem de registros). ├── create_tables_and_records.py # Script de inicialização do banco. ├── principal.py # Menu principal da aplicação. └── requirements.txt # Lista de dependências Python.
---

## Como Executar o Projeto

Siga os passos abaixo para configurar e rodar a aplicação.

### 1. Instalação de Dependências

Navegue até o diretório raiz do projeto no terminal e instale as bibliotecas Python necessárias:
pip install -r requirements.txt

2. Inicialização do Banco de Dados (DDL e DML)
Este script apaga, recria todas as tabelas e sequences e insere os dados de amostra:
python create_tables_and_records.py

3. Execução da Aplicação
Após a inicialização do banco, inicie o menu principal:
python principal.py
