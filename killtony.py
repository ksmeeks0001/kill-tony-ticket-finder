import smtplib
from email.mime.text import MIMEText
import json
import requests


def email(sender, to, password, body, subject):
    """
    send an email with SMTP on outlook
    """
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    
    mailer = get_mailer(sender, password)
    
    mailer.sendmail(sender, to, msg.as_string())
    

def get_mailer(sender, password):
    """
    Return an open SMTP mailer
    """
    mailer = smtplib.SMTP('smtp.gmail.com', 587)
    mailer.ehlo()
    mailer.starttls()
    mailer.login(sender, password)

    return mailer


if __name__ == '__main__':

    with open('C:\\Users\\kevsm\\Desktop\\killtony\\configs.json', 'r') as file:
        CONFIGS = json.load(file)
    
    
    resp = requests.get('https://comedymothership.com/_next/data/sPRtZRRCAzAmIo-Ap7UHX/en/shows.json')
    if resp.status_code != 200:
        email(CONFIGS['email'], CONFIGS['email'], CONFIGS['emailPass'], "Bad status code", "KILL TONY TICKET FINDER") 
        exit()

    data = resp.json()

    for event in data['pageProps']['data']['events']:
        if event['title'] != "KILL TONY" or event['status'] != 'active' or event['ticketAvailability'] == 'soldout':
            continue

        msg = f"KILL TONY tickets available for {event['start']}!\n"
        msg += event['url']
        email(CONFIGS['email'], CONFIGS['email'], CONFIGS['emailPass'], msg, "KILL TONY TICKET FINDER")
