# 📧 FIX: Emails dans SPAM

## Problème
Les emails SendGrid vont dans spam car l'adresse `noreply@hera.work` n'est pas vérifiée.

## Solution Immédiate (Gratuite)

### 1. Vérifier un email SendGrid (Sender Authentication)

1. **Va sur SendGrid** : https://app.sendgrid.com/settings/sender_auth/senders
2. **Clique "Create New Sender"**
3. **Remplis avec TON email** (celui que tu contrôles) :
   ```
   From Name: Hera Coloring Books
   From Email: lakhdarberache@gmail.com  (ou ton email)
   Reply To: lakhdarberache@gmail.com
   Company Address: (ton adresse)
   ```
4. **Vérifie ton email** (SendGrid envoie un lien de confirmation)
5. **Une fois vérifié**, mets à jour `.env` sur Render :
   ```
   SENDGRID_FROM_EMAIL=lakhdarberache@gmail.com
   ```

### 2. Alternative: Utiliser Gmail SMTP (Plus fiable pour éviter spam)

Au lieu de SendGrid, tu peux utiliser Gmail directement :

**Fichier: `aipart/email_service_gmail.py`** (nouveau)
```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

GMAIL_USER = os.getenv('GMAIL_USER')  # ton.email@gmail.com
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')  # voir ci-dessous

def send_email_via_gmail(to_email, subject, html_content, attachment_path=None):
    msg = MIMEMultipart()
    msg['From'] = f"Hera Coloring Books <{GMAIL_USER}>"
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(html_content, 'html'))
    
    if attachment_path:
        with open(attachment_path, 'rb') as f:
            part = MIMEBase('application', 'pdf')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
            msg.attach(part)
    
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    server.send_message(msg)
    server.quit()
    return True
```

**Configuration Gmail App Password:**
1. Va sur https://myaccount.google.com/security
2. Active "2-Step Verification"
3. Crée un "App Password" pour "Mail"
4. Utilise ce mot de passe dans `.env` :
   ```
   GMAIL_USER=ton.email@gmail.com
   GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
   ```

## Solution Long Terme (Professionnelle)

### Acheter un domaine et configurer DNS

1. **Achète un domaine** (ex: `herabooks.com` sur Namecheap ~10$/an)
2. **Configure SendGrid Domain Authentication**
3. **Ajoute les DNS records** (CNAME, SPF, DKIM)
4. **Utilise** `noreply@herabooks.com`

Avec un domaine vérifié, les emails ne vont JAMAIS dans spam.

---

## Action Immédiate à faire MAINTENANT :

**Option 1 (Rapide):** Vérifie ton email Gmail sur SendGrid et mets à jour `SENDGRID_FROM_EMAIL`

**Option 2 (Meilleur):** Utilise Gmail SMTP directement (plus fiable, pas de spam)

Quelle option préfères-tu ?
