import smtplib
from email.mime.text import MIMEText

sender_email = "petitpatrickpetit@gmail.com"
receiver_email = "petitpatrickpetit@gmail.com"
app_password = "kcfyiqyorustrtdf"

subject = "📈 AI-BOT TESTVARSEL"
body = "Hei Patrick!\n\nDette er en test fra din AI-bot. Du er nå koblet til e-postsystemet 💼📩"

msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = sender_email
msg["To"] = receiver_email

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)
    print("✅ E-post sendt!")
except Exception as e:
    print("❌ Noe gikk galt:", e)
app_password = "LIM_INN_APP_PASSORDET_DITT_HER"
app_password = "exwmpaiwprzpacdz"
import smtplib
from email.mime.text import MIMEText

sender_email = "petitpatrickpetit@gmail.com"
receiver_email = "petitpatrickpetit@gmail.com"
app_password = "HER_LIMER_DU_INN_APP_PASSORDET"

subject = "📈 AI-BOT TESTVARSEL"
body = "Hei Patrick!\n\nDette er en test fra din egen bot.\nE-post fungerer 100% 🚀"

msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = sender_email
msg["To"] = receiver_email

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)
    print("✅ E-post sendt!")
except Exception as e:
    print("❌ Noe gikk galt:", e)

