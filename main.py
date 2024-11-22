"""
NOME: Erik Samuel Viana Hsu
RA: 10403109
NOME: Mateus Kenzo Iochimoto
RA: 10400995
NOME: Thiago Shihan Cardoso Toma
RA: 10400764
"""

import csv
from collections import Counter
from importarMusica import buscar_info_artista_por_musica
from grafoLista import *
import pandas as pd
import ast

generos_aceitos = ["adoracao", "gospel", "rock", "folk", "reggae", "pop", "christian", "worship", "j-pop", "hip hop", "k-pop", "mpb", "indie", "sertanejo", "r&b", "disco", "broadway", "samba", "bossa nova", "jazz", "singer-songwriter", "rap", "trap", "funk", "classical", "emo", "alt", "metal", "game", "soul", "blues", "opera", "symphonic", "instrumental", "edm", "country", "punk", "lo-fi", "pagode", "j-rock", "vtuber", "anime"]
# Dicionário para associar músicas aos seus objetos
musicas = {}

# Dicionário para associar gêneros aos seus vértices
generos = {}

def ler_forms(arquivo):
    """
    Lê o formulário de entrada, realiza chamadas para obter informações das músicas,
    e atualiza o nome das músicas no formulário com os nomes padronizados da API.
    
    Parâmetros:
    - arquivo (str): Caminho para o arquivo CSV do formulário.
    
    Salva:
    - Atualiza o CSV do formulário com os nomes padronizados das músicas.
    """
    # Carregar o CSV do formulário
    df = pd.read_csv(arquivo, delimiter=",")
    
    # Lista para armazenar todas as informações das músicas
    musicas_info = {}

    for index, row in df.iterrows():
        # Dividir a coluna 'musica' por ';'
        musicas = row['musica'].split(';')
        musicas_padronizadas = []

        for musica in musicas:
            musica = musica.strip()  # Remove espaços extras
            info_musica = buscar_info_artista_por_musica(musica)  # Chamada da API

            if info_musica:
                # Normalizar os gêneros usando a função mapear_generos
                generos_mapeados = mapear_generos(info_musica.get('generos', []).split(", "))
                info_musica['generos_mapeados'] = generos_mapeados  # Já será uma string

                # Substituir nome da música pelo padronizado
                nome_musica_padronizado = info_musica['musica']
                musicas_padronizadas.append(nome_musica_padronizado)

                # Atualizar dicionário de informações de músicas
                if nome_musica_padronizado in musicas_info:
                    musicas_info[nome_musica_padronizado]['aparicoes'] += 1
                else:
                    musicas_info[nome_musica_padronizado] = info_musica
            else:
                # Caso não encontre informações na API, manter o nome original
                musicas_padronizadas.append(musica)

        # Atualizar a coluna 'musica' no DataFrame
        df.at[index, 'musica'] = "; ".join(musicas_padronizadas)
        
    # Salvar o formulário atualizado
    df.to_csv("forms.csv", index=False)

    # Salvar o CSV com informações de músicas
    df_final = pd.DataFrame.from_dict(musicas_info, orient='index')
    df_final.to_csv("musicas_info.csv", index=False)

def mapear_generos(generos_musica):
    """
    Mapeia uma lista de gêneros específicos para seus gêneros principais, sem repetições.

    Parâmetros:
    - generos_musica (list): Lista de gêneros associados à música.

    Retorna:
    - list: Lista de gêneros mapeados para os gêneros principais (sem repetições) 
            ou ['N/A'] se nenhum gênero corresponder.
    """
    # Normaliza os gêneros aceitos para comparação
    
    generos_aceitos_normalizados = {g.lower(): g for g in generos_aceitos}  
    generos_mapeados = set()  # Conjunto para evitar repetições

    if not generos_musica:  # Verifica se a lista de gêneros está vazia
        return ["N/A"]

    for genero in generos_musica:
        genero_lower = genero.lower()  # Normaliza o gênero para comparação
        generos_encontrados = []

        # Procura por todos os gêneros aceitos como substrings
        for aceito_lower, aceito_original in generos_aceitos_normalizados.items():
            if aceito_lower in genero_lower:  # Substring encontrada
                generos_encontrados.append(aceito_original)

        # Adiciona todos os gêneros encontrados ao conjunto
        if generos_encontrados:
            generos_mapeados.update(generos_encontrados)

    # Se nenhum gênero foi mapeado, retorna 'N/A'
    return ", ".join(sorted(generos_mapeados)) if generos_mapeados else "N/A"

