# 🎨 Hera AI Backend

Backend Flask pour générer des pages de coloriage avec Google Imagen API.

## 🚀 Installation

1. **Créer et activer l'environnement virtuel :**

```bash
# Depuis la racine du projet
python -m venv venv

# Activer l'environnement (Windows)
.\venv\Scripts\Activate.ps1

# Activer l'environnement (Mac/Linux)
source venv/bin/activate
```

2. **Installer les dépendances Python :**

```bash
cd aipart
pip install -r requirements.txt
```

3. **Configurer l'API Key :**

Créer un fichier `.env` dans le dossier `aipart/` :

```bash
# aipart/.env
GOOGLE_API_KEY=your_google_api_key_here
```

⚠️ **Important:** Ne jamais commiter le fichier `.env` ! Il est déjà dans `.gitignore`.

## ▶️ Lancer le Backend

```bash
cd aipart
python generated_image.py
```

Le serveur Flask démarrera sur `http://localhost:5000`

## 🔑 Obtenir une API Key

1. Aller sur [Google Cloud Console](https://console.cloud.google.com/)
2. Créer un projet ou sélectionner un projet existant
3. Activer l'API Imagen
4. Créer une API Key dans "APIs & Services" > "Credentials"
5. Copier la clé dans le fichier `.env`

## 📡 Endpoints

- `GET /api/health` - Health check
- `POST /api/generate` - Générer une image de coloriage
- `GET /api/download/<filename>` - Télécharger une image générée

## 📦 Structure

```
aipart/
├── generated_image.py    # Backend Flask
├── requirements.txt      # Dépendances Python
├── .env                  # Variables d'environnement (ignoré par git)
├── .env.example          # Exemple de configuration
├── generated_images/     # Images générées (créé auto)
└── README.md             # Cette documentation
```

## 🔄 Workflow

1. Frontend React envoie les sélections (theme, topic, difficulty) à `/api/generate`
2. Backend construit un prompt optimisé pour des pages de coloriage enfants
3. Google Imagen génère l'image
4. Image retournée en base64 + sauvegardée localement
5. Frontend affiche l'image et permet le paiement

## 🛠️ Technologies

- **Flask** - Web server
- **Flask-CORS** - Cross-origin support
- **Google Genai** - Imagen 4.0 API
- **Pillow** - Image processing
- **Python-dotenv** - Environment variables management

## ⚠️ Notes

- Le backend doit tourner en parallèle avec le frontend React (port 3000)
- CORS est activé pour accepter les requêtes depuis localhost:3000
- Les images sont sauvegardées dans `generated_images/`
- Le fichier `.env` contient des informations sensibles et ne doit JAMAIS être commité
