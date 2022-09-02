import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def mailing(objet, texte, destinataire, type):
    try:
        if type == "Newsletter":
            display_email = "Newsletter Chronodrone <newsletter@chronodrone.fr>"
        else:
            display_email = "Contact Chronodrone <contact@chronodrone.fr>"
        sender_email = "chronodrone.groupeb@orange.fr"
        password = "Chronodrone1"

        message = MIMEMultipart("alternative")
        message["Subject"] = objet
        message["From"] = display_email
        message["To"] = destinataire
        html = MIMEText(texte,"html")
        message.attach(html)
        # Create secure connection with server and send email
        with smtplib.SMTP_SSL("smtp.orange.fr", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, destinataire, message.as_string())
        return "okMail"
    except Exception:
        return "erreur"


