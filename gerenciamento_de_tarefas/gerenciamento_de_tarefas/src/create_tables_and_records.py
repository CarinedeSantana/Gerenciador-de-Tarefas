from conexion.oracle_queries import OracleQueries

def create_tables(query:str):
    list_of_commands = query.split(";")

    oracle = OracleQueries(can_write=True)
    oracle.connect()

    for command in list_of_commands:    
        if len(command) > 0:
            print(command)
            try:
                oracle.executeDDL(command)
                print("Successfully executed")
            except Exception as e:
                # O tratamento de erro foi alterado aqui para não parar o script em caso de DROP
                print(f"Erro ao executar DDL: {e}") 

def generate_records(query:str, sep:str=';'):
    list_of_commands = query.split(sep)

    oracle = OracleQueries(can_write=True)
    oracle.connect()

    for command in list_of_commands:    
        if len(command) > 0:
            print(command)
            oracle.write(command)
            print("Successfully executed")

def run():

    # 1. Executa o DDL (Criação e remoção de tabelas, sequences e FKs)
    # Arquivo na pasta raiz: ../sql/Apaga os relacionamentos.sql
    with open("../sql/Apaga os relacionamentos.sql") as f:
        query_create = f.read()

    print("Criando/Recriando tabelas (DDL)...")
    create_tables(query=query_create)
    print("Tabelas criadas com sucesso!")

    # 2. Insere os dados de SETOR e FUNCIONARIO
    # Arquivo na pasta raiz: ../sql/INSERE DADOS NA TABELA DE SETOR.sql
    with open("../sql/INSERE DADOS NA TABELA DE SETOR.sql") as f:
        query_generate_setores = f.read()

    print("Gerando registros iniciais (Setores e Funcionários)...")
    # Assume que a função generate_records usa ';' como separador de comandos DML simples
    generate_records(query=query_generate_setores) 
    print("Registros iniciais gerados com sucesso!")

    # 3. Insere os dados de TAREFA (que usam blocos PL/SQL)
    # Arquivo na pasta raiz: ../sql/INSERE DADOS NA TABELA DE TAREFAS.sql
    with open("../sql/INSERE DADOS NA TABELA DE TAREFAS.sql") as f:
        query_generate_tarefas = f.read()

    print("Gerando registros de Tarefas (DML com blocos PL/SQL)...")
    # Usa ' -- ' como separador para os blocos PL/SQL (padrão para o PL/SQL)
    generate_records(query=query_generate_tarefas, sep='--') 
    print("Registros de Tarefas gerados com sucesso!")

if __name__ == '__main__':
    run()