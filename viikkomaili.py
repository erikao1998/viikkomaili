
import datetime
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from datetime import date

def generate_weeknumber():
    x = datetime.datetime.now()
    year = x.year
    month = x.month
    day = x.day

    week = datetime.date(year, month, day).isocalendar()[1]
    return week + 1


url = "https://etelasuomalainenosakunta.fi/tapahtumakalenteri/"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
times = soup.find_all("span", class_="tribe-event-date-start")
titles = soup.find_all('a', class_="tribe-events-calendar-list__event-title-link tribe-common-anchor-thin")

t = [(time.get_text(), title.get_text().strip()) for time, title in zip(times, titles)]

print(t)

