import imaplib
import email
import time
import requests

# === CONFIG ===
EMAIL = "fittrader007@gmail.com"
PASSWORD = "gsdq cuho kfxw tlgy"  # App Password
IMAP_URL = "imap.gmail.com"

bot_token = "7362387491:AAHBFNfpf9iDmMnqrkOjr65j_XXrYn0-sfY"
chat_id = 1142478687  # Keep as integer
# ==============

def send_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {"chat_id": chat_id, "text": text}
        response = requests.post(url, data=data)
        print("✅ Sent to Telegram:", response.json())
    except Exception as e:
        print("❌ Error sending to Telegram:", e)

def check_mail():
    try:
        print("📬 Checking mail...")
        mail = imaplib.IMAP4_SSL(IMAP_URL)
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")

        _, msgnums = mail.search(None, '(UNSEEN SUBJECT "BUY Signal")')
        mail_ids = msgnums[0].split()

        if not mail_ids:
            print("📭 No new signals.")
            mail.logout()
            return

        for num in mail_ids:
            _, data = mail.fetch(num, "(RFC822)")
            msg = email.message_from_bytes(data[0][1])

            # Safely extract body
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body_bytes = part.get_payload(decode=True)
                        if body_bytes:
                            body = body_bytes.decode()
            else:
                body_bytes = msg.get_payload(decode=True)
                if body_bytes:
                    body = body_bytes.decode()

            print("📨 New signal:", body.strip())
            send_telegram(body.strip())

        mail.logout()
    except Exception as e:
        print("❌ Error in check_mail:", e)

# === LOOP ===
while True:
    check_mail()
    time.sleep(30)  # Check every 30 seconds