def carregar_grafo(caminho_formulario, caminho_musicas):
    grafo = Grafo()
    usuario_id = 1

    
    # Carregar as informações de músicas e gêneros
    with open(caminho_musicas, newline='', encoding='utf-8') as file_musicas:
        reader = csv.DictReader(file_musicas)
        for linha in reader:
            nome_musica = linha['musica'].strip()
            
            lista_generos = linha['generos_mapeados'].split(", ")
            
            # Criar vértice da música
            musica_vertice = Musica(nome=nome_musica, generos=lista_generos)
            musicas[nome_musica] = musica_vertice
            grafo.adiciona_vertice(musica_vertice.nome)
            
            # Criar vértices para os gêneros, se ainda não existirem
            for genero in lista_generos:
                genero_vertice = Genero(genero)
                generos[genero] = genero_vertice
                grafo.adiciona_vertice(genero_vertice.nome)
                
                # Conectar música ao gênero
                grafo.insereA(musica_vertice.nome, generos[genero].nome)

    # Carregar as informações dos usuários e suas respostas
    with open(caminho_formulario, newline='', encoding='utf-8') as file_formulario:
        reader = csv.DictReader(file_formulario)
        for row in reader:
            # Criar vértice do usuário
            usuario_vertice = Usuario(nome=row['nome'])
            grafo.adiciona_vertice(usuario_vertice.nome)

            # Conectar o usuário às músicas que ele marcou
            musicas_marcadas = row['musica'].split(';')  # Músicas separadas por ';'
            for musica_nome in musicas_marcadas:
                musica_nome = musica_nome.strip()
                if musica_nome in musicas:
                    grafo.insereA(usuario_vertice.nome, musicas[musica_nome].nome)

    return grafo

