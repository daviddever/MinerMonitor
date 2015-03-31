import cexapi
import smtplib
from email.mime.multipart import MIMEMultipart
from email.MIMEText import MIMEText
from config import config
import json2html
import time

username = config['username']
api_key = config['key']
api_secrect = config['secret']

alert_addresses = config['alert_addresses']
sender = config['sender_address']
smtp_server = config['smtp_server']
workers = config['workers']

COMMASPACE = ', '

def get_stats():
    ghash = cexapi.api(username, api_key, api_secrect)
    stats =  ghash.workers()

    return stats

def check_stats(stats, workers):

    bad_workers = ['']

    for worker in workers:
        if worker['last15m'] < 1500000:
            bad_workers.append(worker)

    if len(bad_workers) > 0:
        return bad_workers

def send_alert(recipient, sender, alert_for, stats, table):
    message = MIMEMultipart('related')
    message['Subject'] = 'Miner Alert!'
    message['From'] = sender
    message['To'] = COMMASPACE.join(recipient)
    message.preamble = 'This is a multi-part message in MIME format.'

    message_alternative = MIMEMultipart('alternative')
    message.attach(message_alternative)

    message_text = MIMEText('{0} may be having issues. GHash is reporting low hash rates\n Ghash stats are below\n {1}'.format(alert_for, stats))
    message_alternative.attach(message_text)

    message_text = MIMEText('<h2>{0} may be having issues.</h2><br>GHash is reporting low hash rates<br>Ghash stats are below<br>{1}'.format(alert_for, table))
    message_text.replace_header('Content-Type','text/html')
    message_alternative.attach(message_text)

    s = smtplib.SMTP(smtp_server)
    s.sendmail(sender, recipient, message.as_string())
    s.quit()


def make_table(json):
    table = json2html.json2html.convert(json = json)

    return table

while True:

    time.sleep(60)

    stats = get_stats()

    bad_wokers = check_stats(stats, workers)
    if bad_workers:
       table = make_table(stats)
       send_alert(alert_addresses, sender, bad_workers, stats, table)

       time.sleep(3600)
