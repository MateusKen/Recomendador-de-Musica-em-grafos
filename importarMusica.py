"""
NOME: Erik Samuel Viana Hsu
RA: 10403109
NOME: Mateus Kenzo Iochimoto
RA: 10400995
NOME: Thiago Shihan Cardoso Toma
RA: 10400764
"""

import os
from dotenv import load_dotenv, dotenv_values
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Carrega o .env e faz autenticação com o Spotify
load_dotenv()
auth_manager = SpotifyClientCredentials(client_id=os.getenv("client_id"), client_secret=os.getenv("client_secret"))
sp = spotipy.Spotify(auth_manager=auth_manager)

# Função para buscar informações de cada música
def buscar_info_artista_por_musica(nome_musica):
    """
    Busca informações relacionadas a uma música e seu artista no Spotify.

    Parâmetros:
    - nome_musica (str): Nome da música a ser pesquisada.

    Retorna:
    - dict: Um dicionário contendo informações padronizadas da música e do artista, incluindo:
        - "musica" (str): Nome padronizado da música.
        - "generos" (str): Gêneros associados ao artista, separados por vírgulas.

    Comportamento:
    - Realiza uma busca no Spotify usando a API para localizar a música.
    - Obtém informações detalhadas do primeiro artista relacionado à música.
    - Se a música for encontrada, retorna as informações relevantes. Caso contrário, exibe uma mensagem de erro e retorna `None`.

    Exemplo de retorno:
    ```python
    {
        "musica": "imagine",
        "generos": "rock, pop"
    }
    ```

    Exceções:
    - Certifique-se de que a conexão com a API do Spotify esteja configurada corretamente.
    - Garante que a música existe antes de tentar acessar os dados do artista.

    """
    
    # Realiza a busca no Spotify
    resultado_busca = sp.search(q=nome_musica, type='track', limit=1)
    
    if resultado_busca['tracks']['items']:
        track = resultado_busca['tracks']['items'][0]
        nome_musica = track['name'].strip().lower()  # Padroniza o nome da música
        artista = track['artists'][0]  # Pega apenas o primeiro artista
        artista_info = sp.artist(artista['id'])

        # Padronizar os gêneros do artista
        generos = ', '.join([genero.strip().lower() for genero in artista_info['genres']])

        # Informações do primeiro artista
        info_artista = {
            "musica": nome_musica,
            "generos": generos  # Convertendo lista de gêneros em string padronizada
        }

        return info_artista
    else:
        print(f"Música '{nome_musica}' não encontrada.")
        return None
