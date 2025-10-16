# 📧 Configuration Gmail SMTP - GRATUIT (500 emails/jour)

## Pourquoi Gmail au lieu de Resend ?
- ✅ **100% GRATUIT** jusqu'à 500 emails/jour
- ✅ Pas besoin de vérifier un domaine
- ✅ Peut envoyer à n'importe qui
- ✅ Parfait pour démarrer ton business

---

## 🔧 Étape 1 : Activer l'authentification à 2 facteurs

1. Va sur https://myaccount.google.com/security
2. Cherche "**Validation en deux étapes**" (2-Step Verification)
3. **Active-la** (obligatoire pour les App Passwords)

---

## 🔑 Étape 2 : Créer un App Password Gmail

1. Va sur https://myaccount.google.com/apppasswords
2. Connecte-toi si nécessaire
3. Dans "**Sélectionner l'application**" → Choisis "**Autre (nom personnalisé)**"
4. Tape : `Hera Coloring Book`
5. Clique sur "**Générer**"
6. Gmail va afficher un **mot de passe de 16 caractères** comme : `abcd efgh ijkl mnop`
7. **COPIE CE MOT DE PASSE** (tu ne le reverras plus !)

---

## 📝 Étape 3 : Configurer le fichier .env

Ouvre le fichier `.env` et remplace :

```env
# Gmail SMTP Configuration
GMAIL_EMAIL=hera.work.noreply@gmail.com
GMAIL_APP_PASSWORD=abcdefghijklmnop    # ← Colle le mot de passe de 16 caractères (sans espaces)
```

**IMPORTANT :** 
- Utilise le **App Password** (16 caractères), PAS ton mot de passe Gmail normal !
- Enlève tous les espaces du mot de passe : `abcd efgh ijkl mnop` → `abcdefghijklmnop`

---

## ✅ Étape 4 : Tester l'envoi d'email

Une fois configuré, teste avec :

```powershell
cd aipart
python test_email_gmail.py
```

Tu devrais recevoir un email de test sur `lakhdarberache@gmail.com` !

---

## 🚀 Avantages de Gmail SMTP

| Feature | Gmail SMTP | Resend (Free) |
|---------|-----------|---------------|
| **Prix** | 100% GRATUIT | 100 emails/mois |
| **Limite** | 500 emails/jour | 100 emails/mois |
| **Domaine requis** | ❌ Non | ✅ Oui (pour prod) |
| **Envoi vers** | N'importe qui | Ton email seulement |
| **Configuration** | 5 minutes | Complexe (DNS) |

---

## ⚠️ Limites de Gmail

- **500 emails par jour maximum**
- Si tu dépasses → ton compte est temporairement bloqué (24h)
- Pour + de 500/jour → utilise un service payant (SendGrid, Mailgun, etc.)

---

## 📊 Estimation pour ton business

**Exemple :** 10 ventes/jour
- 10 clients × 2 emails (confirmation + PDF) = **20 emails/jour**
- **600 emails/mois**
- Coût avec Gmail : **GRATUIT ✅**

**Limite :** Jusqu'à 250 clients/jour (500 emails ÷ 2)

---

## 🔒 Sécurité

✅ L'App Password est distinct de ton mot de passe Gmail principal
✅ Tu peux le révoquer à tout moment sur https://myaccount.google.com/apppasswords
✅ Personne ne peut accéder à ton Gmail avec ce mot de passe (juste envoyer des emails)

---

## 📞 Problèmes courants

### "Error: Username and Password not accepted"
→ Vérifie que tu as :
1. Activé la validation en 2 étapes
2. Utilisé un **App Password** (pas ton mot de passe Gmail)
3. Copié le mot de passe SANS espaces

### "Error: SMTP AUTH extension not supported"
→ Ton entreprise/école bloque Gmail SMTP. Utilise un autre email ou Resend.

### "Error: Daily sending quota exceeded"
→ Tu as dépassé 500 emails/jour. Attends 24h ou passe à un service payant.

---

## 🎯 Prochaines étapes

1. ✅ Active la validation en 2 étapes sur Gmail
2. ✅ Crée un App Password
3. ✅ Configure le `.env` avec le mot de passe
4. ✅ Teste avec `python test_email_gmail.py`
5. 🚀 Lance ton business !

---

**Questions ?** Tout est expliqué ici : https://support.google.com/accounts/answer/185833
