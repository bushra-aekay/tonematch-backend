import os
import resend
import logging
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY
SENDER_EMAIL = os.getenv("RESEND_SENDER_EMAIL")

def send_link_to_email(recipent_email: str, url: str):
    if not all([RESEND_API_KEY, SENDER_EMAIL]):
        logger.warning("WARMING: Resend credentials missing. Email send skipped.")
        return
    
    params:resend.Emails.SendParams = {
        "from": SENDER_EMAIL,
        "to": [recipent_email],
        "subject": "Your Login Link",
        "html": f""" 
        <html><body>
        <p>Click the link below to securely log into your account:</p>
        <p><a href="{url}">Login to your Account</a></p>
        <p>This link expires in 10 minutes</p>
        </body></html>
        """
    }

    try:
        email: resend.Email = resend.Emails.send(params)
        
        logger.info(f"Resend Success: Link sent to {recipent_email}. ID: {email['id']}")
        return email
    except resend.exceptions.ResendError as e:
        logger.error(f"Resend API Error: {str(e)}, Detail: {e.message}")
    except Exception as e:
        logger.critical(f"General Error during Resend call: {e}")