#!/usr/bin/python
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def sendAlert(subject, emailBody):

    fromaddr = "instafame.alerts@gmail.com"
    toaddr = "instafameapp@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = str(subject)

    body = str(emailBody)
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "Qus6TzHQbFd454UTeLqSQQwWNP3QRW8DNtjTjJ2SEhw4EPYTNHTPKMYDaQcFkGwBF6w8xtacTnbUsJke7n5nyhjYfCauaBXs3gu7")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
