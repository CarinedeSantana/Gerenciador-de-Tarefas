from model.tarefa import Tarefa
from model.funcionario import Funcionario
from model.setor import Setor # Adicionado: Import necessário para criar o objeto Setor na validação
from controller.controller_funcionario import Controller_Funcionario # Dependência para validação
from controller.controller_setor import Controller_Setor # Adicionado: Import necessário para validação/busca de Setor
from conexion.oracle_queries import OracleQueries
from datetime import date
from dateutil import parser 

class Controller_Tarefa:
    def __init__(self):
        self.ctrl_funcionario = Controller_Funcionario()
        self.ctrl_setor = Controller_Setor() # Adicionado: Necessário para a função valida_funcionario()
        
    def inserir_tarefa(self) -> Tarefa:
        
        # Cria uma nova conexão com o banco
        oracle = OracleQueries()
        
        # Lista os funcionários existentes para associar à tarefa
        self.listar_funcionarios(oracle, need_connect=True)
        # Matrícula tratada como String (VARCHAR2)
        matricula_funcionario = input("Digite a Matrícula do Funcionário (Responsável): ")
        funcionario = self.valida_funcionario(oracle, matricula_funcionario)
        if funcionario == None:
            return None

        # Solicita a descrição e status
        descricao = input("Descrição da Tarefa: ")
        status = input("Status da Tarefa (Ex: Pendente, Em Andamento, Concluída): ")
        
        # Solicita a data limite (String) e converte para objeto Date
        data_limite_str = input("Data Limite (formato DD/MM/AAAA): ")
        data_limite = parser.parse(data_limite_str, dayfirst=True).date()

        # Recupera o cursor para executar um bloco PL/SQL anônimo
        cursor = oracle.connect()
        # Cria a variável de saída com o tipo especificado
        output_value = cursor.var(int)

        # Cria um dicionário para mapear as variáveis de entrada e saída
        # A Matrícula (String) é passada diretamente
        data = dict(id=output_value, descricao=descricao, data_limite=data_limite, status=status, matricula_func=funcionario.get_matricula())
        # Executa o bloco PL/SQL anônimo para inserção e recuperação da chave primária
        cursor.execute("""
        begin
            :id := LABDATABASE.TAREFA_ID_SEQ.NEXTVAL;
            insert into LABDATABASE.TAREFA (ID, DESCRICAO, DATA_LIMITE, STATUS, ID_FUNCIONARIO) values(:id, :descricao, :data_limite, :status, :matricula_func);
        end;
        """, data)
        # Recupera o ID da nova tarefa
        id_tarefa = output_value.getvalue()
        # Persiste (confirma) as alterações
        oracle.conn.commit()
        
        # Recupera os dados da nova tarefa
        df_tarefa = oracle.sqlToDataFrame(f"select ID, DESCRICAO, DATA_LIMITE, STATUS, ID_FUNCIONARIO from LABDATABASE.TAREFA where ID = {id_tarefa}")
        # Cria um novo objeto Tarefa
        nova_tarefa = Tarefa(df_tarefa.id.values[0], df_tarefa.descricao.values[0], df_tarefa.data_limite.values[0], df_tarefa.status.values[0], funcionario)
        # Exibe os atributos da nova tarefa
        print(nova_tarefa.to_string())
        # Retorna o objeto nova_tarefa
        return nova_tarefa

    def atualizar_tarefa(self) -> Tarefa:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o ID da tarefa a ser alterada
        id_tarefa = int(input("ID da Tarefa que irá alterar: "))        

        # Verifica se a tarefa existe na base de dados
        if not self.verifica_existencia_tarefa(oracle, id_tarefa):
            
            # Lista os funcionários existentes para o usuário escolher o novo responsável
            self.listar_funcionarios(oracle)
            # Matrícula tratada como String (VARCHAR2)
            matricula_funcionario = input("Nova Matrícula do Funcionário (Responsável): ")
            funcionario = self.valida_funcionario(oracle, matricula_funcionario)
            if funcionario == None:
                return None

            # Solicita as novas informações
            nova_descricao = input("Nova Descrição da Tarefa: ")
            novo_status = input("Novo Status da Tarefa: ")
            nova_data_limite_str = input("Nova Data Limite (formato DD/MM/AAAA): ")
            nova_data_limite = parser.parse(nova_data_limite_str, dayfirst=True).date()

            # Atualiza a tarefa
            # Matrícula (ID_FUNCIONARIO) está entre aspas simples para ser tratada como string no SQL
            oracle.write(f"update LABDATABASE.TAREFA set DESCRICAO = '{nova_descricao}', STATUS = '{novo_status}', DATA_LIMITE = to_date('{nova_data_limite}','yyyy-mm-dd'), ID_FUNCIONARIO = '{funcionario.get_matricula()}' where ID = {id_tarefa}")
            
            # Recupera os dados da tarefa atualizada
            df_tarefa = oracle.sqlToDataFrame(f"select ID, DESCRICAO, DATA_LIMITE, STATUS, ID_FUNCIONARIO from LABDATABASE.TAREFA where ID = {id_tarefa}")
            # Cria um novo objeto Tarefa
            tarefa_atualizada = Tarefa(df_tarefa.id.values[0], df_tarefa.descricao.values[0], df_tarefa.data_limite.values[0], df_tarefa.status.values[0], funcionario)
            # Exibe os atributos da tarefa
            print(tarefa_atualizada.to_string())
            # Retorna o objeto tarefa_atualizada
            return tarefa_atualizada
        else:
            print(f"O ID {id_tarefa} não existe.")
            return None

    def excluir_tarefa(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o ID da tarefa a ser excluída
        id_tarefa = int(input("ID da Tarefa que irá excluir: "))        

        # Verifica se a tarefa existe na base de dados
        if not self.verifica_existencia_tarefa(oracle, id_tarefa):            
            # Recupera os dados da tarefa
            df_tarefa = oracle.sqlToDataFrame(f"select ID, DESCRICAO, DATA_LIMITE, STATUS, ID_FUNCIONARIO from LABDATABASE.TAREFA where ID = {id_tarefa}")
            funcionario = self.valida_funcionario(oracle, df_tarefa.id_funcionario.values[0])
            
            # Confirmação
            opcao_excluir = input(f"Tem certeza que deseja excluir a tarefa {id_tarefa} [S ou N]: ")
            if opcao_excluir.lower() == "s":
                # Revome a tarefa da tabela
                oracle.write(f"delete from LABDATABASE.TAREFA where ID = {id_tarefa}")
                # Cria um novo objeto Tarefa para informar que foi removido
                tarefa_excluida = Tarefa(df_tarefa.id.values[0], df_tarefa.descricao.values[0], df_tarefa.data_limite.values[0], df_tarefa.status.values[0], funcionario)
                # Exibe os atributos da tarefa excluída
                print("Tarefa Removida com Sucesso!")
                print(tarefa_excluida.to_string())
        else:
            print(f"O ID {id_tarefa} não existe.")

    def verifica_existencia_tarefa(self, oracle:OracleQueries, id:int=None) -> bool:
        # Recupera os dados da tarefa transformando em um DataFrame
        df_tarefa = oracle.sqlToDataFrame(f"select ID, DESCRICAO from LABDATABASE.TAREFA where ID = {id}")
        return df_tarefa.empty

    def listar_funcionarios(self, oracle:OracleQueries, need_connect:bool=False):
        query = """
                select f.matricula
                    , f.nome as funcionario 
                from LABDATABASE.FUNCIONARIO f
                order by f.nome
                """
        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))

    def valida_funcionario(self, oracle:OracleQueries, matricula_funcionario:str=None) -> Funcionario:
        # Verifica a existência do funcionário usando a string da matrícula
        if self.ctrl_funcionario.verifica_existencia_funcionario(oracle, matricula_funcionario):
            print(f"A Matrícula {matricula_funcionario} informada não existe na base.")
            return None
        else:
            oracle.connect()
            # CORREÇÃO FINAL: Colocar aspas simples na Matrícula no SQL para ser tratada como VARCHAR2
            df_funcionario = oracle.sqlToDataFrame(f"select MATRICULA, NOME, ID_SETOR from LABDATABASE.FUNCIONARIO where MATRICULA = '{matricula_funcionario}'")
            
            # Busca os dados do Setor
            # O ID_SETOR é um número, então não precisa de aspas no SQL
            df_setor = oracle.sqlToDataFrame(f"select ID, NOME from LABDATABASE.SETOR where ID = {df_funcionario.id_setor.values[0]}")
            
            # Cria os objetos Setor e Funcionario
            setor = Setor(df_setor.id.values[0], df_setor.nome.values[0])
            funcionario = Funcionario(df_funcionario.matricula.values[0], df_funcionario.nome.values[0], setor)
            return funcionario