from celery_app import celery
import smtplib
from email.mime.text import MIMEText
from os import getenv
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)

SMTP_HOST: str = getenv("SMTP_HOST") or ""
SMTP_PORT: int = int(getenv("SMTP_PORT") or 587)
SMTP_USER: str = getenv("SMTP_USER") or ""
SMTP_PASSWORD: str = getenv("SMTP_PASSWORD") or ""
SMTP_FROM: str = getenv("SMTP_FROM") or ""


@celery.task  # type: ignore[misc]
def notify_task_created(
    task_id: int, title: str, user_email: str
) -> dict[str, str | int]:
    msg = MIMEText(f"Your task '{title}' (ID: {task_id}) was created successfully.")
    msg["Subject"] = f"Task Created: {title}"
    msg["From"] = SMTP_FROM
    msg["To"] = user_email

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_FROM, user_email, msg.as_string())

    print(f"[email] Sent to {user_email} for task {task_id}")
    return {"task_id": task_id, "emailed": user_email}
