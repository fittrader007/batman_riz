import imaplib, email, time, requests

EMAIL = "fittrader007@gmail.com"
PASSWORD = "gsdq cuho kfxw tlgy"
IMAP_URL = "imap.gmail.com"
bot_token = "7362387491:AAHBFNfpf9iDmMnqrkOjr65j_XXrYn0-sfY"
chat_id = "1142478687"

def check_mail():
    mail = imaplib.IMAP4_SSL(IMAP_URL)
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    _, msgnums = mail.search(None, '(UNSEEN SUBJECT "BUY Signal")')
    for num in msgnums[0].split():
        _, data = mail.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(data[0][1])
        body = msg.get_payload(decode=True).decode()
        send_telegram(body)

    mail.logout()

def send_telegram(text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)

while True:
    check_mail()
    time.sleep(30)  # Check every 30 seconds
