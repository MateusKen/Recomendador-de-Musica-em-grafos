import os
from dotenv import load_dotenv, dotenv_values
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()
# Autenticação


# Autenticação com o Spotify
auth_manager = SpotifyClientCredentials(client_id=os.getenv("client_id"), client_secret=os.getenv("client_secret"))
sp = spotipy.Spotify(auth_manager=auth_manager)

# Função para buscar informações de cada música
def buscar_info_artista_por_musica(nome_musica):
    resultado_busca = sp.search(q=nome_musica, type='track', limit=1)
    
    if resultado_busca['tracks']['items']:
        track = resultado_busca['tracks']['items'][0]
        nome_musica = track['name']
        artista = track['artists'][0]  # Pega apenas o primeiro artista

        artista_nome = artista['name']
        artista_info = sp.artist(artista['id'])

        # Informações do primeiro artista
        info_artista = {
            "musica": nome_musica,
            "artista": artista_nome,
            #"seguidores": artista_info['followers']['total'],
            #"popularidade": artista_info['popularity'],
            "generos": ', '.join(artista_info['genres']),  # Convertendo lista de gêneros em string
            #"url_spotify": artista_info['external_urls']['spotify'],
            "aparicoes": 1  # Coluna 'aparicoes' criada e inicializada como 1
        }

        return info_artista
    else:
        print(f"Música '{nome_musica}' não encontrada.")
        return None