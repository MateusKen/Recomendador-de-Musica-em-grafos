"""
NOME: Erik Samuel Viana Hsu
RA: 10403109
NOME: Mateus Kenzo Iochimoto
RA: 10400995
NOME: Thiago Shihan Cardoso Toma
RA: 10400764
"""

class Vertice:
    """Classe base para vértices."""
    def __init__(self, id):
        self.id = id  # Identificador único do vértice

    def __str__(self):
        return f"Vértice {self.id}"


class Usuario(Vertice):
    """Classe para vértices do tipo Usuário."""
    def __init__(self, id, nome):
        super().__init__(id)
        self.nome = nome

    def __str__(self):
        return f"Usuário: {self.nome}"


class Musica(Vertice):
    """Classe para vértices do tipo Música."""
    def __init__(self, id, nome, genero):
        super().__init__(id)
        self.nome = nome
        self.genero = genero

    def __str__(self):
        return f"Música: {self.nome} (Gênero: {self.genero})"
    
class Grafo:
    def __init__(self):
        self.adj = {}  # Dicionário de listas de adjacência

    def adiciona_vertice(self, id):
        if id not in self.adj:
            self.adj[id] = []

    def insereA(self, v, w):
        if v in self.adj and w in self.adj:
            self.adj[v].append(w)

    def removeA(self, v, w):
        if v in self.adj and w in self.adj[v]:
            self.adj[v].remove(w)

    def show(self):
        for v, conexoes in self.adj.items():
            conexoes_str = ', '.join(map(str, conexoes))
            print(f"Vértice {v}: {conexoes_str if conexoes else 'Sem conexões'}")
