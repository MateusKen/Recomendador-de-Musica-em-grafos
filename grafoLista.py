"""
NOME: Erik Samuel Viana Hsu
RA: 10403109
NOME: Mateus Kenzo Iochimoto
RA: 10400995
NOME: Thiago Shihan Cardoso Toma
RA: 10400764
"""

import csv

class Genero:
    """Classe base para vértices."""
    def __init__(self, nome):
        self.nome = nome  # nome único do vértice

    def __str__(self):
        return self.nome

class Usuario:
    """Classe para vértices do tipo Usuário."""
    def __init__(self, nome):
        self.nome = nome

    def __str__(self):
        return self.nome

class Musica:
    """Classe para vértices do tipo Música."""
    def __init__(self, nome, generos):
        self.nome = nome
        self.generos = generos  # Suporte a múltiplos gêneros

    def __str__(self):
        return self.nome
    
class Grafo:
    def __init__(self):
        self.adj = {}  # Dicionário de conjuntos de adjacência

    def adiciona_vertice(self, vertice):
        if vertice not in self.adj:
            self.adj[vertice] = set()

    def insereA(self, v, w):
        """Insere uma aresta não direcionada entre os vértices v e w."""
        if v in self.adj and w in self.adj:
            self.adj[v].add(w)  # Adiciona w à lista de adjacência de v
            self.adj[w].add(v)  # Adiciona v à lista de adjacência de w

    def removeA(self, v, w):
        """Remove uma aresta não direcionada entre os vértices v e w."""
        if v in self.adj and w in self.adj[v]:
            self.adj[v].remove(w)  # Remove w da lista de adjacência de v
        if w in self.adj and v in self.adj[w]:
            self.adj[w].remove(v)  # Remove v da lista de adjacência de w

    def eh_conexo(self):
        """
        Verifica se o grafo é conexo (todos os vértices são alcançáveis a partir de qualquer vértice).
        
        Returns:
        bool: True se o grafo for conexo, False caso contrário
        """
        if not self.adj:
            return False
        
        # Escolhe um vértice inicial para iniciar a busca
        inicio = list(self.adj.keys())[0]
        
        # Conjunto para rastrear vértices visitados
        visitados = set()
        
        def dfs(vertice):
            """Busca em profundidade para marcar vértices alcançáveis"""
            visitados.add(vertice)
            for vizinho in self.adj[vertice]:
                if vizinho not in visitados:
                    dfs(vizinho)
        
        # Realiza DFS a partir do vértice inicial
        dfs(inicio)
        
        # Verifica se todos os vértices foram visitados
        return len(visitados) == len(self.adj)
    
    def show(self):
        for v, conexoes in self.adj.items():
            conexoes_str = ', '.join(map(str, conexoes))  # Junta os vizinhos em uma string
            print(f"{v} -> {conexoes_str if conexoes else 'Sem conexões'}")
