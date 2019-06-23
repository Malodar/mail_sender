# -*- coding: UTF-8 -*-
import csv, smtplib, ssl
import email.mime.multipart as mp
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from multiprocessing import Pool


def sending_email(row):
    name = row[0]
    author = row[1]
    password = row[2]
    recipient = row[3]
    # recipient = 'jdang1404@gmail.com'
    dob = row[4]
    passport_num = row[5]
    phone = row[6]
    email = row[7]
    purpose = row[8]
    attachments = [x for x in row[9:] if x]

    text = f"""
            Name: {name}

            DOB: {dob}

            Passport Number: {passport_num}

            Phone number: {phone}

            Email: {email}

            Purpose: {purpose}
            """

    msg = mp.MIMEMultipart()
    msg['to'] = recipient
    msg['from'] = author
    msg['subject'] = 'TEST ' + passport_num
    msg.attach(MIMEText(text))

    for f in attachments or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=f
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % f.split('/')[-1].split('\\')[-1]
        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com')
    server.starttls()
    try:
        server.login(author, password)
    except:
        server = smtplib.SMTP('smtp.yandex.com')
        server.starttls()
        server.login(author, password)
    server.sendmail(msg['from'], [msg['to']], msg.as_string())
    print(f'Message sent from {author}')
    print('----------------------')


# with open('sample1.csv', 'r') as rf:
#     reader = csv.reader(rf)
#     next(reader)
#
#     with Pool(2) as p:
#         p.map(sending_email, reader)

    # for row in reader:
    #     send_email(row)

text = 'HELLO WORLD'
password = '62tranphu'
author = 'linh.tongkhanh51@gmail.com'
msg = mp.MIMEMultipart()
msg['to'] = 'kunitsyn-a-v@yandex.ru'
msg['from'] = author
msg['subject'] = 'TEST '
msg.attach(MIMEText(text))

#
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
# server.starttls()

server.login(author, password)

server.sendmail(msg['from'], [msg['to']], msg.as_string())
print(f'Message sent from {author}')
print('----------------------')
