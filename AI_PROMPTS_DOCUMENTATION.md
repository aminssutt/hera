# 🎨 Prompts AI - Hera Coloring Books

## 📋 Vue d'ensemble

Hera utilise 2 types de prompts :
1. **Imagen 4.0** : Génération des pages noir & blanc (line art)
2. **Gemini 2.5 Flash Image** : Coloration des pages noir & blanc

---

## 🖤 Prompt #1 : Génération Pages Noir & Blanc (Imagen 4.0)

### Template du Prompt :
```
Create a black and white coloring book page for children.
Theme: {theme}. Art style: {style_desc}. Complexity: {difficulty_desc}.
IMPORTANT: The image MUST be black and white line art ONLY - clean outlines, no shading, no grayscale.
Perfect for coloring with crayons or markers. High contrast, clear lines, child-friendly design.
CRITICAL: NO TEXT, NO WORDS, NO LETTERS, NO NUMBERS - only pure line art illustrations.
```

### Variables :
- **{theme}** : Thème choisi (ex: "Animals", "Space", "Dinosaurs")
- **{style_desc}** : Style artistique parmi :
  - `Ghibli` → "Studio Ghibli inspired, whimsical and magical"
  - `Cartoon` → "fun cartoon style with bold outlines"
  - `Minimal` → "minimalist clean line art style"
  - `Comic` → "comic book style with dynamic compositions"
  - `Detailed` → "highly detailed and intricate patterns"
  - `Magical` → "magical and fantastical with sparkles and stars"

- **{difficulty_desc}** : Niveau de complexité :
  - `Easy` → "simple, large shapes with minimal details, perfect for young children"
  - `Medium` → "moderate details with medium complexity, suitable for kids 6-10"
  - `Hard` → "intricate details and complex patterns, challenging for older kids"

### Exemple Concret :
```
Create a black and white coloring book page for children.
Theme: Animals and Space. Art style: fun cartoon style with bold outlines. Complexity: simple, large shapes with minimal details, perfect for young children.
IMPORTANT: The image MUST be black and white line art ONLY - clean outlines, no shading, no grayscale.
Perfect for coloring with crayons or markers. High contrast, clear lines, child-friendly design.
CRITICAL: NO TEXT, NO WORDS, NO LETTERS, NO NUMBERS - only pure line art illustrations.
```

### Configuration Imagen :
```python
aspect_ratio='3:4'  # Portrait 768x1024 - parfait pour A4
output_mime_type='image/png'
safety_filter_level='BLOCK_LOW_AND_ABOVE'
person_generation='ALLOW_ADULT'
```

---

## 🌈 Prompt #2 : Coloration (Gemini 2.5 Flash Image)

### Template du Prompt :
```
Color in this black and white coloring book illustration neatly using the following colors: {color_list}.
Do not change the line art. Stay within the lines. Use flat, solid colors without shading or texture.
Make it bright, fun, and perfect for kids!
```

### Variables :
- **{color_list}** : Liste des couleurs hex sélectionnées par l'utilisateur
  - Exemple : "#FF6B6B, #5EB3E4, #FFD93D, #7B68EE"
  - Si aucune couleur sélectionnée : "vibrant child-friendly colors"

### Exemple Concret :
```
Color in this black and white coloring book illustration neatly using the following colors: #FF6B6B, #5EB3E4, #FFD93D, #4ECDC4, #FF6F91.
Do not change the line art. Stay within the lines. Use flat, solid colors without shading or texture.
Make it bright, fun, and perfect for kids!
```

### Input :
- Image noir & blanc générée par Imagen (PNG)
- Prompt de coloration
- Modèle : `gemini-2.5-flash-image`

---

## 🎯 Stratégie de Prompting

### ✅ Points Forts :
1. **Clarté** : Instructions explicites et précises
2. **Contraintes** : "NO TEXT", "black and white ONLY", "Stay within lines"
3. **Contexte** : "for children", "coloring book", "fun"
4. **Format** : Aspect ratio 3:4 pour A4

### 📈 Améliorations Possibles :
1. **Ajout de variations** : "Create DIFFERENT illustrations on theme X"
2. **Cohérence** : "In the same style as previous pages"
3. **Détails** : Plus de guidance sur la composition

---

## 🔄 Workflow Complet

### Pour Livre Noir & Blanc (10 pages) :
```
Étape 1 : Génération avec Imagen
  ↓
  Prompt B&W → Image 1.png
  Prompt B&W → Image 2.png
  ...
  Prompt B&W → Image 10.png
  ↓
  Total : 10 appels Imagen
```

### Pour Livre Coloré (10 pages = 5 B&W + 5 Colored) :
```
Étape 1 : Génération B&W avec Imagen
  ↓
  Prompt B&W → Image 1.png
  Prompt B&W → Image 2.png
  ...
  Prompt B&W → Image 5.png
  ↓
Étape 2 : Coloration avec Gemini
  ↓
  Image 1.png + Prompt Color → Image 1_colored.png
  Image 2.png + Prompt Color → Image 2_colored.png
  ...
  Image 5.png + Prompt Color → Image 5_colored.png
  ↓
  Total : 5 appels Imagen + 5 appels Gemini
```

---

## 📊 Quotas et Coûts

### Imagen 4.0 :
- **Quota gratuit** : 70 images/jour (tier 1 payant)
- **Utilisation** : Génération des pages B&W uniquement
- **Format** : 768x1024 (portrait 3:4)

### Gemini 2.5 Flash Image :
- **Quota** : Plus généreux que Imagen
- **Utilisation** : Coloration des pages B&W
- **Avantage** : Garde le line art intact

### Optimisation :
- Livre B&W = moins cher (Imagen seulement)
- Livre Coloré = utilise les 2 APIs
- Économie quota : Limiter pages de test à 2-4

---

## 🎨 Palettes de Couleurs Disponibles

L'utilisateur peut choisir parmi **4 palettes de 7 couleurs** :

### 🔥 Warm Colors :
`#FF6B6B, #FF8E3C, #FFA500, #FFD93D, #FF6F91, #FF9AA2, #FFB347`

### ❄️ Cold Colors :
`#4A90E2, #5EB3E4, #00D4FF, #4ECDC4, #7B68EE, #6A5ACD, #20B2AA`

### 🌸 Pastel Colors :
`#FFB6C1, #E0BBE4, #B4E7CE, #FFE4E1, #FFDFD3, #C7CEEA, #FFF5BA`

### 🖤 Natural & Neutral Colors :
`#2C2C2C, #5A5A5A, #8B8B8B, #A0826D, #8B4513, #D2B48C, #F5F5DC`

Ces couleurs sont ensuite injectées dans le prompt de coloration Gemini.

---

## 🚀 Résumé Technique

| Élément | Valeur |
|---------|--------|
| **Modèle B&W** | Imagen 4.0 Generate |
| **Modèle Color** | Gemini 2.5 Flash Image |
| **Résolution** | 768x1024 (3:4) |
| **Format Output** | PNG |
| **Contrainte Clé** | NO TEXT, B&W line art only |
| **Personnalisation** | Theme, Style, Difficulty, Colors |
| **Quota Quotidien** | 70 images Imagen/jour |

---

**Dernière mise à jour** : 22 octobre 2025
