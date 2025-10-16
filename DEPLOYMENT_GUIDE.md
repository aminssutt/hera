# 🚀 DÉPLOIEMENT EN LIGNE - GUIDE COMPLET

## Vue d'ensemble

- **Backend** : Render.com (gratuit)
- **Frontend** : Vercel (gratuit)
- **Mode** : Stripe TEST (on teste en ligne avant de lancer)

---

## PARTIE 1 : DÉPLOYER LE BACKEND (Flask) 🐍

### Étape 1 : Créer un compte Render

1. Va sur https://render.com
2. Clique "**Get Started**"
3. Connecte-toi avec **GitHub**
4. Autorise Render à accéder à tes repos

### Étape 2 : Pousser le code sur GitHub

**Si ton code N'EST PAS encore sur GitHub :**

```powershell
cd C:\Users\k250079\Desktop\Projects\Hera
git init
git add .
git commit -m "Initial commit - Hera coloring book platform"
git branch -M main
git remote add origin https://github.com/aminssutt/hera.git
git push -u origin main
```

**Si déjà sur GitHub, mets à jour :**

```powershell
cd C:\Users\k250079\Desktop\Projects\Hera
git add .
git commit -m "Add deployment files"
git push
```

### Étape 3 : Créer le Web Service sur Render

1. Sur Render Dashboard, clique "**New +**" → "**Web Service**"
2. Connecte ton repo GitHub `aminssutt/hera`
3. Configure :
   - **Name** : `hera-backend`
   - **Region** : `Frankfurt` (Europe - plus proche)
   - **Root Directory** : `aipart`
   - **Environment** : `Python 3`
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `gunicorn generated_image:app --bind 0.0.0.0:$PORT --timeout 300`
   - **Instance Type** : `Free` ✅

4. Clique "**Advanced**" et ajoute les **Environment Variables** :

```
GOOGLE_API_KEY=your_google_api_key
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
GMAIL_EMAIL=your_email@gmail.com
GMAIL_APP_PASSWORD=your_gmail_app_password
FRONTEND_URL=https://hera.vercel.app
BACKEND_URL=https://hera-backend.onrender.com
```

**IMPORTANT:** Utilise tes vraies clés (ne copie pas ces exemples)

5. Clique "**Create Web Service**"

6. **Attends 5-10 minutes** que le déploiement se termine

7. Une fois déployé, tu auras une URL comme : `https://hera-backend.onrender.com`

---

## PARTIE 2 : DÉPLOYER LE FRONTEND (React) ⚛️

### Étape 1 : Créer un compte Vercel

1. Va sur https://vercel.com
2. Clique "**Sign Up**"
3. Connecte-toi avec **GitHub**

### Étape 2 : Mettre à jour l'URL du backend

Avant de déployer, il faut que le frontend pointe vers le backend Render :

