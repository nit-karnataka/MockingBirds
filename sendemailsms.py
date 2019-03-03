import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import os

import time
from time import sleep
from sinchsms import SinchSMS

class SendSMS:
    def __init__(self, recienpt_no):
        self.number = recienpt_no
        self.app_key = 'a26ee675-b15c-422c-ba04-4dd117e97bb4'
        self.app_secret = 'jiz5EVhoTUuWoKyy54ibhw=='

    def send(self, sms_body):
        client = SinchSMS(self.app_key, self.app_secret)
        print("Sending '%s' to %s" % (sms_body, self.number))

        response = client.send_message(self.number, sms_body)
        message_id = response['messageId']
        response = client.check_status(message_id)

        while response['status'] != 'Successful':
            print(response['status'])
            time.sleep(1)
            response = client.check_status(message_id)

        print(response['status'])

class SendEmail:
    def __init__(self, fromaddr, from_password, toaddr):
        self.fromaddr = fromaddr
        self.toaddr = toaddr
        self.from_password = from_password
        self.msg = MIMEMultipart()

    def upload_attachments(self, attachments):
        for attachment in attachments:
            filename = os.path.basename(attachment)
            with open(attachment, 'rb') as file_reader:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(file_reader.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', "attachment; filename={}".format(filename))
                self.msg.attach(part)

    def send(self, subject, body, attachments):
        self.msg['From'] = self.fromaddr
        self.msg['To'] = ', '.join(self.toaddr)
        self.msg['Subject'] = subject

        self.msg.attach(MIMEText('Please Check Attachments', 'plain'))

        self.upload_attachments(attachments)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.fromaddr, self.from_password)

        text = self.msg.as_string()
        server.sendmail(self.fromaddr, ', '.join(self.toaddr), text)
        server.quit()

class SendEmailSms:
    def __init__(self, fromaddr, from_password, toaddr, recienpt_no='+919981763613'):
        self.email_server = SendEmail(fromaddr, from_password, toaddr)
        self.sms_server = SendSMS(recienpt_no)

    def send(self, attachments, subject_email='Recommended PDFs for your Research', body_email='Please Find Attached PDFs', sms_body='Please check your E-mail for Recommended PDFs for your Research.'):
        self.email_server.send(subject_email, body_email, attachments)
        print(self.sms_server.send(sms_body))


if __name__ == '__main__':
    toaddr = ['jatinmandav3@gmail.com', 'rupakkalita3@gmail.com', 'ritikakumari1302@gmail.com']
    subject = 'Research Papers'
    body = 'Please find attached PDFs matching your keywords.'
    attachments = ['pdfs/10-1055-a-0650-3908.PMC6175603.pdf']
    sms_body = 'You have recieved new papers. Please check your E-mail'
    #recienpt_no = []

    fromaddr = 'pdhindujaa@gmail.com'
    password = '!1q2w3e4r5t%'
    server = SendEmailSms(fromaddr, password, toaddr)
    server.send(subject, body, attachments, sms_body)
