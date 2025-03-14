import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email():
    sender_email = "game.vision.udf@gmail.com"
    receiver_email = "joao.torres@vernet.com.br"
    password = "ljnv rosa drnr nwwl"
    
    subject = "Assunto do E-mail"
    body = "Este é um e-mail enviado via Python!"
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        
        # Enviar e-mail
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("E-mail enviado com sucesso!")
        
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
    finally:
        server.quit()

# Chamada da função para enviar o e-mail
send_email()