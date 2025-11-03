# Configuration du Compteur de Commandes

## ✅ Solution Simple - Variables d'Environnement

Le compteur utilise maintenant la variable d'environnement `INITIAL_ORDER_COUNT` pour persister entre les déploiements.

### Configuration sur Render

1. **Allez dans les Environment Variables de votre service backend**
2. **Ajoutez cette variable :**
   ```
   INITIAL_ORDER_COUNT=1
   ```
   (ou le nombre actuel de commandes déjà effectuées)

3. **Redéployez le service**

### Comment ça marche

- Au démarrage du backend, si `order_counter.json` n'existe pas, il est créé avec la valeur de `INITIAL_ORDER_COUNT`
- À chaque paiement réussi, le compteur s'incrémente dans le fichier JSON
- Quand vous redéployez, le fichier est perdu, mais il se recrée avec la valeur de l'env var
- **IMPORTANT** : Mettez à jour `INITIAL_ORDER_COUNT` régulièrement avec le nombre réel de commandes !

### Mise à jour du compteur

Quand vous avez de nouvelles commandes :
1. Notez le nombre total de commandes
2. Mettez à jour `INITIAL_ORDER_COUNT` dans Render
3. Pas besoin de redéployer immédiatement (ça prendra effet au prochain démarrage)

### Variables d'environnement requises

```bash
PROMO_FIRST_CUSTOMERS=100
PROMO_PRICE=1.99
REGULAR_PRICE=9.99
INITIAL_ORDER_COUNT=1  # ← Nombre actuel de commandes
```

### Vérifier le compteur

Le frontend appelle automatiquement `/api/current-price` au chargement, ce qui :
- Réveille le backend s'il est en veille
- Initialise le compteur s'il n'existe pas
- Retourne le prix et les places restantes

Pas besoin d'attendre qu'une preview soit générée !

