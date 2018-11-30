#!/usr/bin/python

import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Credentials:
eUser = "rsd18wc3"
eFrom = "rsd18wc3@gmail.com"
ePsswd = "Rsd2018wc3"
eTo = "cavie17@student.sdu.dk"

def mail_feedback(eSubject, eBody):
    # Compose email
    msg = MIMEMultipart()
    # Headers
    msg['From'] = eUser
    msg['To'] = eTo
    msg['Subject'] = eSubject
    # Body
    msg.attach(MIMEText(eBody, 'plain'))

    # Establish server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    # Log in
    server.login(eUser, ePsswd)

    # Convert object to string
    text = msg.as_string()

    # Send email
    server.sendmail(eFrom, eTo, text)