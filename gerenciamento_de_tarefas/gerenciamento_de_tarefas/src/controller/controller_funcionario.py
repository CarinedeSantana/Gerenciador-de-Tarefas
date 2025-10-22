from model.funcionario import Funcionario
from model.setor import Setor
from controller.controller_setor import Controller_Setor # Dependência para validação
from conexion.oracle_queries import OracleQueries

class Controller_Funcionario:
    def __init__(self):
        self.ctrl_setor = Controller_Setor()
        
    def inserir_funcionario(self) -> Funcionario:
        
        # Cria uma nova conexão com o banco
        oracle = OracleQueries(can_write=True) # Necessário para inserir
        oracle.connect()
        
        # Lista os setores existentes para associar ao funcionário
        self.listar_setores(oracle, need_connect=False) 
        id_setor = int(input("Digite o ID do Setor (Existente): "))
        setor = self.valida_setor(oracle, id_setor)
        if setor == None:
            return None

        # Solicita ao usuario a MATRÍCULA e NOME
        matricula_funcionario = input("Matrícula do Funcionário (Nova): ") # CORREÇÃO: Lida como str
        
        # Verifica se a matrícula já existe (função ajustada para str abaixo)
        if not self.verifica_existencia_funcionario(oracle, matricula_funcionario):
            print(f"A Matrícula {matricula_funcionario} já existe.")
            return None

        nome_funcionario = input("Nome do Funcionário (Novo): ")

        # Insere o registro
        # Matrícula e Nome são strings, precisam de aspas simples no SQL
        oracle.write(f"INSERT INTO LABDATABASE.FUNCIONARIO VALUES ('{matricula_funcionario}', '{nome_funcionario}', {setor.get_id()})")
        
        # Recupera os dados do novo funcionário criado
        df_funcionario = oracle.sqlToDataFrame(f"select MATRICULA, NOME, ID_SETOR from LABDATABASE.FUNCIONARIO where MATRICULA = '{matricula_funcionario}'")
        
        # Cria um novo objeto Funcionario (Setor já foi validado)
        novo_funcionario = Funcionario(df_funcionario.matricula.values[0], df_funcionario.nome.values[0], setor)
        # Exibe os atributos do novo funcionário
        print(novo_funcionario.to_string())
        # Retorna o objeto novo_funcionario
        return novo_funcionario

    def atualizar_funcionario(self) -> Funcionario:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário a matrícula do funcionário a ser alterado
        matricula_funcionario = input("Matrícula do Funcionário que deseja atualizar: ") # CORREÇÃO: Lida como str

        # Verifica se o funcionário existe na base de dados
        if self.verifica_existencia_funcionario(oracle, matricula_funcionario): # CORREÇÃO: Invertida a lógica para verificar a NÃO EXISTÊNCIA
            print(f"A Matrícula {matricula_funcionario} não existe.")
            return None
        
        # Lista os setores existentes para o usuário escolher o novo
        self.listar_setores(oracle)
        id_setor = int(input("Novo ID do Setor (Existente): "))
        setor = self.valida_setor(oracle, id_setor)
        if setor == None:
            return None
        
        # Solicita ao usuario o novo nome
        novo_nome = input("Nome do Funcionário (Novo): ")

        # Atualiza o nome e o setor do funcionário existente
        # Matrícula e Nome são strings, precisam de aspas
        oracle.write(f"UPDATE LABDATABASE.FUNCIONARIO SET NOME = '{novo_nome}', ID_SETOR = {setor.get_id()} WHERE MATRICULA = '{matricula_funcionario}'")
        
        # Recupera os dados do funcionário atualizado
        df_funcionario = oracle.sqlToDataFrame(f"SELECT MATRICULA, NOME, ID_SETOR FROM LABDATABASE.FUNCIONARIO WHERE MATRICULA = '{matricula_funcionario}'")
        
        # Cria um novo objeto Funcionario
        funcionario_atualizado = Funcionario(df_funcionario.matricula.values[0], df_funcionario.nome.values[0], setor)
        # Exibe os atributos do funcionário
        print(funcionario_atualizado.to_string())
        # Retorna o objeto funcionario_atualizado
        return funcionario_atualizado

    def excluir_funcionario(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário a matrícula do funcionário a ser excluído
        matricula_funcionario = input("Matrícula do Funcionário que irá excluir: ") # CORREÇÃO: Lida como str

        # Verifica se o funcionário existe na base de dados
        if self.verifica_existencia_funcionario(oracle, matricula_funcionario): # CORREÇÃO: Invertida a lógica
            print(f"A Matrícula {matricula_funcionario} não existe.")
            return None
            
        # Recupera os dados do funcionário
        df_funcionario = oracle.sqlToDataFrame(f"SELECT MATRICULA, NOME, ID_SETOR FROM LABDATABASE.FUNCIONARIO WHERE MATRICULA = '{matricula_funcionario}'")
        setor = self.valida_setor(oracle, df_funcionario.id_setor.values[0])
        
        # Revome o funcionário da tabela
        oracle.write(f"DELETE FROM LABDATABASE.FUNCIONARIO WHERE MATRICULA = '{matricula_funcionario}'")            
        
        # Cria um novo objeto Funcionario para informar que foi removido
        funcionario_excluido = Funcionario(df_funcionario.matricula.values[0], df_funcionario.nome.values[0], setor)
        # Exibe os atributos do funcionário excluído
        print("Funcionário Removido com Sucesso!")
        print(funcionario_excluido.to_string())

    def verifica_existencia_funcionario(self, oracle:OracleQueries, matricula:str=None) -> bool: # CORREÇÃO: Recebe str
        # Recupera os dados do funcionário transformando em um DataFrame
        # CORREÇÃO: Matrícula precisa de aspas no SQL
        df_funcionario = oracle.sqlToDataFrame(f"SELECT MATRICULA, NOME, ID_SETOR FROM LABDATABASE.FUNCIONARIO WHERE MATRICULA = '{matricula}'")
        return df_funcionario.empty # Retorna True se a Matrícula NÃO existe
    
    def listar_setores(self, oracle:OracleQueries, need_connect:bool=False):
        query = "select ID, NOME from LABDATABASE.SETOR order by NOME"
        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))

    def valida_setor(self, oracle:OracleQueries, id_setor:int=None) -> Setor:
        if self.ctrl_setor.verifica_existencia_setor(oracle, id_setor):
            print(f"O ID do Setor {id_setor} informado não existe na base.")
            return None
        else:
            oracle.connect()
            # Recupera os dados do setor
            df_setor = oracle.sqlToDataFrame(f"select ID, NOME from LABDATABASE.SETOR where ID = {id_setor}")
            # Cria um novo objeto Setor
            setor = Setor(df_setor.id.values[0], df_setor.nome.values[0])
            return setor