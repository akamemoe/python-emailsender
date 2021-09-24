#!/usr/bin/env python3

import smtplib
from email.utils import formataddr
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os,sys,configparser,click

class EmailHelper():

    def __init__(self,conf):
        self._host = conf['smtphost']
        self._port = int(conf['smtpport'])
        self._username = conf['username']
        self._password = conf['password']
        self._nickname = conf['nickname'] or username

    def send_email(self,recipient,subject,content):

        msg = MIMEText(content)

        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = formataddr([self._nickname,self._username])
        msg['To'] = formataddr(['To',recipient])

        with smtplib.SMTP_SSL(self._host, self._port) as server:
            server.login(self._username, self._password)
            server.sendmail(self._username, recipient, msg.as_string())

    def send_email_with_attachments(self,recipient,subject,content,attached_files=[]):
        msg = MIMEMultipart()

        for file_item in attached_files:
            assert os.path.exists(file_item)
            with open(file_item,'rb') as f:
                data = f.read()
            part = MIMEApplication(data,name=os.path.basename(file_item))
            msg.attach(part)

        msg.attach(MIMEText(content))

        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = formataddr([self._nickname,self._username])
        msg['To'] = formataddr(['To',recipient])

        with smtplib.SMTP_SSL(self._host, self._port) as server:
            server.login(self._username, self._password)
            server.sendmail(self._username, recipient, msg.as_string())


@click.command()
@click.option('-r','--recipient',required=True,help='the recipient email address')
@click.option('-s','--subject',required=True,help='the subject of email')
@click.option('-t','--text',required=True,help='the plain text content of email')
@click.option('-c','--config',default='email.ini',help='specify config file')
@click.option('-f','--attached_files',multiple=True,help='the attached files')
def commandline(recipient,subject,text,attached_files,config):
    cfg = configparser.ConfigParser()
    configLocation = None
    for location in [config,os.path.expanduser('~/.email.ini'),'/etc/emailsender/email.ini']:
        if os.path.exists(location):
            configLocation = location
            break
    assert configLocation != None 
    cfg.read(configLocation,encoding='utf-8')
    helper = EmailHelper(cfg['EMAIL'])
    helper.send_email_with_attachments(recipient,subject,text,attached_files)

if __name__ == '__main__':
    commandline()
