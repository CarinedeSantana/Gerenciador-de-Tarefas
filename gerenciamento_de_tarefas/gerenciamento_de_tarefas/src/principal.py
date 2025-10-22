from utils import config
from utils.splash_screen import SplashScreen
from reports.relatorios import Relatorio

# Importação dos novos controllers (adaptados para SETOR, FUNCIONARIO, TAREFA)
from controller.controller_setor import Controller_Setor
from controller.controller_funcionario import Controller_Funcionario
from controller.controller_tarefa import Controller_Tarefa

# Inicialização dos objetos
tela_inicial = SplashScreen()
relatorio = Relatorio()

# Inicialização dos controllers
ctrl_setor = Controller_Setor()
ctrl_funcionario = Controller_Funcionario()
ctrl_tarefa = Controller_Tarefa()


def reports(opcao_relatorio:int=0):
    # As opções correspondem ao MENU_RELATORIOS do config.py
    if opcao_relatorio == 1:
        relatorio.get_relatorio_tarefas_por_funcionario() # 1 - Relatório de Tarefas por Funcionário
    elif opcao_relatorio == 2:
        relatorio.get_relatorio_tarefas()                   # 2 - Relatório de Todas as Tarefas
    elif opcao_relatorio == 3:
        relatorio.get_relatorio_funcionarios()              # 3 - Relatório de Funcionários
    elif opcao_relatorio == 4:
        relatorio.get_relatorio_setores()                   # 4 - Relatório de Setores


def inserir(opcao_inserir:int=0):
    # As opções correspondem ao MENU_ENTIDADES do config.py
    if opcao_inserir == 1:                               # 1 - SETOR
        novo_setor = ctrl_setor.inserir_setor()
    elif opcao_inserir == 2:                             # 2 - FUNCIONÁRIO
        novo_funcionario = ctrl_funcionario.inserir_funcionario()
    elif opcao_inserir == 3:                             # 3 - TAREFA
        nova_tarefa = ctrl_tarefa.inserir_tarefa()


def atualizar(opcao_atualizar:int=0):
    # As opções correspondem ao MENU_ENTIDADES do config.py
    if opcao_atualizar == 1:                             # 1 - SETOR
        setor_atualizado = ctrl_setor.atualizar_setor()
    elif opcao_atualizar == 2:                           # 2 - FUNCIONÁRIO
        funcionario_atualizado = ctrl_funcionario.atualizar_funcionario()
    elif opcao_atualizar == 3:                           # 3 - TAREFA
        tarefa_atualizada = ctrl_tarefa.atualizar_tarefa()


def excluir(opcao_excluir:int=0):
    # As opções correspondem ao MENU_ENTIDADES do config.py
    if opcao_excluir == 1:                               # 1 - SETOR
        ctrl_setor.excluir_setor()
    elif opcao_excluir == 2:                             # 2 - FUNCIONÁRIO
        ctrl_funcionario.excluir_funcionario()
    elif opcao_excluir == 3:                             # 3 - TAREFA
        ctrl_tarefa.excluir_tarefa()


def run():
    print(tela_inicial.get_updated_screen())
    config.clear_console()

    while True:
        print(config.MENU_PRINCIPAL)
        opcao = int(input("Escolha uma opção [1-5]: "))
        config.clear_console(1)

        if opcao == 1: # 1 - Relatórios
            print(config.MENU_RELATORIOS)
            # O MENU_RELATORIOS vai de 0 a 4
            opcao_relatorio = int(input("Escolha uma opção [0-4]: "))
            config.clear_console(1)

            reports(opcao_relatorio)

            config.clear_console(1)

        elif opcao == 2: # 2 - Inserir Registros

            print(config.MENU_ENTIDADES)
            # O MENU_ENTIDADES vai de 1 a 3
            opcao_inserir = int(input("Escolha uma opção [1-3]: "))
            config.clear_console(1)

            inserir(opcao_inserir=opcao_inserir)

            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 3: # 3 - Atualizar Registros

            print(config.MENU_ENTIDADES)
            # O MENU_ENTIDADES vai de 1 a 3
            opcao_atualizar = int(input("Escolha uma opção [1-3]: "))
            config.clear_console(1)

            atualizar(opcao_atualizar=opcao_atualizar)

            config.clear_console()

        elif opcao == 4: # 4 - Remover Registros

            print(config.MENU_ENTIDADES)
            # O MENU_ENTIDADES vai de 1 a 3
            opcao_excluir = int(input("Escolha uma opção [1-3]: "))
            config.clear_console(1)

            excluir(opcao_excluir=opcao_excluir)

            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 5: # 5 - Sair

            print(tela_inicial.get_updated_screen())
            config.clear_console()
            print("Obrigado por utilizar o nosso sistema.")
            exit(0)

        else:
            print("Opção inválida.")
            config.clear_console(1)

if __name__ == "__main__":
    run()