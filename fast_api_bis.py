# **************************************************************************** # NOM DU PROJET : TrendMovieAPI - Plateforme Cinématographique Collaborative. 
# NOM DU FICHIER : fast_api_bis.py  
# RÔLE ......... : Développement et Déploiement d'une API RESTful (Exercice 3.1). 
#                  Permet la gestion complète (CRUD) d'un catalogue de films  
#                  via une infrastructure Cloud (GitHub + Streamlit Cloud). 
# FONCTIONNALITÉS : 
# - Consultation globale et filtrée (GET)  
# - Ajout collaboratif de nouveaux titres (POST)  
# - Mise à jour et correction de données (PUT/PATCH)  
# - Suppression d'entrées (DELETE) 
# 
# VERSION ...... : V2.0 - Version finale optimisée pour le rendu   
# ENVIRONNEMENT : VS Code - Python 3.12+, FastAPI, Uvicorn, Streamlit, GitHub Ecosystem   
# URL DÉPÔT .... : https://github.com/Titi1057/film-api 
# **************************************************************************** from fastapi import FastAPI, HTTPException  # FastAPI pour l'API, HTTPException pour les erreurs (404, etc.)  
from pydantic import BaseModel              # Pour définir le schéma des données (Data Validation)  
from typing import List                     # Pour définir des listes typées dans les réponses  
import streamlit as st                      # Pour créer des interfaces utilisateur (UI) web 
import uvicorn                              # Le serveur web asynchrone (ASGI) pour faire tourner FastAPI 
import os                                   # Le module natif de Python pour interagir avec l'OS 

# 1. PARTIE STREAMLIT (Ce que le Cloud voit en premier)  
st.set_page_config(page_title="TrendMovie API", page_icon="🎥")  
st.title(" Serveur TrendMovie API")  
st.success("L'infrastructure est opérationnelle !")  
st.write("Le backend FastAPI tourne en arrière-plan.")  
st.info(" [Accéder à la Documentation API (/docs)](/docs)")  

# 1. --- MODÈLE DE DONNÉES (Pydantic) ---  
# Ce modèle définit la structure d'un objet "Film".   
# FastAPI l'utilise pour vérifier que les données envoyées par les utilisateurs sont correctes.  
class Movie(BaseModel):  
    id: int                 # Identifiant unique (ex: 1)  
    titre: str              # Chaîne de caractères  
    realisateur: str        # Chaîne de caractères  
    genre: str              # Chaîne de caractères  
    score_tendance: int     # Entier (utilisé pour le tri de popularité)  
    entrees_estimées: int   # Nombre de spectateurs prévus  
    en_salle: bool          # Booléen (True si le film est déjà sorti)  

# Initialisation de l'application FastAPI  
# C'est l'objet "app" qui recevra toutes les requêtes HTTP.  
app = FastAPI(title="TrendMovieAPI 2026")  

