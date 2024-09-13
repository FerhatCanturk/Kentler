import smtplib
from flask import current_app
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def MailGonderme(AliciAdresi, Baslik, Konu):
    return True
    SiteOwner  = current_app.config.get('BaseSabitler', {})
    smtp_server = SiteOwner.get('SmtpHost', 'smtp.gmail.com')
    smtp_port = SiteOwner.get('Port', '587')
    sender_email = SiteOwner.get('AdminMail', 'frhtcntrk@gmail.com')
    sender_password = SiteOwner.get('SENDER_PASSWORD', 'smtp.gmail.com')   
    

    # Başlık oluşturma
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = AliciAdresi.strip()
    msg['Subject'] = Baslik

    # E-posta gövdesi oluşturma
    body = Konu
    msg.attach(MIMEText(body, 'plain'))  # Gövdeyi eklemek

    Durum = True

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # TLS bağlantısı başlatma (Gmail için gerekli)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, AliciAdresi, msg.as_string())
    except smtplib.SMTPException as e:
        Durum = True
    except Exception as e:
        Durum = True
    finally:
        if server:
            # Bağlantıyı kapatma
            server.quit()
    return Durum

    


