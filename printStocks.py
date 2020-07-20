import re
import urllib2
from bs4 import BeautifulSoup
import time
import datetime



def get_stocks(url):
    print 'Retrieving stock information from ' + url
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)

    source = str(soup.find_all('table')[5])
    table = re.findall('><td>(.*?)</td></tr>', source, re.5)

    stocks = []
    # Company name, link, symbol, eps, time
    pattern = r'(.+)</td><td><a href="(.+)">(.+)</a></td><td align="center">(.+)</td><td align="center"><small>([\w\s]+)</small>'
    for line in table:
        M = re.search(pattern, line)
        if M:
            stocks.append([M.group(1), M.group(2), M.group(3), M.group(4), M.group(5)])

    return stocks




def get_next_date():
    today = datetime.date.today()
    next = today + datetime.timedelta(days= 7-today.weekday()>3 else 1)
    next = next.timetuple()

    y = str(next.tm_year)
    m = next.tm_mon
    if m <= 9:
        m = '0' + str(m)
    else:
        m = str(m)
    d = next.tm_mday
    if d <= 9:
        d = '0' + str(d)
    else:
        d = str(d)

    date = y + m + d
    return date



def screen_positive_eps(stocks):
    positives = []
    for stock in stocks:
        if stock[3] != 'N/A' and float(stock[3]) > 0.0:
            positives.append(stock)

    return positives



def sort_today(stocks):
    sorted = []
    for stock in stocks:
        if stock[4] == 'After Market Close':
            sorted.append(stock)
    for stock in stocks:
        if stock[4] == 'Time Not Supplied':
            sorted.append(stock)

    return sorted
