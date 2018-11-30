#!/usr/bin/python

# Sending lib
import smtplib
# Email formatting
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
# Time stamps
import time


# Credentials:
eUser = "rsd18wc3"
eFrom = "rsd18wc3@gmail.com"
ePsswd = "Rsd2018wc3"
eTo = "cavie17@student.sdu.dk"
eSubject = "WorkCell 3 initalization"

# Compose email
msg = MIMEMultipart()
# Headers
msg['From'] = eUser
msg['To'] = eTo
msg['Subject'] = eSubject
# Body
eBody = "WorkCell 3 initialized correctly." + "\n" + "\n" + time.strftime("%c")
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