from model.setor import Setor # Assume que 'setor.py' estará no mesmo pacote/diretório 'model'

class Funcionario:
    def __init__(self, 
                 matricula:str=None, # CORREÇÃO: Deve ser str
                 nome:str=None,
                 setor:Setor=None
                 ):
        self.set_matricula(matricula)
        self.set_nome(nome)
        self.set_setor(setor)

    def set_matricula(self, matricula:str): # CORREÇÃO: Deve ser str
        self.matricula = matricula

    def set_nome(self, nome:str):
        self.nome = nome

    def set_setor(self, setor:Setor):
        self.setor = setor

    def get_matricula(self) -> str: # CORREÇÃO: Deve ser str
        return self.matricula

    def get_nome(self) -> str:
        return self.nome

    def get_setor(self) -> Setor:
        return self.setor

    def to_string(self) -> str:
        # Inclui o nome do setor na string
        nome_setor = self.get_setor().get_nome() if self.get_setor() else "N/A"
        return f"Matrícula: {self.get_matricula()} | Nome: {self.get_nome()} | Setor: {nome_setor}"