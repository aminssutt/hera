# 🚀 GUIDE DE REDÉPLOIEMENT - Version 1.1

## ✅ Checklist Pré-Déploiement

- [x] Code pushé sur GitHub (commit `9a2ee79`)
- [x] Fichiers de test supprimés
- [x] `.env` non commité (vérifié)
- [x] CHANGELOG.md créé
- [x] Tous les tests locaux passent

---

## 📦 PARTIE 1: Backend (Render)

### 1.1 Vérifier que Render détecte le nouveau commit

1. Va sur https://dashboard.render.com
2. Clique sur ton service `hera-backend`
3. Vérifie que le dernier déploiement se lance automatiquement
4. **Si pas de déploiement automatique**: Clique "Manual Deploy" → "Deploy latest commit"

### 1.2 Vérifier les variables d'environnement

Dans Render Dashboard → `hera-backend` → Environment:

```
GOOGLE_API_KEY=***REMOVED***
STRIPE_SECRET_KEY=sk_test_51SInnSB68Jrin23z...
STRIPE_PUBLISHABLE_KEY=pk_test_51SInnSB68Jrin23z...
SENDGRID_API_KEY=SG.tx7S5kOMTFq09moxsc3agw...
SENDGRID_FROM_EMAIL=noreply@hera.work
FRONTEND_URL=https://ton-app.vercel.app
BACKEND_URL=https://hera-backend.onrender.com
```

⚠️ **IMPORTANT**: Vérifie que `GOOGLE_API_KEY` a accès à **Gemini 2.5 Flash Image** en plus d'Imagen 4.0

### 1.3 Surveiller les logs de déploiement

```
==> Building...
==> Installing dependencies from requirements.txt
==> Starting server with gunicorn
```

**Durée estimée**: 3-5 minutes

### 1.4 Tester le backend

```bash
# Health check
curl https://hera-backend.onrender.com/api/health

# Devrait retourner:
{"status":"ok","message":"Hera AI Backend is running"}
```

---

## 🌐 PARTIE 2: Frontend (Vercel)

### 2.1 Vérifier le déploiement automatique

1. Va sur https://vercel.com/dashboard
2. Ton projet `hera` devrait auto-déployer dès le push GitHub
3. Attends que le statut passe à "Ready" (⚡)

**Durée estimée**: 1-2 minutes

### 2.2 Vérifier les variables d'environnement

Dans Vercel → Project Settings → Environment Variables:

```
VITE_BACKEND_URL=https://hera-backend.onrender.com
```

### 2.3 Si pas de déploiement auto

1. Dans Vercel Dashboard → Deployments
2. Clique "Redeploy" sur le dernier déploiement
3. OU clique "Import Git Repository" et reconnecte

---

## 🧪 PARTIE 3: Tests de Validation

### 3.1 Test Frontend

1. **Page d'accueil**: https://ton-app.vercel.app
   - ✅ Titre "Hēra" visible
   - ✅ Animations fonctionnent
   - ✅ Bouton "Create Your Book"

2. **Flow de création** (clic sur "Create Your Book"):
   - ✅ Step 1: Sélectionner 2 thèmes (ex: Animals, Nature)
   - ✅ Step 2: Choisir style (ex: Cartoon)
   - ✅ Step 3: Ajuster pages (ex: 10), difficulté (Easy)
   - ✅ Step 4: Clic "Generate Preview"

3. **Preview Generation**:
   - ⏰ Attendre 10-30 secondes
   - ✅ Image de preview s'affiche
   - ✅ Options de format visibles:
     - Digital PDF: $9.99 ✅
     - Physical Book: DISABLED avec "🚧 Coming Soon" ✅
   - ✅ Options de type:
     - Black & White Only ✅
     - Colored Version: "5 B&W + 5 colored (10 total)" ✅

### 3.2 Test Payment Flow (OPTIONNEL - coûte des crédits AI)

⚠️ **ATTENTION**: Ceci générera un vrai livre et consommera des crédits API Google

1. Sélectionner "Digital PDF" + "Black & White Only"
2. Clic "Proceed to Payment"
3. Page Stripe Checkout s'ouvre
4. Utiliser carte test: `4242 4242 4242 4242`, Exp: `12/25`, CVC: `123`
5. ✅ Redirection vers `/success`
6. ⏰ Attendre 15-30 minutes (génération + email)
7. ✅ Email reçu avec PDF attaché
8. ✅ PDF a frontpage.png comme première page