**Ouvre `src/config.js` (ou crée-le si n'existe pas) :**

```javascript
export const BACKEND_URL = import.meta.env.PROD 
  ? 'https://hera-backend.onrender.com'
  : 'http://localhost:5000';
```

**Puis dans tous les fichiers où tu as `http://localhost:5000`, remplace par :**

```javascript
import { BACKEND_URL } from './config';

// Au lieu de:
fetch('http://localhost:5000/api/generate', ...)

// Utilise:
fetch(`${BACKEND_URL}/api/generate`, ...)
```

### Étape 3 : Déployer sur Vercel

1. Sur Vercel Dashboard, clique "**Add New**" → "**Project**"
2. Sélectionne ton repo `aminssutt/hera`
3. Configure :
   - **Framework Preset** : `Vite`
   - **Root Directory** : `./` (racine)
   - **Build Command** : `npm run build`
   - **Output Directory** : `dist`

4. Ajoute les **Environment Variables** :
   ```
   VITE_BACKEND_URL=https://hera-backend.onrender.com
   ```

5. Clique "**Deploy**"

6. **Attends 2-3 minutes**

7. Une fois déployé, tu auras une URL comme : `https://hera.vercel.app`

---

## PARTIE 3 : CONFIGURER LE WEBHOOK STRIPE 🔗

Maintenant que tout est en ligne, configure le webhook Stripe :

1. Va sur https://dashboard.stripe.com/test/webhooks
2. Clique "**Add endpoint**"
3. **Endpoint URL** : `https://hera-backend.onrender.com/api/webhook`
4. **Events** : Sélectionne `checkout.session.completed`
5. Clique "**Add endpoint**"
6. Copie le **Signing Secret** (commence par `whsec_...`)

### Ajouter le Webhook Secret sur Render :

1. Retourne sur Render Dashboard
2. Clique sur ton service `hera-backend`
3. Va dans "**Environment**"
4. Ajoute :
   ```
   STRIPE_WEBHOOK_SECRET=whsec_ton_secret_ici
   ```
5. Clique "**Save Changes**"
6. Le service va redémarrer automatiquement

---

## ✅ PARTIE 4 : TESTER LE SITE EN LIGNE

1. Va sur `https://hera.vercel.app`
2. Crée un livre :
   - Thèmes : Animals, Nature
   - Pages : **6** (pour test rapide)
   - Génère le preview
3. Clique "**Proceed to Payment**"
4. Paie avec carte test :
   ```
   Email: lakhdarberache@gmail.com
   Card: 4242 4242 4242 4242
   Exp: 12/25
   CVC: 123
   ```
5. Après paiement :
   - ✅ Email de confirmation immédiat
   - ⏳ Génération du livre (5-10 min pour 6 pages)
   - ✅ Email final avec PDF

---

## 🔍 MONITORING

### Logs du Backend (Render) :
1. Va sur Render Dashboard
2. Clique sur `hera-backend`
3. Onglet "**Logs**"
4. Tu verras en temps réel :
   - Paiements reçus
   - Génération des pages
   - Envoi d'emails

### Logs du Frontend (Vercel) :
1. Va sur Vercel Dashboard
2. Clique sur ton projet
3. Onglet "**Deployments**"
4. Clique sur le dernier déploiement
5. Tu verras les logs de build

---

## 🎯 URLS FINALES

| Service | URL | Statut |
|---------|-----|--------|
| **Frontend** | https://hera.vercel.app | Public |
| **Backend API** | https://hera-backend.onrender.com | Public |
| **Webhook** | https://hera-backend.onrender.com/api/webhook | Stripe |
| **Test Checkout** | /api/create-checkout | API |

---

## 💡 AVANTAGES DE L'HÉBERGEMENT EN LIGNE

✅ **Pas besoin de ngrok** - URLs permanentes
✅ **Accessible de partout** - Test sur mobile, tablette
✅ **Webhook toujours actif** - Pas besoin de garder PC allumé
✅ **SSL automatique** - HTTPS gratuit
✅ **Déploiement automatique** - Push sur GitHub → auto-deploy
✅ **100% GRATUIT** - Render + Vercel free plans

---

## ⚠️ LIMITES DU PLAN GRATUIT

### Render (Backend) :
- Se met en **veille après 15 min** d'inactivité
- **Premier chargement lent** (~30 sec) quand il se réveille
- 750h/mois gratuits (≈ 31 jours)

### Vercel (Frontend) :
- **Pas de limite** sur le plan gratuit
- **Toujours rapide** (CDN global)

---

## 🚀 PASSAGE EN PRODUCTION

Quand tu seras prêt à lancer pour de vrai :

1. **Change les clés Stripe** :
   - `sk_test_...` → `sk_live_...`
   - `pk_test_...` → `pk_live_...`

2. **Configure un domaine personnalisé** :
   - Frontend : `hera.work` (au lieu de hera.vercel.app)
   - Backend : `api.hera.work` (au lieu de hera-backend.onrender.com)

3. **Passe à Render paid plan** ($7/mois) :
   - Pas de veille automatique
   - Toujours rapide
   - Plus de ressources

---

## 📞 PROBLÈMES ?

### Backend ne démarre pas ?
- Vérifie les logs Render
- Vérifie que toutes les env variables sont configurées
- Vérifie requirements.txt

### Frontend erreur 404 ?
- Vérifie que VITE_BACKEND_URL est correct
- Vérifie les logs Vercel
- Vérifie que dist/ est bien généré

### Webhook pas appelé ?
- Vérifie l'URL webhook sur Stripe Dashboard
- Vérifie que le backend est bien déployé
- Vérifie les logs Render

---

Prêt à déployer ? Commence par pousser le code sur GitHub ! 🚀
