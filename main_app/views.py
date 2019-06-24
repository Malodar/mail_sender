import os
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.mail import BadHeaderError, send_mail, send_mass_mail
from datetime import datetime
from .forms import EventUploadFileForm
from django.core.files.storage import default_storage
from django.conf import settings
from datetime import datetime

import csv, smtplib, ssl
import email.mime.multipart as mp
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from multiprocessing import Pool
from .forms import EventUploadFileForm


def index(request):
    form = EventUploadFileForm()
    return render(request, 'main_app/index.html', {'form': form})


def sending_email(dct):
    name = dct["name"]
    author = dct["author"]

    password = dct["password"]
    # print('password:', password)
    recipient = dct["recipient"]
    # recipient = 'jdang1404@gmail.com'
    dob = dct["dob"]
    passport_num = dct["passport"]
    phone = dct["phone"]
    email = dct["email"]
    purpose = dct["purpose"]
    attachments = dct["attachement"]

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
    # print('author:', msg['from'])
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
        server.sendmail(msg['from'], [msg['to']], msg.as_string())
        # print(f'Message sent from {author}')
        # print('----------------------')
    except:
        print('WRONG LOGIN OR PASSWORD:', author, password)
        server = smtplib.SMTP('smtp.yandex.com')
        server.starttls()
        server.login(author, password)
    # server.quit()


def upload_csv(request):
    if request.method == 'POST':
        form = EventUploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file_csv']
            save_path = os.path.join(settings.BASE_DIR, 'upload', str(csv_file))
            uploaded_file_path = default_storage.save(save_path, csv_file)
            print('path:', uploaded_file_path)
            # return HttpResponseRedirect(reverse("upload_csv"))

            file_data = open(uploaded_file_path, 'r', encoding='utf-8').read()
            lines = file_data.split("\n")[1:]
            # loop over the lines and save them in db. If error , store as string and then display
            context = []
            for line in lines:
                fields = line.split(",")
                if fields != ['']:
                    data_dict = {}
                    data_dict["name"] = fields[0]
                    if '@gmail' not in fields[1]:
                        data_dict['author'] = fields[1] + '@gmail.com'
                    else:
                        data_dict["author"] = fields[1]
                    data_dict["password"] = fields[2]
                    data_dict["recipient"] = fields[3]
                    data_dict["dob"] = fields[4]
                    data_dict["passport"] = fields[5]
                    data_dict["phone"] = fields[6]
                    data_dict["email"] = fields[7]
                    data_dict["purpose"] = fields[8]
                    data_dict["attachement"] = 'Yes' if fields[9] else 'No'
                    # data_dict["attachement"] = [x for x in fields[9:] if x]
                    context.append(data_dict)

            return render(request, 'main_app/upload_csv.html', {'uploaded_file': uploaded_file_path,
                                                                'data': context})
    else:
        form = EventUploadFileForm()
    return render(request, 'main_app/upload_csv.html', {'form': form})


def send_bulk_emails(request):
    start = datetime.now()
    print('START:', start)
    context = eval(request.POST['fl'])
    # for c in context:
    #     sending_email(c)
    with Pool(5) as p:
        p.map(sending_email, context)
    stop = datetime.now()
    print('Time required to send 105 emails:', stop - start)
    return render(request, 'main_app/sent_mails.html', {})