# 2. --- BASE DE DONNÉES SIMULÉE ---  
# Utilisation d'une liste Python (In-Memory Storage) pour stocker nos 20 films.  
# Conformément à la consigne : "un jeu de données à consulter et partager".  
db_movies = [  
    {"id": 1, "titre": "Avengers: Doomsday", "realisateur": "Russo Brothers", "genre": "Action", "score_tendance": 98, "entrees_estimées": 5000000, "en_salle": False},  
    {"id": 2, "titre": "Dune: Part Three", "realisateur": "Denis Villeneuve", "genre": "SF", "score_tendance": 95, "entrees_estimées": 3200000, "en_salle": False},  
    {"id": 3, "titre": "Marsupilami", "realisateur": "Philippe Lacheau", "genre": "Comédie", "score_tendance": 88, "entrees_estimées": 3825975, "en_salle": True},  
    {"id": 4, "titre": "Mickey 17", "realisateur": "Bong Joon-ho", "genre": "SF", "score_tendance": 82, "entrees_estimées": 1200000, "en_salle": True},  
    {"id": 5, "titre": "Avatar: Fire and Ash", "realisateur": "James Cameron", "genre": "Aventure", "score_tendance": 97, "entrees_estimées": 0, "en_salle": False},  
    {"id": 6, "titre": "Beyond the Spider-Verse", "realisateur": "Joaquim Dos Santos", "genre": "Animation", "score_tendance": 94, "entrees_estimées": 0, "en_salle": False},  
    {"id": 7, "titre": "The Batman Part II", "realisateur": "Matt Reeves", "genre": "Polar", "score_tendance": 91, "entrees_estimées": 0, "en_salle": False},  
    {"id": 8, "titre": "L'IA qui m'aimait", "realisateur": "Cédric Klapisch", "genre": "Romance", "score_tendance": 65, "entrees_estimées": 450000, "en_salle": True},  
    {"id": 9, "titre": "Super-Soldat 2026", "realisateur": "Michael Bay", "genre": "Action", "score_tendance": 70, "entrees_estimées": 800000, "en_salle": True},  
    {"id": 10, "titre": "Toy Story 5", "realisateur": "Andrew Stanton", "genre": "Animation", "score_tendance": 89, "entrees_estimées": 0, "en_salle": False},  
    {"id": 11, "titre": "Gladiator III", "realisateur": "Ridley Scott", "genre": "Historique", "score_tendance": 78, "entrees_estimées": 0, "en_salle": False},  
    {"id": 12, "titre": "Star Wars: New Order", "realisateur": "Sharmeen Obaid-Chinoy", "genre": "SF", "score_tendance": 75, "entrees_estimées": 0, "en_salle": False},  
    {"id": 13, "titre": "Shrek 5", "realisateur": "Walt Dohrn", "genre": "Animation", "score_tendance": 93, "entrees_estimées": 0, "en_salle": False},  
    {"id": 14, "titre": "Inception 2", "realisateur": "Christopher Nolan", "genre": "Thriller", "score_tendance": 85, "entrees_estimées": 0, "en_salle": False},  
    {"id": 15, "titre": "Zootopie 2", "realisateur": "Jared Bush", "genre": "Animation", "score_tendance": 87, "entrees_estimées": 0, "en_salle": False},  
    {"id": 16, "titre": "Fast & Furious 12", "realisateur": "Justin Lin", "genre": "Action", "score_tendance": 60, "entrees_estimées": 1500000, "en_salle": True},  
    {"id": 17, "titre": "The Legend of Zelda", "realisateur": "Wes Ball", "genre": "Fantasy", "score_tendance": 96, "entrees_estimées": 0, "en_salle": False},  
    {"id": 18, "titre": "Metroid Prime", "realisateur": "Brie Larson", "genre": "SF", "score_tendance": 84, "entrees_estimées": 0, "en_salle": False},  
    {"id": 19, "titre": "Sherlock Holmes 3", "realisateur": "Dexter Fletcher", "genre": "Mystère", "score_tendance": 79, "entrees_estimées": 0, "en_salle": False},  
    {"id": 20, "titre": "Blade", "realisateur": "Yann Demange", "genre": "Horreur", "score_tendance": 81, "entrees_estimées": 0, "en_salle": False}  
]  

# --- 3. ROUTES DE L'API (Méthodes HTTP / CRUD) ---  

# Route racine : Message de bienvenue  
@app.get("/")  
async def root():  
    """Point d'entrée principal de l'API."""  
    return {"message": "Bienvenue sur ma Base de Données Cinématographique 2026"}  

# Opération READ (Tout lire)  
@app.get("/movies")  
async def get_movies():  
    """Renvoie la liste complète des films partagés."""  
    return db_movies  

# Opération READ (Lire un élément spécifique)  
@app.get("/movies/{movie_id}")  
async def get_movie_by_id(movie_id: int):  
    """Recherche un film par son ID. Renvoie une erreur 404 si non trouvé."""  
    for movie in db_movies:  
        if movie["id"] == movie_id:  
            return movie  
    # Si la boucle finit sans trouver l'ID, on lève une exception  
    raise HTTPException(status_code=404, detail=f"Aucun film avec l'identifiant {movie_id} trouvé")  

# Opération CREATE (Ajouter un film)  
@app.post("/movies")  
async def post_movie(movie: Movie):  
    """Ajoute un nouveau film à la base de données commune."""  
    db_movies.append(movie.dict()) # On transforme l'objet Pydantic en dictionnaire pour le stockage  
    return movie  

# Opération UPDATE (Mettre à jour un film)  
@app.put("/movies/{movie_id}")  
async def update_movie(movie_id: int, movie_update: Movie):  
    """Met à jour les informations d'un film existant via son ID."""  
    for index, movie in enumerate(db_movies):  
        if movie["id"] == movie_id:  
            # Remplacement de l'ancien dictionnaire par le nouveau  
            db_movies[index] = movie_update.dict()  
            return movie_update  
    raise HTTPException(status_code=404, detail=f"Aucun film avec l'identifiant {movie_id} trouvé")  

# Opération DELETE (Supprimer un film)  
@app.delete("/movies/{movie_id}")  
async def delete_movie(movie_id: int):  
    """Supprime un film de la base partagée."""  
    for index, movie in enumerate(db_movies):  
        if movie["id"] == movie_id:  
            db_movies.pop(index) # Supprime l'élément à l'index trouvé  
            return {"OK": True} # Confirmation de suppression  
    raise HTTPException(status_code=404, detail=f"Aucun film avec l'identifiant {movie_id} n'existe")