# SteganographIA

Une plateforme sécurisée qui intègre des signatures d'images uniques et résistantes à la compression lors du téléchargement. Les utilisateurs authentifiés peuvent signer des images et vérifier ultérieurement leur paternité via une fonctionnalité dédiée. Le système garantit une authentification forte, la confidentialité des données, et maintient la qualité d'image tout en permettant une identification fiable basée sur la signature intégrée.

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#-architecture)
- [Technologies](#-technologies)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [Structure du projet](#-structure-du-projet)
- [API](#-api)
- [Développement](#-développement)
- [Docker](#-docker)

## ✨ Fonctionnalités

### Authentification & Sécurité
- 🔐 Authentification par email/mot de passe sécurisée
- 🔑 Authentification OAuth avec Google
- 📧 Vérification d'email et réinitialisation de mot de passe

### Stéganographie
- 🖼️ Signature d'images avec messages cachés (LSB - Least Significant Bit)
- ✅ Vérification d'authenticité des images signées
- 📝 Extraction de messages cachés dans les images
- 🎯 Support des formats BMP, PNG, JPEG
- 💾 Historique des signatures et vérifications

### Interface Utilisateur
- 🎨 Interface moderne avec design glassmorphique
- 🌓 Mode sombre/clair
- 📱 Design responsive
- 🔍 Recherche avancée dans les signatures et vérifications
- 📊 Tableaux interactifs avec animations fluides
- 📤 Upload par glisser-déposer

## 🏗️ Architecture

Le projet suit une architecture **full-stack** avec séparation claire entre frontend et backend :

```
┌─────────────────┐
│   Frontend       │  React + Vite + Tailwind CSS
│   (Port 5173)   │
└────────┬─────────┘
         │
         │ HTTP/REST
         │
┌────────▼─────────┐
│   Backend       │  FastAPI + SQLAlchemy
│   (Port 8000)   │
└────────┬─────────┘
         │
         │ SQL
         │
┌────────▼─────────┐
│   PostgreSQL     │  Base de données
│   (Port 5432)    │
└─────────────────┘
```

## 🛠️ Technologies

### Backend
- **FastAPI** - Framework web moderne et performant
- **SQLAlchemy** - ORM pour la gestion de la base de données
- **Alembic** - Migrations de base de données
- **PostgreSQL** - Base de données relationnelle
- **Pillow** - Traitement d'images
- **Stegano** - Bibliothèque de stéganographie
- **OpenCV** - Traitement avancé d'images
- **Python-JOSE** - Gestion des tokens JWT
- **Bcrypt** - Hachage des mots de passe
- **Authlib** - Authentification OAuth

### Frontend
- **React 19** - Bibliothèque UI
- **Vite** - Build tool et dev server
- **Tailwind CSS 4** - Framework CSS utilitaire
- **React Router** - Routage côté client
- **Axios** - Client HTTP
- **Jotai** - Gestion d'état
- **React Hook Form** - Gestion de formulaires
- **Zod** - Validation de schémas

### Infrastructure
- **Docker** & **Docker Compose** - Containerisation

## 📦 Prérequis

- **Docker** >= 20.10
- **Docker Compose** >= 2.0
- **Node.js** >= 18 
- **Python** >= 3.11 
- **PostgreSQL** >= 16 

## 🚀 Installation

### Installation avec Docker (Recommandé)

1. **Cloner le repository**
```bash
git clone <repository-url>
cd steganographia
```

2. **Configurer les variables d'environnement**

Créez un fichier `.env` dans le dossier `backend/` :
```bash
cp backend/.env.example backend/.env
# Éditez backend/.env avec vos configurations
```

Variables importantes à configurer :
- `DATABASE_URL` - URL de connexion PostgreSQL
- `SECRET_KEY` - Clé secrète pour JWT
- `GOOGLE_CLIENT_ID` - ID client Google OAuth (optionnel)
- `GOOGLE_CLIENT_SECRET` - Secret client Google OAuth (optionnel)
- `SMTP_*` - Configuration email pour vérification/réinitialisation

3. **Lancer les services**
```bash
docker compose build
docker compose up -d
docker exec -it steganographia-backend-1 sh
#!/bin/sh
# migration avec alembic
set -e
if [ ! -d "./alembic" ]; then
    echo "Alembic folder not found, initializing..."
    alembic init alembic
fi
if [ -z "$(ls -A alembic/versions 2>/dev/null)" ]; then
    echo "No migrations found, generating initial migration..."
    alembic revision --autogenerate -m "initial migration"
fi
echo "Applying migrations..."
alembic upgrade head

```

Les services seront disponibles sur :
- Frontend : http://localhost:5173
- Backend API : http://localhost:8000
- API Documentation : http://localhost:8000/docs
- PostgreSQL : localhost:5432

## ⚙️ Configuration

### Variables d'environnement Backend

Fichier : `backend/.env`

```env
ENV=dev

# Database
POSTGRES_USER=stegosaurus
POSTGRES_PASSWORD=i+MHt~oG^1NLMjJ
POSTGRES_DB=steganographia

# JWT
SECRET_KEY=peace-follows-a-thorny-path
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Google OAuth
GOOGLE_CLIENT_ID=581482278150-uhcss1euvjr9jhv2voqo9vak8d9e2g22.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=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
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback
GOOGLE_OAUTH2_METADATA_URL=https://accounts.google.com/.well-known/openid-configuration

# Admin credentials
DEFAULT_ADMIN_EMAIL=admin.steganographia.mbds.2025@yopmail.com
DEFAULT_ADMIN_PASSWORD=Admin1234!

# SMTP
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=steganographia.grp2.mbds.2025@gmail.com
SMTP_PASSWORD=sfaqioarglciixxm
SMTP_FROM_NAME=SteganographIA Team

# Frontend
FRONTEND_URL=http://localhost:5173
FRONTEND_RESET_PASSWORD_URL=http://localhost:5173/reset-password/
FRONTEND_CONFIRM_EMAIL_URL=http://localhost:5173/confirm-email/

RESET_PASSWORD_EXPIRE_MINUTES=30
EMAIL_CONFIRMATION_EXPIRE_MINUTES=60
MAX_PASSWORD_RESET_REQUESTS=3

DEBUG=False
```

### Variables d'environnement Frontend

Fichier : `frontend/.env`

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

## 📖 Utilisation

### Première utilisation

1. **Accéder à l'application**
   - Ouvrez http://localhost:5173 dans votre navigateur

2. **Créer un compte**
   - Cliquez sur "S'inscrire"
   - Remplissez le formulaire
   - Vérifiez votre email (si configuré)

3. **Signer une image**
   - Allez dans "Sign Image"
   - Uploadez une image (BMP, PNG, JPEG)
   - Entrez un message à cacher
   - Cliquez sur "Signer l'image"
   - Téléchargez l'image signée

4. **Vérifier une image**
   - Allez dans "Verify Image"
   - Uploadez une image signée
   - Cliquez sur "Vérifier l'image"
   - Consultez les détails de vérification

5. **Gérer vos signatures**
   - Consultez "My Signatures" pour voir l'historique
   - Utilisez la barre de recherche pour filtrer
   - Téléchargez vos images signées

6. **Gérer vos vérifications**
   - Consultez "My Verifications" pour l'historique
   - Recherchez par UUID, statut, date ou message

## 📁 Structure du projet

```
steganographia/
├── backend/                 # Application FastAPI
│   ├── alembic/            # Migrations de base de données
│   ├── media/               # Images uploadées
│   ├── src/
│   │   ├── constants/       # Constantes et patterns
│   │   ├── controllers/     # Contrôleurs API
│   │   ├── core/            # Configuration et middleware
│   │   ├── db/              # Configuration base de données
│   │   ├── dependencies/    # Dépendances FastAPI
│   │   ├── exceptions/      # Gestion des erreurs
│   │   ├── models/          # Modèles SQLAlchemy
│   │   ├── repositories/    # Couche d'accès aux données
│   │   ├── schemas/         # Schémas Pydantic
│   │   ├── seeds/           # Données initiales
│   │   ├── services/        # Logique métier
│   │   ├── templates/       # Templates email
│   │   ├── utils/           # Utilitaires
│   │   └── main.py          # Point d'entrée
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env
│
├── frontend/                # Application React
│   ├── public/
│   ├── src/
│   │   ├── api/             # Clients API
│   │   ├── atoms/           # État global (Jotai)
│   │   ├── components/      # Composants React
│   │   ├── layouts/         # Layouts de pages
│   │   ├── pages/           # Pages de l'application
│   │   ├── schemas/         # Schémas de validation
│   │   ├── services/         # Services frontend
│   │   ├── styles/          # Styles CSS
│   │   └── utils/           # Utilitaires
│   ├── Dockerfile
│   ├── package.json
│   └── vite.config.js
│
├── docker-compose.yml       # Configuration Docker
└── README.md
```

## 🔌 API

### Documentation interactive

Une fois le backend lancé, accédez à :
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

### Endpoints principaux

#### Authentification
- `POST /api/auth/register` - Inscription
- `POST /api/auth/login` - Connexion
- `POST /api/auth/logout` - Déconnexion
- `POST /api/auth/refresh` - Rafraîchir le token
- `GET /api/auth/google` - Authentification Google
- `POST /api/auth/forgot-password` - Demande de réinitialisation
- `POST /api/auth/reset-password` - Réinitialisation du mot de passe

#### Stéganographie
- `POST /api/stego/sign` - Signer une image
- `POST /api/stego/verify` - Vérifier une image
- `GET /api/stego/signatures` - Liste des signatures
- `GET /api/stego/verifications` - Liste des vérifications

#### Utilisateurs
- `GET /api/users/me` - Informations utilisateur actuel
- `PUT /api/users/me` - Mettre à jour le profil

## 🐳 Docker

### Commandes Docker utiles

```bash
# Démarrer tous les services
docker compose up -d

# Voir les logs
docker compose logs -f

# Arrêter les services
docker compose down

# Reconstruire les images
docker compose build --no-cache

# Accéder au shell du backend
docker exec -it steganographia-backend-1 sh

# Accéder au shell du frontend
docker exec -it steganographia-frontend-1 sh
```

### Volumes Docker

Les données sont persistées dans des volumes :
- `postgres_data` - Base de données PostgreSQL
- `./backend/media` - Images uploadées (monté en volume)

## 🔒 Sécurité

- ✅ Authentification JWT sécurisée
- ✅ Hachage des mots de passe avec bcrypt

## 📝 Notes

- Les images signées conservent leur qualité visuelle
- Les signatures sont résistantes à la compression
- Le système utilise l'algorithme LSB (Least Significant Bit) pour la stéganographie
- Support des formats BMP, PNG et JPEG
