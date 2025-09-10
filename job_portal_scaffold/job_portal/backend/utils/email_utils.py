from datetime import datetime
from flask_mail import Message
from ..app import mail, db
from ..models.email_log import EmailLog

def send_email(to, subject, html_body, text_body=None):
    log = EmailLog(to_address=to, subject=subject, body=html_body, status="queued")
    db.session.add(log)
    db.session.commit()
    try:
        msg = Message(subject=subject, recipients=[to])
        if text_body:
            msg.body = text_body
        msg.html = html_body
        mail.send(msg)
        log.status = "sent"
        log.sent_at = datetime.utcnow()
    except Exception as e:
        log.status = "failed"
        log.error = str(e)
    finally:
        db.session.commit()
        return log.status
