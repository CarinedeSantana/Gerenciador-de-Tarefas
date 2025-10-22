from conexion.oracle_queries import OracleQueries

class Relatorio:
    def __init__(self):
        # Associa a query de Relatório de Setores
        with open("sql/relatorio_setores.sql") as f:
            self.query_relatorio_setores = f.read()

        # Associa a query de Relatório de Funcionários
        with open("sql/relatorio_funcionarios.sql") as f:
            self.query_relatorio_funcionarios = f.read()

        # Associa a query de Relatório de Todas as Tarefas
        with open("sql/relatorio_todas_tarefas.sql") as f:
            self.query_relatorio_tarefas = f.read()

        # Associa a query de Relatório de Tarefas por Funcionário
        with open("sql/relatorio_tarefas_por_funcionario.sql") as f:
            self.query_relatorio_tarefas_por_funcionario = f.read()


    def get_relatorio_setores(self):
        # Cria uma nova conexão com o banco
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        print("\n=======================================================")
        print("              RELATÓRIO DE SETORES")
        print("=======================================================")
        print(oracle.sqlToDataFrame(self.query_relatorio_setores))
        input("Pressione Enter para Sair do Relatório de Setores")

    def get_relatorio_funcionarios(self):
        # Cria uma nova conexão com o banco
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        print("\n=======================================================")
        print("            RELATÓRIO DE FUNCIONÁRIOS")
        print("=======================================================")
        print(oracle.sqlToDataFrame(self.query_relatorio_funcionarios))
        input("Pressione Enter para Sair do Relatório de Funcionários")

    def get_relatorio_tarefas(self):
        # Cria uma nova conexão com o banco
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        print("\n=======================================================")
        print("           RELATÓRIO DE TODAS AS TAREFAS")
        print("=======================================================")
        print(oracle.sqlToDataFrame(self.query_relatorio_tarefas))
        input("Pressione Enter para Sair do Relatório de Tarefas")

    def get_relatorio_tarefas_por_funcionario(self):
        # Cria uma nova conexão com o banco
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        print("\n=======================================================")
        print("      RELATÓRIO DE TAREFAS POR FUNCIONÁRIO")
        print("=======================================================")
        print(oracle.sqlToDataFrame(self.query_relatorio_tarefas_por_funcionario))
        input("Pressione Enter para Sair do Relatório de Tarefas por Funcionário")