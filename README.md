# Recomendador de Músicas com Grafos

Sistema de recomendação de músicas que modela usuários e músicas como um grafo e sugere faixas novas a partir das conexões entre eles. Os dados das músicas vêm da API do Spotify.

[Vídeo de apresentação](https://www.youtube.com/watch?v=VrdUdeRjdpg)

Este é um projeto desenvolvido para a disciplina de Teoria dos Grafos com o objetivo de explorar a utilização de grafos na criação de um sistema de recomendação de músicas.

📝 **Descrição do Projeto**

O sistema utiliza um grafo  que conecta usuários a músicas com base em interações ou preferências. A partir da análise das conexões existentes, o algoritmo recomenda músicas novas para os usuários, priorizando aquelas que possuem maior similaridade com seus gostos.

🚀 **Funcionalidades**

	•	Inserção de dados: Adicionar novos usuários e músicas ao grafo.
	•	Recomendações personalizadas: Geração de recomendações com base nas conexões do grafo.
	•	Visualização do grafo: Exibição das relações usuário-música em formato gráfico ou textual.
	•	Leitura de grafo a partir de arquivo csv.
 	•	Verificação de conexidade do grafo.
  

🛠️ **Tecnologias Utilizadas**

	•	Linguagem de programação: Python
	•	Estrutura de dados: Grafo (representado por listas de adjacência adjacência)	
	•	Bibliotecas (Python):
		-	Spotipy: biblioteca do python especializada para realizar as chamadas na API do Spotify
		-	Pandas: biblioteca python para criar dataframes, utilizada nesse projeto para exportar as respostas do formulário, manipular os dados e criar o csv do projeto
		-	csv: biblioteca python para manipulação de arquivos csv
		-	collections: biblioteca nativa python com funções prontas
		-	os: biblioteca python que realiza syscalls
		-	dotenv: biblioteca python para usar arquivos .env
  
	•	Spotify API: para fazer chamadas e buscar informações sobre as músicas
	•	CSV: tipo de arquivo que vai ser usado para armazenar os dados do projeto







Para acessar a API do Spotify é necessário acessar: https://developer.spotify.com
Fazer o login, criar um projeto e pegar o id e o secret
Depois de ter isso criado só precisa criar um .env na pasta

para instalar as dependências do projeto, baixe o arquivo "requirements.txt" e use o comando

**pip install -r requirements.txt**

## Autores

Erik Samuel Viana Hsu, Mateus Kenzo Iochimoto e Thiago Shihan Cardoso Toma.
Projeto final de Teoria dos Grafos, Ciência da Computação, Universidade Presbiteriana Mackenzie.
