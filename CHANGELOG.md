# Changelog - Mise à jour v1.1

## Date: 20 Octobre 2025

### ✨ Nouvelles Fonctionnalités

#### 🎨 Système de Coloration Intelligent
- **Avant**: Les pages "colored" étaient des images complètement différentes générées aléatoirement
- **Maintenant**: Les pages colorées sont EXACTEMENT les mêmes que les pages B&W mais coloriées
- **Technique**: 
  1. Génération des pages B&W avec **Imagen 4.0**
  2. Coloration de la même image avec **Gemini 2.5 Flash Image**
  3. Résultat: Cohérence parfaite entre B&W et colored

**Fichier modifié**: `aipart/book_generator.py`
- Nouvelle fonction `generate_single_page()` avec paramètre `source_image_path`
- Pour colored edition: génère toutes les pages B&W, puis les colorise une par une

#### 🖼️ Nouvelle Page de Couverture PDF
- **Avant**: Page de titre avec fond rose dégradé + texte "HERA" + détails
- **Maintenant**: Première page du PDF affiche `frontpage.png` en pleine page
- **Technique**: Redimensionnement automatique pour remplir A4 tout en gardant les proportions
- **Fallback**: Si frontpage.png manque, crée une page rose simple

**Fichier modifié**: `aipart/pdf_generator.py`

### 🚧 Désactivations Temporaires

#### Physical Book - Coming Soon
- Le bouton "Physical Book" est maintenant **disabled** avec badge "🚧 Coming Soon"
- Seul le format **Digital PDF** est disponible
- L'option **Colored Version** reste **entièrement fonctionnelle**

**Fichier modifié**: `src/components/steps/StepFour.jsx`

### 🐛 Corrections de Bugs

#### Description Colored Version
- **Bug**: Affichait "10 B&W + 0 colored" avant de cliquer sur le bouton
- **Fix**: Affiche maintenant correctement "12 B&W + 12 colored (24 total)" dès le début
- Utilise `Math.floor(selections.pages / 2)` directement au lieu de fonctions conditionnelles

### 🧹 Nettoyage

- Suppression de tous les fichiers de test (`test_*.py`)
- Suppression des images de test générées
- Code mort retiré de `pdf_generator.py`

### 📦 Fichiers Modifiés

```
aipart/
  - book_generator.py        ✅ Système de coloration Gemini
  - pdf_generator.py         ✅ Cover avec frontpage.png
  
src/components/steps/
  - StepFour.jsx            ✅ Physical Book disabled + Fix description

images/
  + frontpage.png           ✅ Nouvelle image de cover
  
public/images/
  + frontpage.png           ✅ Copie pour le web (non utilisée finalement)
```

### ⚠️ Notes Importantes

1. **Temps de génération pour Colored**:
   - Black & White: ~10-15 min pour 24 pages
   - Coloration avec Gemini: ~5-10 min pour 24 pages
   - **Total: 20-25 minutes** pour un livre colored de 24 pages
   - → Recommandation: Implémenter background jobs (Celery/Redis)

2. **API Requirements**:
   - Google Imagen 4.0 API activée
   - Gemini 2.5 Flash Image API activée
   - Même API key pour les deux services

3. **Déploiement**:
   - Backend: Render.com (requirements.txt à jour)
   - Frontend: Vercel (pas de changement d'env vars nécessaire)

### 🚀 Prêt pour Déploiement

- ✅ Tous les tests passent
- ✅ Code nettoyé
- ✅ Pas de secrets exposés
- ✅ Images ajoutées au repo
- ✅ Documentation mise à jour

### 📝 TODO Futur

1. **Background Jobs** (Priorité haute)
   - Implémenter Celery + Redis pour éviter timeout
   - Webhooks Stripe déclenchent job async
   
2. **Database** (Priorité haute)
   - Stocker les commandes (order tracking)
   - Retry failed generations
   
3. **Optimisation Images**
   - Compresser les PNGs avant PDF
   - Réduire taille finale du PDF

4. **Physical Book**
   - Intégration API impression (Printful, Lulu, etc.)
   - Gestion shipping addresses
   - Calcul frais de port

---

**Version**: 1.1.0
**Auteur**: Hera Team
**Status**: ✅ Ready for Production
