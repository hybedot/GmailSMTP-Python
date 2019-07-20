import os
from typing import List
import smtplib

from dotenv import load_dotenv

class GmailerException(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class Gmailer():
    load_dotenv(".env", verbose=True)
    EMAIL = os.environ.get("EMAIL", None)
    PASSWORD = os.environ.get("PASSWORD", None)

    FAILED_LOAD_EMAIL = 'Failed to load email'
    FAILED_LOAD_PASSWORD = 'Failed to load password'

    @classmethod
    def sendMail(cls, sender:str, email: List[str], subject: str, body: str):
        if cls.EMAIL is None:
            raise GmailerException(cls.FAILED_LOAD_EMAIL)

        if cls.PASSWORD is None:
            raise GmailerException(cls.FAILED_LOAD_PASSWORD)
        
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            
            try:
                server.login(cls.EMAIL, cls.PASSWORD)

                msg = f"Subject: {subject}\n\n{body}"
                
                server.sendmail(
                    sender,
                    email,
                    msg
                )
                print ('Email sent')
            finally:
                server.quit()

        except smtplib.SMTPAuthenticationError:
            print ('Error: Your email or password is incorrect')
        except smtplib.SMTPException as e:
            print(e)
        

