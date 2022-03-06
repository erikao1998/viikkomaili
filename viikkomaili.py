
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
from urllib.request import urlopen
from dotenv import load_dotenv
from os import getenv
import requests
from bs4 import BeautifulSoup

load_dotenv()
wp_password = getenv("PASSWORD")
wp_username = getenv("USER_NAME")
sender_email = getenv("SENDER_EMAIL")
receiver_email = getenv("RECEIVER_EMAIL")
email_password = getenv("EMAIL_PASSWORD")
viikkomaili_url = getenv("URL")

def generate_weeknumber():
    x = datetime.datetime.now()
    year = x.year
    month = x.month
    day = x.day

    week = datetime.date(year, month, day).isocalendar()[1]
    return week + 1

port = 465
smtp_server = "smtp.gmail.com"

session = requests.session()

url = "https://www.etelasuomalainenosakunta.fi/wp-login.php"
cookies = {"wordpress_test_cookie": "WP%20Cookie%20check"}
data = {"log": wp_username, "pwd": wp_password, "wp-submit": "Kirjaudu sis\xc3\xa4\xc3\xa4n", "redirect_to": "https://www.etelasuomalainenosakunta.fi/wp-admin/", "testcookie": "1"}
session.post(url, cookies=cookies, data=data)

page = session.get(viikkomaili_url)
soup = BeautifulSoup(page.text, 'html.parser')
t = soup.pre

text = t.contents[0]
splitted_text = text.split("* * *")
tulevat_tapahtumat_split = splitted_text[3].split("- - -")
new_tt = ""
counter = 0
for x in tulevat_tapahtumat_split:

    if counter > 3:
        break
    if "Kahvitus" not in x:
        new_tt = new_tt + x
        counter += 1

# The next line is commented because it is used only if there are no upcoming events in the week (if this line is used, one must comment lines 64-66).
# new_text = "Viikon ohjelma:\n\nEi tapahtumia tällä viikolla :(\n\n- - -\n\n"

new_text = ""
for i in range(len(splitted_text) - 1):
    new_text = new_text + splitted_text[i]

new_text = new_text + new_tt

week_number = generate_weeknumber()

message = """\
Subject: Osakunnan tapahtumat viikolla {}

{}
""".format(week_number, new_text)

encoded_message = message.encode("utf-8")

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, email_password)
    server.sendmail(sender_email, receiver_email, encoded_message)
    print("Viesti lähetetty!")
