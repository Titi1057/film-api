# ****************************************************************************
#  # Nom ......... : fast_api.py 
# Rôle ........ : Développement d'une API RESTful collaborative pour la 
#                 gestion d'un catalogue cinématographique (Exercice 3.1).
#                 Permet la consultation (GET), l'ajout (POST) et la mise à 
#                 jour (PATCH/PUT) en temps réel d'une base de données de films.
# Auteur ...... : Tchenkaeva Iman
# Version ..... : V1.2 - Version finale optimisée pour le rendu 
# Environnement : VS Code - Python 3.12+ 
# Librairies .. : FastAPI, Uvicorn, Pydantic (modélisation de données)""
# **************************************************************************** ```

# ****************************************************************************
# NOM DU PROJET : TrendMovieAPI 2026
# RÔLE ......... : Développement et Déploiement d'une API RESTful Hybride.
# VERSION ...... : V3.0 - Stable Cloud
# ****************************************************************************

from fastapi import FastAPI, HTTPException  # Cœur de l'API et gestion des erreurs
from pydantic import BaseModel              # Validation des données (Schéma)
from typing import List                     # Typage des listes pour les réponses
import streamlit as st                      # Interface de monitoring Cloud
import os                                   # Interaction avec le système

# --- 1. CONFIGURATION DE L'INTERFACE DE MONITORING (FRONTEND) ---
# Ce bloc est essentiel pour que Streamlit Cloud valide le déploiement.
st.set_page_config(page_title="TrendMovie API Monitor", page_icon="🎬")

st.title("🚀 Serveur TrendMovie API - Statut : En ligne")
st.success("L'infrastructure Cloud a validé le déploiement du service Backend.")
st.write("Le moteur **FastAPI** tourne en arrière-plan pour gérer les requêtes CRUD.")

# Lien cliquable vers la documentation
st.info("💡 **Accès Développeur** : La documentation interactive Swagger est disponible ici : [/docs](/docs)")

# --- 2. MODÈLE DE DONNÉES (Pydantic) ---
# Définit la structure d'un objet "Film" pour la validation automatique.
class Movie(BaseModel):
    id: int                 # Identifiant unique
    titre: str              # Nom du film
    realisateur: str        # Nom du réalisateur
    genre: str              # Catégorie
    score_tendance: int     # Score sur 100
    entrees_estimées: int   # Volume de spectateurs
    en_salle: bool          # État de sortie

# Initialisation de l'application FastAPI
app = FastAPI(title="TrendMovie API 2026")

# --- 3. BASE DE DONNÉES SIMULÉE (In-Memory) ---
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

# --- 4. ROUTES DE L'API (CRUD) ---

@app.get("/")
async def root():
    """Accueil de l'API."""
    return {"message": "Bienvenue sur ma Base de Données Cinématographique 2026"}

@app.get("/movies", response_model=List[Movie])
async def get_movies():
    """READ : Renvoie la liste complète des films."""
    return db_movies

@app.get("/movies/{movie_id}")
async def get_movie_by_id(movie_id: int):
    """READ : Recherche par ID."""
    for movie in db_movies:
        if movie["id"] == movie_id:
            return movie
    raise HTTPException(status_code=404, detail="Film non trouvé")

@app.post("/movies")
async def post_movie(movie: Movie):
    """CREATE : Ajout collaboratif d'un nouveau film."""
    db_movies.append(movie.dict())
    return movie

@app.put("/movies/{movie_id}")
async def update_movie(movie_id: int, movie_update: Movie):
    """UPDATE : Mise à jour des informations."""
    for index, movie in enumerate(db_movies):
        if movie["id"] == movie_id:
            db_movies[index] = movie_update.dict()
            return movie_update
    raise HTTPException(status_code=404, detail="ID introuvable")

@app.delete("/movies/{movie_id}")
async def delete_movie(movie_id: int):
    """DELETE : Suppression d'une entrée."""
    for index, movie in enumerate(db_movies):
        if movie["id"] == movie_id:
            db_movies.pop(index)
            return {"OK": True, "message": "Film supprimé"}
    raise HTTPException(status_code=404, detail="ID introuvable")