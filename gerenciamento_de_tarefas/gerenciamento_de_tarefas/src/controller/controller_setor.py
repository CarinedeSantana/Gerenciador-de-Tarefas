from model.setor import Setor
from conexion.oracle_queries import OracleQueries

class Controller_Setor:
    def __init__(self):
        pass
        
    def inserir_setor(self) -> Setor:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        # Cria uma nova conexão com o banco
        oracle = OracleQueries()
        # Recupera o cursor para executar um bloco PL/SQL anônimo
        cursor = oracle.connect()
        # Cria a variável de saída com o tipo especificado
        output_value = cursor.var(int)

        # Solicita ao usuario o nome do novo setor
        nome_novo_setor = input("Nome do Setor (Novo): ")

        # Cria um dicionário para mapear as variáveis de entrada e saída
        data = dict(codigo=output_value, nome_setor=nome_novo_setor)
        # Executa o bloco PL/SQL anônimo para inserção e recuperação da chave primária
        cursor.execute("""
        begin
            :codigo := LABDATABASE.SETOR_ID_SEQ.NEXTVAL;
            insert into LABDATABASE.SETOR values(:codigo, :nome_setor);
        end;
        """, data)
        # Recupera o código do novo setor
        id_setor = output_value.getvalue()
        # Persiste (confirma) as alterações
        oracle.conn.commit()
        # Recupera os dados do novo setor criado
        df_setor = oracle.sqlToDataFrame(f"select ID, NOME from LABDATABASE.SETOR where ID = {id_setor}")
        # Cria um novo objeto Setor
        novo_setor = Setor(df_setor.id.values[0], df_setor.nome.values[0])
        # Exibe os atributos do novo setor
        print(novo_setor.to_string())
        # Retorna o objeto novo_setor
        return novo_setor

    def atualizar_setor(self) -> Setor:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o ID do setor a ser alterado
        id_setor = int(input("ID do Setor que irá alterar: "))        

        # Verifica se o setor existe na base de dados
        if not self.verifica_existencia_setor(oracle, id_setor):
            # Solicita o novo nome do setor
            novo_nome_setor = input("Nome do Setor (Novo): ")
            # Atualiza o nome do setor existente
            oracle.write(f"update LABDATABASE.SETOR set NOME = '{novo_nome_setor}' where ID = {id_setor}")
            # Recupera os dados do setor atualizado
            df_setor = oracle.sqlToDataFrame(f"select ID, NOME from LABDATABASE.SETOR where ID = {id_setor}")
            # Cria um novo objeto Setor
            setor_atualizado = Setor(df_setor.id.values[0], df_setor.nome.values[0])
            # Exibe os atributos do setor atualizado
            print(setor_atualizado.to_string())
            # Retorna o objeto setor_atualizado
            return setor_atualizado
        else:
            print(f"O ID {id_setor} não existe.")
            return None

    def excluir_setor(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o ID do setor a ser excluído
        id_setor = int(input("ID do Setor que irá excluir: "))        

        # Verifica se o setor existe na base de dados
        if not self.verifica_existencia_setor(oracle, id_setor):            
            # Recupera os dados do setor
            df_setor = oracle.sqlToDataFrame(f"select ID, NOME from LABDATABASE.SETOR where ID = {id_setor}")
            # Revome o setor da tabela
            oracle.write(f"delete from LABDATABASE.SETOR where ID = {id_setor}")            
            # Cria um novo objeto Setor para informar que foi removido
            setor_excluido = Setor(df_setor.id.values[0], df_setor.nome.values[0])
            # Exibe os atributos do setor excluído
            print("Setor Removido com Sucesso!")
            print(setor_excluido.to_string())
        else:
            print(f"O ID {id_setor} não existe.")

    def verifica_existencia_setor(self, oracle:OracleQueries, id:int=None) -> bool:
        # Recupera os dados do setor transformando em um DataFrame
        df_setor = oracle.sqlToDataFrame(f"select ID, NOME from LABDATABASE.SETOR where ID = {id}")
        return df_setor.empty