### 3.3 Test Colored Version (OPTIONNEL - très coûteux)

⚠️ **COÛT ÉLEVÉ**: 2x plus de crédits (génération + coloration)

1. Choisir "Colored Version" avec 6 pages (minimum pour tester)
2. Procéder au paiement
3. ⏰ Attendre 30-45 minutes
4. ✅ PDF contient:
   - Page 1: frontpage.png (cover)
   - Pages 2-7: 3 B&W
   - Pages 8-13: 3 colored (MÊME images que les B&W mais en couleur)

---

## 🐛 Troubleshooting

### Erreur: "Failed to generate image"

**Cause**: API Google Imagen/Gemini pas accessible
**Solutions**:
1. Vérifier que `GOOGLE_API_KEY` est correcte dans Render
2. Vérifier billing activé sur Google Cloud Console
3. Vérifier quota API pas dépassé
4. Logs Render: `API Error: ...` donnera le détail

### Erreur: "Email failed"

**Cause**: SendGrid API issue
**Solutions**:
1. Vérifier `SENDGRID_API_KEY` dans Render
2. Vérifier sender email `noreply@hera.work` est vérifié dans SendGrid
3. PDF sera quand même généré et sauvegardé côté serveur

### Erreur: Webhook timeout

**Cause**: Génération de livre trop longue (>30 min)
**Solution temporaire**: 
1. Réduire nombre de pages à 10 max pour les tests
2. **Solution permanente**: Implémenter background jobs (Celery)

### Images frontpage.png manquantes dans PDF

**Cause**: Image pas déployée ou path incorrect
**Vérifications**:
1. `images/frontpage.png` existe dans le repo GitHub ✅
2. Render a bien pull les changements ✅
3. Logs backend: chercher "Using frontpage.png as cover" ou "Warning: frontpage.png not found"

---

## 📊 Monitoring Post-Déploiement

### Logs à surveiller (Render)

```bash
# Succès de génération
✅ Using frontpage.png as cover: /opt/render/project/src/images/frontpage.png
✅ Image générée avec succès!
🌈 Step 2: Coloring the same X pages with Gemini...
✅ PDF créé avec succès
✅ Email sent successfully!
```

### Métriques à vérifier

- **Temps moyen de génération**: 
  - B&W only (10 pages): ~5-10 min ✅
  - Colored (10 pages): ~15-25 min ⚠️ (peut timeout)
  
- **Taux de succès email**: 
  - Doit être >95% (SendGrid gratuit = 100 emails/jour)
  
- **Taux d'erreur API**: 
  - Imagen: <5%
  - Gemini coloring: <10% (nouveau, peut être instable)

---

## ✅ Validation Finale

Après déploiement, remplis cette checklist:

- [ ] Backend démarre sans erreur (Render logs)
- [ ] Frontend accessible (Vercel deployment successful)
- [ ] Page d'accueil charge correctement
- [ ] Preview generation fonctionne (1 image test)
- [ ] Physical Book est bien disabled
- [ ] Colored version description affiche "X B&W + X colored"
- [ ] Payment Stripe redirige correctement
- [ ] (Optionnel) PDF généré avec frontpage.png comme cover
- [ ] (Optionnel) Email reçu avec PDF

---

## 🎉 Si Tout Fonctionne

**FÉLICITATIONS !** 🚀 Ton application Hera v1.1 est en production !

**Prochaines étapes recommandées**:

1. **Surveiller les premiers utilisateurs réels**
   - Combien de previews générés?
   - Combien de paiements complétés?
   - Temps de génération moyen?

2. **Implémenter background jobs** (urgent si >10 pages)
   - Celery + Redis
   - Éviter timeout webhooks

3. **Ajouter analytics**
   - Google Analytics
   - Stripe Dashboard pour conversions

4. **Monitoring uptime**
   - UptimeRobot (gratuit)
   - Alertes si backend down

---

**Version**: 1.1.0  
**Date**: 20 Octobre 2025  
**Commit**: `9a2ee79`  
**Status**: 🟢 Ready for Production
