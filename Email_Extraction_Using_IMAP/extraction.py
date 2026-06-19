import imaplib
import email
from email.header import decode_header



IMAP_SERVER = "imap.gmail.com"
EMAIL = "---"
APP_PASSWORD = "---"  



def decode_mime_header(value):
    if not value:
        return ""

    decoded_parts = decode_header(value)
    result = ""

    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            result += part.decode(encoding or "utf-8", errors="ignore")
        else:
            result += part

    return result


# ========================
# EXTRACT EMAIL BODY
# ========================
def extract_body(message):
    body = ""

    if message.is_multipart():
        for part in message.walk():

            content_type = part.get_content_type()
            disposition = str(part.get("Content-Disposition"))

            if (
                content_type == "text/plain"
                and "attachment" not in disposition.lower()
            ):
                payload = part.get_payload(decode=True)

                if payload:
                    body = payload.decode(errors="ignore")
                    break

    else:
        payload = message.get_payload(decode=True)
        if payload:
            body = payload.decode(errors="ignore")

    return body


# ========================
# READ EMAILS FROM FOLDER
# ========================
def fetch_from_folder(mail, folder):

    print("\n" + "=" * 80)
    print(f"📁 Reading folder: {folder}")
    print("=" * 80)

    status, _ = mail.select(f'"{folder}"')

    if status != "OK":
        print(f"❌ Cannot open folder: {folder}")
        return

    status, data = mail.search(None, "ALL")

    if status != "OK":
        print("❌ Failed to fetch emails")
        return

    email_ids = data[0].split()

    latest_emails = email_ids

    for email_id in reversed(latest_emails):

        status, msg_data = mail.fetch(email_id, "(RFC822)")

        if status != "OK":
            continue

        raw_email = msg_data[0][1]

        message = email.message_from_bytes(raw_email)

        subject = decode_mime_header(message.get("Subject"))
        sender = decode_mime_header(message.get("From"))
        date = message.get("Date")
        body = extract_body(message)

        print("\n----------------------------------------")
        print("Subject :", subject)
        print("From    :", sender)
        print("Date    :", date)
        print("Body    :")
        print(body[:500])  # preview only


# ========================
# MAIN FUNCTION
# ========================
def read_emails():

    mail = imaplib.IMAP4_SSL(IMAP_SERVER)

    try:
        mail.login(EMAIL, APP_PASSWORD)

        # Gmail folders
        folders = [
            "INBOX",
            "[Gmail]/Sent Mail",
            "[Gmail]/Spam"
        ]

        for folder in folders:
            fetch_from_folder(mail, folder)

    finally:
        mail.logout()


# ========================
# RUN SCRIPT
# ========================
if __name__ == "__main__":
    read_emails()
