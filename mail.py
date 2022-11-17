import sys
import os
import smtplib
import yfinance as yf

## from email.message import EmailMessage

email_addr = 'serviceburner714@gmail.com'
email_pass = 'ktilnzouhwxgdbdj'


class create_email:
    def __init__(self, start):
        self.screen = start.screen
        self.create_Email_page_finished = False

    def send_email(self, user_email, stocks):

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()                             ## secures email
            smtp.starttls()
            smtp.ehlo()

            smtp.login(email_addr, email_pass)

            subject = 'Stock Alert Confirmation'
            body = 'You have created an alert for the following stocks: \n' + str(stocks)
            msg = f'Subject: {subject}\n\n{body}'

            smtp.sendmail('serviceburner714@gmail.com', user_email, msg)

    def check_update(self, list):
        # this gets ticker and assigns it to tick
        tick = yf.Ticker(list)
        # this allows to get price from 
        yo = tick.info
        yo_price = yo['regularMarketPrice']
        print(yo_price)