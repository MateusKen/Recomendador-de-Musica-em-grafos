"""
NOME: Erik Samuel Viana Hsu
RA: 10403109
NOME: Mateus Kenzo Iochimoto
RA: 10400995
NOME: Thiago Shihan Cardoso Toma
RA: 10400764
"""

import csv

class Grafo:
    def __init__(self, n):
        self.V = n  # Número de vértices
        self.adj = [[] for _ in range(n)]  # Lista de adjacência
        self.musicas = {}  # Dicionário para armazenar as músicas

    

    def insereA(self, v, w):
        self.adj[v].append(w)  # Insere aresta de v para w

    def removeA(self, v, w):
        self.adj[v].remove(w)

    def set_musica(self, v, musica):
        self.musicas[v] = musica  # Associa música ao vértice v

    def show(self):
        for v in range(self.V):
            # Recupera a música associada ao vértice v, se existir
            musica = self.musicas.get(v, "Nenhuma música")
            # Formata a string para mostrar a conexão
            conexoes = ' -> '.join(f"{self.musicas.get(w, 'Nenhuma música')}" for w in self.adj[v])
            print(f"Vértice {v} ({musica}): {conexoes if conexoes else 'Sem conexões'}")