from conexion.oracle_queries import OracleQueries
from utils import config

class SplashScreen:

    def __init__(self):
        # Consultas de contagem de registros - inicio
        self.qry_total_setores = config.QUERY_COUNT.format(tabela="SETOR")
        self.qry_total_funcionarios = config.QUERY_COUNT.format(tabela="FUNCIONARIO")
        self.qry_total_tarefas = config.QUERY_COUNT.format(tabela="TAREFA")
        # Consultas de contagem de registros - fim

        # Nome(s) do(s) criador(es)
        self.created_by = "Seu Nome Aqui" # Substitua com o seu nome
        self.professor = "Prof. M.Sc. Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2024/1" # Atualize o semestre

    def get_total_setores(self):
        # Cria uma nova conexão com o banco
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros
        return oracle.sqlToDataFrame(self.qry_total_setores)["total_setor"].values[0]

    def get_total_funcionarios(self):
        # Cria uma nova conexão com o banco
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros
        return oracle.sqlToDataFrame(self.qry_total_funcionarios)["total_funcionario"].values[0]

    def get_total_tarefas(self):
        # Cria uma nova conexão com o banco
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros
        return oracle.sqlToDataFrame(self.qry_total_tarefas)["total_tarefa"].values[0]

    def get_updated_screen(self):
        return f"""
        ########################################################
        #             SISTEMA DE GESTÃO DE TAREFAS              
        #                                                         
        #  TOTAL DE REGISTROS:                                    
        #      1 - SETORES:          {str(self.get_total_setores()).rjust(5)}
        #      2 - FUNCIONÁRIOS:     {str(self.get_total_funcionarios()).rjust(5)}
        #      3 - TAREFAS:          {str(self.get_total_tarefas()).rjust(5)}
        #
        #
        #  CRIADO POR: {self.created_by}
        #
        #  PROFESSOR:  {self.professor}
        #
        #  DISCIPLINA: {self.disciplina}
        #              {self.semestre}
        ########################################################
        """