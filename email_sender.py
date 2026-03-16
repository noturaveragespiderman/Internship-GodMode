import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from config import GMAIL_ADDRESS, GMAIL_APP_PASSWORD, CV_PDF_PATH

def send_email(to_email, subject, body, cover_letter_text):
    # Use "mixed" for emails with attachments
    msg = MIMEMultipart("mixed")
    msg["From"] = f"Leonardo Sommariva <{GMAIL_ADDRESS}>"
    msg["To"] = to_email
    msg["Subject"] = subject

    # Create an "alternative" container for plain + HTML body
    body_part = MIMEMultipart("alternative")

    plain = MIMEText(body, "plain")

    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; font-size: 15px; color: #222;
                 max-width: 600px; margin: auto; padding: 20px;">

        <p style="margin-bottom: 20px; line-height: 1.6;">
            {body.replace(chr(10), '<br>')}
        </p>

        <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">

        <p style="font-size: 14px; color: #555; margin: 0;">Best regards,</p>
        <p style="margin: 4px 0;">
            <strong style="font-size: 15px;">Leonardo Sommariva</strong>
        </p>
        <p style="font-size: 13px; color: #555; margin: 2px 0;">
            Master in International Management Candidate
        </p>
        <p style="font-size: 13px; color: #555; margin: 2px 0;">
            University of Cape Town - Graduate School of Business
        </p>
        <p style="font-size: 13px; margin: 4px 0;">
            <a href="mailto:{GMAIL_ADDRESS}" style="color: #0066cc; text-decoration: none;">{GMAIL_ADDRESS}</a>
            &nbsp;|&nbsp;
            <a href="https://www.linkedin.com/in/leonardo-sommariva/" style="color: #0066cc; text-decoration: none;">LinkedIn</a>
        </p>
    
    </body>
    </html>
    """

    html = MIMEText(html_body, "html")
    body_part.attach(plain)
    body_part.attach(html)
    msg.attach(body_part)

    # Attach CV PDF
    if os.path.exists(CV_PDF_PATH):
        with open(CV_PDF_PATH, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition",
                            "attachment; filename=Leonardo_Sommariva_CV.pdf")
            msg.attach(part)
    else:
        print(f"WARNING: CV file not found at {CV_PDF_PATH}")

    # Attach cover letter as txt
    cl_part = MIMEText(cover_letter_text, "plain")
    cl_part.add_header("Content-Disposition",
                       "attachment; filename=Leonardo_Sommariva_Cover_Letter.txt")
    msg.attach(cl_part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_ADDRESS, to_email, msg.as_string())