def mostra_arquivo(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as f:
        tudo = f.readlines()
        for linha in tudo:
            print(linha.strip())
    f.close()

def deletar_grafo(grafo):
    grafo = None

def gravar_grafo(grafo, arquivo):
    with open(arquivo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
        writer = csv.writer(arquivo_csv)
        
        # Escrevendo cabeçalho
        writer.writerow(["Vértice", "Tipo", "Arestas"])

        # Iterando pelos vértices e suas conexões
        for vertice, conexoes in grafo.adj.items():
            # Determinar o tipo do vértice com base na classe
            if isinstance(vertice, Usuario):
                tipo = "Usuário"
            elif isinstance(vertice, Musica):
                tipo = "Música"
            elif isinstance(vertice, Genero):
                tipo = "Gênero"
            else:
                tipo = "Desconhecido"

            # Conexões serão representadas como uma string separada por vírgulas
            conexoes_str = ", ".join(map(str, conexoes))
            writer.writerow([vertice, tipo, conexoes_str])
    arquivo_csv.close()

def menu():
    grafo = None
    while True:
        print("\nMenu de opções: ")
        print("a1. Le o arquivo do forms (faz chamada na API)")#👍
        print("a. Ler dados do arquivo e criar grafo")#👍
        print("b. Gravar dados no arquivo")#👍
        print("c. Inserir vértice")#👍
        print("d. Inserir aresta")#👍
        print("e. Remover vértice")
        print("f. Remover aresta")
        print("g. Mostrar conteúdo do arquivo")
        print("h. Mostrar grafo")#👍
        print("i. Apresentar conexidade do grafo")
        print("j. Sair")

        opcao = input("\nEscolha uma opção: ")
        if opcao == "a1":
            ler_forms("forms.csv")
            
        elif opcao == "a":
            grafo = carregar_grafo("forms.csv", "musicas_info.csv")
            print("Grafo criado!")

        elif opcao == "b":
            if grafo:

                gravar_grafo(grafo, "forms1.csv")
                print(f"Grafo gravado em forms1.csv.")
            else:
                print("Grafo não carregado.")

        elif opcao == "c":
            if grafo is not None: 
                op = input("\nVoce gostaria de adicionar uma musica ou um usuario? ")
                if op.lower() == "musica":
                    newMusica = input("\nDigite o nome da música a ser inserida: ")

                    info_musica = buscar_info_artista_por_musica(newMusica)
                    generos_mapeados = mapear_generos(info_musica.get('generos', []).split(", ")).split(", ")
                    novaMusica = Musica(info_musica['musica'], generos_mapeados)
                    grafo.adiciona_vertice(novaMusica.nome)

                    for genero in generos_mapeados:
                        genero_vertice = Genero(genero)
                        generos[genero] = genero_vertice
                        grafo.adiciona_vertice(genero_vertice.nome)
                
                        # Conectar música ao gênero
                        grafo.insereA(novaMusica.nome, generos[genero].nome)

                elif op.lower() == "usuario":
                    newUsuario = input("\nDigite o nome do usuario a ser inserido: ")
                    novoUsuario = Usuario(newUsuario)
                    grafo.adiciona_vertice(novoUsuario)
                else:
                    print("Opcao nao identificada")
            else:
                print("Grafo não carregado.")
            print(grafo.adj)
        elif opcao == "d":
            if grafo:
                v = input("\nDigite o vértice de origem: ")
                w = input("Digite o vértice de destino: ")
                grafo.insereA(v, w)

            else:
                print("Grafo não carregado.")

        elif opcao == "e":
            if grafo:
                v = input("Digite o vértice a ser removido: ")
                grafo.adj.pop(v)

            else:
                print("Grafo não carregado.")
        elif opcao == "f":
            if grafo:
                v = int(input("Digite o vértice de origem: "))
                w = int(input("Digite o vértice de destino: "))
                grafo.removeA(v, w)
                print(f"Aresta {v} -> {w} removida.")
            else:
                print("Grafo não carregado.")
        
        elif opcao == "g":
            arquivo = input("Digite o nome do arquivo: ")
            grafo = mostra_arquivo(arquivo)

        elif opcao == "h":
            if grafo:
                grafo.show()
            else:
                print("Grafo não carregado.")

        elif opcao == "i":
                if(grafo.eh_conexo()):
                    print("O grafo é conexo")
                else:
                    print("O grafo é desconexo")

        elif opcao == "j":
            break

        else:
            print("Opção inválida.")

menu()
grafo = Grafo()
musicaA = Musica("ZE roberto", ["pagode"])
musicaB = Musica("ADAA", ["rock", "metal"])
usuarioA = Usuario("Joao")
usuarioB = Usuario("Mario")
grafo.adiciona_vertice(usuarioA)
grafo.adiciona_vertice(usuarioB)
grafo.adiciona_vertice(musicaA)
grafo.adiciona_vertice(musicaB)
grafo.adiciona_vertice("pagode")
grafo.adiciona_vertice("rock")
grafo.adiciona_vertice("metal")
grafo.insereA(musicaA, "pagode")
grafo.insereA(musicaB, "rock")
grafo.insereA(musicaB, "metal")
grafo.insereA(usuarioA, musicaA)
grafo.insereA(usuarioA, musicaB)
grafo.show()
gravar_grafo(grafo, "forms1.csv")
print("FOI!")
