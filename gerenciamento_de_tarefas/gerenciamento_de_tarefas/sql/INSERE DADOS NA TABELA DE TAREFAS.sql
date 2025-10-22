/* INSERE DADOS NA TABELA DE TAREFAS (depende de FUNCIONARIO) */
DECLARE
  VID_TAREFA NUMBER;
  VMATRICULA_FUNC NUMBER;
  VDATA_LIMITE DATE;
BEGIN
  -- Tarefa para 'ANA PAULA' (Desenvolvimento)
  VID_TAREFA := LABDATABASE.TAREFA_ID_SEQ.NEXTVAL;
  VDATA_LIMITE := SYSDATE + 7; -- Vencimento em 7 dias
  
  SELECT MATRICULA
    INTO VMATRICULA_FUNC
    FROM LABDATABASE.FUNCIONARIO
   WHERE NOME = 'ANA PAULA';
  
  INSERT INTO LABDATABASE.TAREFA VALUES(VID_TAREFA,       /*ID*/
                             'Implementar API de Pagamentos', /*DESCRICAO*/
                             VDATA_LIMITE,              /*DATA_LIMITE*/
                             'Em Andamento',            /*STATUS*/
                             VMATRICULA_FUNC            /*ID_FUNCIONARIO*/
                             );
END;
--
DECLARE
  VID_TAREFA NUMBER;
  VMATRICULA_FUNC NUMBER;
  VDATA_LIMITE DATE;
BEGIN
  -- Tarefa para 'CARLA MELO' (Infraestrutura)
  VID_TAREFA := LABDATABASE.TAREFA_ID_SEQ.NEXTVAL;
  VDATA_LIMITE := SYSDATE + 3; -- Vencimento em 3 dias
  
  SELECT MATRICULA
    INTO VMATRICULA_FUNC
    FROM LABDATABASE.FUNCIONARIO
   WHERE NOME = 'CARLA MELO';
  
  INSERT INTO LABDATABASE.TAREFA VALUES(VID_TAREFA,       /*ID*/
                             'Atualizar Servidor de Banco de Dados', /*DESCRICAO*/
                             VDATA_LIMITE,              /*DATA_LIMITE*/
                             'Pendente',                /*STATUS*/
                             VMATRICULA_FUNC            /*ID_FUNCIONARIO*/
                             );
END;
--
DECLARE
  VID_TAREFA NUMBER;
  VMATRICULA_FUNC NUMBER;
  VDATA_LIMITE DATE;
BEGIN
  -- Tarefa para 'ELIANA GOMES' (Financeiro)
  VID_TAREFA := LABDATABASE.TAREFA_ID_SEQ.NEXTVAL;
  VDATA_LIMITE := SYSDATE + 14; -- Vencimento em 14 dias
  
  SELECT MATRICULA
    INTO VMATRICULA_FUNC
    FROM LABDATABASE.FUNCIONARIO
   WHERE NOME = 'ELIANA GOMES';
  
  INSERT INTO LABDATABASE.TAREFA VALUES(VID_TAREFA,       /*ID*/
                             'Fechamento Mensal de Contas', /*DESCRICAO*/
                             VDATA_LIMITE,              /*DATA_LIMITE*/
                             'Pendente',                /*STATUS*/
                             VMATRICULA_FUNC            /*ID_FUNCIONARIO*/
                             );
END;