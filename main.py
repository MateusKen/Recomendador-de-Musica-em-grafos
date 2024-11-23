"""
NOME: Erik Samuel Viana Hsu
RA: 10403109
NOME: Mateus Kenzo Iochimoto
RA: 10400995
NOME: Thiago Shihan Cardoso Toma
RA: 10400764
"""

import csv
from importarMusica import buscar_info_artista_por_musica
from grafoLista import *
import pandas as pd

generos_aceitos = ["adoracao", "gospel", "rock", "folk", "reggae", "pop", "christian", "worship", "j-pop", "hip hop", "k-pop", "mpb", "indie", "sertanejo", "r&b", "disco", "broadway", "samba", "bossa nova", "jazz", "singer-songwriter", "rap", "trap", "funk", "classical", "emo", "alt", "metal", "game", "soul", "blues", "opera", "symphonic", "instrumental", "edm", "country", "punk", "lo-fi", "pagode", "j-rock", "vtuber", "anime"]

# Dicionário para associar músicas aos seus objetos
musicas = {}

# Dicionário para associar gêneros aos seus vértices
generos = {}

# Dicionário para associar usuários aos seus vértices
usuarios = {}

def verifica_duplicatas(nome, lista):
    return nome in lista

def ler_forms(arquivo):
    """
    Lê o formulário de entrada, realiza chamadas para obter informações das músicas,
    e atualiza o nome das músicas no formulário com os nomes padronizados da API.
    
    Parâmetros:
    - arquivo (str): Caminho para o arquivo CSV do formulário.
    
    Salva:
    - Atualiza o CSV do formulário com os nomes padronizados das músicas.
    - Salva o CSV com informações das músicas (sem colunas desnecessárias).
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
                info_musica['generos'] = generos_mapeados  # Já será uma string

                # Substituir nome da música pelo padronizado
                nome_musica_padronizado = info_musica['musica']
                musicas_padronizadas.append(nome_musica_padronizado)

                # Atualizar dicionário de informações de músicas
                if nome_musica_padronizado not in musicas_info:
                    # Adicionar apenas as colunas relevantes
                    musicas_info[nome_musica_padronizado] = {
                        'musica': nome_musica_padronizado,
                        'generos': generos_mapeados,
                    }
            else:
                # Caso não encontre informações na API, manter o nome original
                musicas_padronizadas.append(musica)

        # Atualizar a coluna 'musica' no DataFrame
        df.at[index, 'musica'] = ";".join(musicas_padronizadas)
        
    # Salvar o formulário atualizado
    df.to_csv("forms.csv", index=False)

    # Salvar o CSV com informações de músicas
    df_final = pd.DataFrame.from_dict(musicas_info, orient='index')
    df_final.to_csv("musicas_info.csv", index=False)

def procura_em_adj(obj, grafo, tipo):
    lista = []
    for node in grafo.adj[obj]:
        if isinstance(node , tipo):
            lista.append(node)
    return lista

def recomendar_musicas_similariodade(grafo, usuario_nome):
    """
    Recomenda músicas para um usuário com base nas músicas ouvidas por outros usuários conectados.

    Parâmetros:
    - grafo (Grafo): O grafo contendo usuários, músicas e gêneros.
    - usuario_nome (str): O nome do usuário para o qual serão feitas as recomendações.

    Retorna:
    - list: Lista de músicas recomendadas para o usuário.
    """
    lista_recomendacao = []
    if usuario_nome in usuarios:
        musicas_de_usuario = procura_em_adj(usuarios[usuario_nome], grafo, Musica)
        for musica in musicas_de_usuario:
            usuario_comum = procura_em_adj(musica, grafo, Usuario)
            if usuarios[usuario_nome] in usuario_comum:
                usuario_comum.remove(usuarios[usuario_nome])

            if usuario_comum != []: #se existir alguém que ouve a mesma música
                for usuario in usuario_comum:
                    print(f"Achou-se uma recomendação para {usuario_nome} porque {usuario.nome} também ouve {musica.nome}")
                    for i in procura_em_adj(usuario, grafo, Musica):
                        lista_recomendacao.append(i.nome)
            else:
                print(f"Ninguém mais ouve {musica.nome} além de {usuario_nome}")
        
        for musica in musicas_de_usuario:
            if musica.nome in lista_recomendacao:
                lista_recomendacao.remove(musica.nome)
            
    else:
        print(f"O usuário {usuario_nome} não existe")
    
    return lista_recomendacao

def recomendar_musicas_por_genero(grafo, usuario_nome):
    """
    Recomenda músicas para um usuário com base nos gêneros das músicas que ele ouve.

    Parâmetros:
    - grafo (Grafo): O grafo contendo usuários, músicas e gêneros.
    - usuario_nome (str): O nome do usuário para o qual serão feitas as recomendações.

    Retorna:
    - list: Lista de músicas recomendadas para o usuário.
    """
    lista_recomendacao = []

    if usuario_nome in usuarios:
        # Pegar as músicas que o usuário ouve
        musicas_de_usuario = procura_em_adj(usuarios[usuario_nome], grafo, Musica)

        # Pegar os gêneros das músicas que o usuário ouve
        generos_do_usuario = set()
        for musica in musicas_de_usuario:
            generos_do_usuario.update(procura_em_adj(musica, grafo, Genero))
        
        # Listar os gêneros disponíveis para o usuário
        generos_nomes = [genero.nome for genero in generos_do_usuario]
        print(f"Gêneros disponíveis para {usuario_nome}: {', '.join(generos_nomes)}")
        
        # Perguntar ao usuário qual gênero analisar
        escolha = input("Digite o nome de um gênero para analisar ou 'todos' para considerar todos: ").strip()
        
        if escolha.lower() == 'todos':
            generos_selecionados = generos_do_usuario
        else:
            genero_escolhido = next((g for g in generos_do_usuario if g.nome.lower() == escolha.lower()), None)
            if genero_escolhido:
                generos_selecionados = {genero_escolhido}
            else:
                print(f"Gênero '{escolha}' não encontrado. Nenhuma recomendação será feita.")
                return lista_recomendacao

        # Para cada gênero selecionado, buscar músicas conectadas a ele
        for genero in generos_selecionados:
            musicas_no_genero = procura_em_adj(genero, grafo, Musica)
            for musica in musicas_no_genero:
                if musica not in musicas_de_usuario and musica.nome not in lista_recomendacao:
                    lista_recomendacao.append(musica.nome)
                    print(f"Recomenda-se {musica.nome} para {usuario_nome}, baseado no gênero {genero.nome}")
    else:
        print(f"O usuário {usuario_nome} não existe.")

    return lista_recomendacao

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

    # Carregar as informações de músicas e gêneros
    with open(caminho_musicas, newline='', encoding='utf-8') as file_musicas:
        reader = csv.DictReader(file_musicas)
        for linha in reader:
            nome_musica = linha['musica'].strip() #string
            lista_generos = linha['generos'].split(";") #lista
            # Criar vértice da música
            musica_vertice = Musica(nome_musica) #objeto musica
            musicas[nome_musica] = musica_vertice #adiciona ao dicionario referencia ao objeto
            grafo.adiciona_vertice(musica_vertice) #cria um vertice no grafo com o nome
            
            # Criar vértices para os gêneros, se ainda não existirem
            for genero in lista_generos:
                if genero not in generos:
                    genero_vertice = Genero(genero) #objeto genero
                    generos[genero] = genero_vertice #adiciona ao dicionario referencia ao objeto
                    grafo.adiciona_vertice(genero_vertice)
                
                # Conectar música ao gênero
                grafo.insereA(musica_vertice, genero_vertice)

    # Carregar as informações dos usuários e suas respostas
    with open(caminho_formulario, newline='', encoding='utf-8') as file_formulario:
        reader = csv.DictReader(file_formulario)
        for row in reader:
            # Criar vértice do usuário
            usuario_vertice = Usuario(row['nome']) #objeto usuario
            usuarios[row['nome']] = usuario_vertice #adiciona usuario ao dicionario
            grafo.adiciona_vertice(usuario_vertice)

            # Conectar o usuário às músicas que ele marcou
            musicas_marcadas = row['musica'].split(';')
            for musica_nome in musicas_marcadas:
                musica_nome = musica_nome.strip()
                grafo.insereA(usuario_vertice, musicas[musica_nome])

    return grafo

def mostra_arquivo(arquivo):
    try:
        with open(arquivo, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            
            # Imprime as linhas do arquivo
            for linha in reader:
                print(", ".join(linha))
    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo}' não foi encontrado.")
    except Exception as e:
        print(f"Erro ao ler o arquivo '{arquivo}': {e}")

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
        print("a2. Recomendar musica por similaridade")#👍
        print("a3. Recomendar musica por genero")#👍
        print("a. Ler dados do arquivo e criar grafo")#👍
        print("b. Gravar dados no arquivo")#👍
        print("c. Inserir vértice")#👍
        print("d. Inserir aresta")#👍
        print("e. Remover vértice")#👍
        print("f. Remover aresta")#👍
        print("g. Mostrar conteúdo do arquivo")#👍
        print("h. Mostrar grafo")#👍
        print("i. Apresentar conexidade do grafo")#👍
        print("j. Sair")#👍

        opcao = input("\nEscolha uma opção: ")
        if opcao == "a1":
            ler_forms("forms.csv")
            print("Dados salvos!")
        
        elif opcao == "a2":
            nome = input("Digite o nome do usuário para fazer a recomendação: ")
            recomendacao = recomendar_musicas_similariodade(grafo, nome)
            if recomendacao != []:
                print(f"As músicas para recomendar para {nome} são: {', '.join(recomendacao)}")
            else:
                print(f"Não deu para achar nenhuma recomendação para {nome}")
        
        elif opcao == "a3":
            nome = input("Digite o nome do usuário para fazer a recomendação: ")
            recomendacao = recomendar_musicas_por_genero(grafo, nome)
            if recomendacao != []:
                print(f"As músicas para recomendar para {nome} são: {', '.join(recomendacao)}")
            else:
                print(f"Não deu para achar nenhuma recomendação para {nome}")

        elif opcao == "a":
            grafo = carregar_grafo("forms.csv", "musicas_info.csv")
            print("Grafo criado!")
        
        elif opcao == "b":
            if grafo:
                gravar_grafo(grafo, "forms1.csv")
                print("Grafo gravado em forms1.csv.")
            else:
                print("Grafo não carregado.")
        
        elif opcao == "c":
            if grafo is not None: 
                op = input("\nVoce gostaria de adicionar uma musica ou um usuario? ")
                if op.lower() == "musica":
                    newMusica = input("\nDigite o nome da música a ser inserida: ")

                    info_musica = buscar_info_artista_por_musica(newMusica)
                    generos_mapeados = mapear_generos(info_musica.get('generos', []).split(", ")).split(", ")
                    if not verifica_duplicatas(info_musica.get('musica'), musicas): #se a musica ainda nao existe
                        musica_vertice = Musica(info_musica['musica'])
                        musicas[newMusica] = musica_vertice
                        grafo.adiciona_vertice(musica_vertice)
                    else:
                        musica_vertice = musicas[newMusica] #pega referencia do objeto
                    for genero in generos_mapeados:
                        if not verifica_duplicatas(genero, generos):
                            genero_vertice = Genero(genero)
                            generos[genero] = genero_vertice
                            grafo.adiciona_vertice(genero_vertice)
                        else:
                            genero_vertice = generos[genero]
                
                        # Conectar música ao gênero
                        grafo.insereA(musica_vertice, genero_vertice)

                elif op.lower() == "usuario":
                    newUsuario = input("\nDigite o nome do usuario a ser inserido: ")
                    usuario_vertice = Usuario(newUsuario)
                    usuarios[newUsuario] = usuario_vertice
                    grafo.adiciona_vertice(usuario_vertice.nome)
                else:
                    print("Opcao nao identificada")
            else:
                print("Grafo não carregado.")

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
                try:
                    grafo.adj.pop(v)
                except KeyError:
                    print("Vértice não encontrado")

            else:
                print("Grafo não carregado.")

        elif opcao == "f":
            if grafo:
                v = input("Digite o vértice de origem: ")
                w = input("Digite o vértice de destino: ")
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
print("FOI!")
