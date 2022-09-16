import sys
import os
import smtplib
## from email.message import EmailMessage

email_addr = 'serviceburner714@gmail.com'
email_pass = 'ktilnzouhwxgdbdj'
user_email = 'moralesjose1428@gmail.com'            ## need to get user input for email

class create_email:
    def __init__(self, start):
        self.screen = start.screen
        self.create_Email_page_finished = False


    def send_email(self):

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()                             ## secures email
            smtp.starttls()
            smtp.ehlo()

            smtp.login(email_addr, email_pass)

            subject = 'Stock Alert Confirmation'
            body = 'You have created an alert for the following stock: '        ## need to include stock symbol
            msg = f'Subject: {subject}\n\n{body}'

            smtp.sendmail('serviceburner714@gmail.com', user_email, msg)
