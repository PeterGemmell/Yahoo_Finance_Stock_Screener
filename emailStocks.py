import re
import urllib2
from bs4 import BeautifulSoup
import time
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

Uname = 'gmail_username'
Pword = 'gmail_password'
Faddr = Uname + '@gmail.com'
Taddr = 'recipient@gmail.com'


def send_email(username, password, fromaddr, toaddr, msg):
    print 'Sending stock information to ' + toaddr
    try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()
            server.login(username,password)
            server.sendmail(fromaddr, toaddr, msg.as_string())
            server.quit()
    except:
            print 'Unable to send email'



def get_stocks(url):
    print 'Retrieving stock information from ' + url
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)

    source = str(soup.find_all('table')[5])
    table = re.findall('><td>(.*?)</td></tr>', source, re.S)

    stocks = []
    # Company name, link, symbol, time, eps
    pattern = r'(.+)</td><td><a href="(.+)">(.+)</a></td><td align="center">(.+)</td><td align="center"><small>([\w\s]+)</small>'
    for line in table:
            M = re.search(pattern, line)
            if M:
                    stocks.append([M.group(1), M.group(2), M.group(3), M.group(4), M.group(5)])

    return stocks


def get_next_date():
        today = datetime.date.today()
        next = today + datetime.timedelta(days= 7-today.weekday() if today.weekday()>3 else 1)
        next = next timetuple()

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


def screen_positive__eps(stocks):
    print 'Screening stocks for positive EPS...'
    positives = []
    for stock in stocks:
            if stock[3] != 'N/A' and float(stock[3]) > 0.0:
                    positives.append(stock)
    return positives


def sort_today(stocks):
        print 'Sorting todays stocks...'
        sorted = []
        for stock in stocks:
                if stock[4] == 'After Market Close':
                        sorted.append(stock)
        for stock in stocks:
                if stock[4] == 'Time Not Supplied':
                        sorted.append(stock)
        return sorted


def sort_tom(stocks):
    print 'Sorting next business days stocks...'
    sorted = []
    for stock in stocks:
        if stock[4] == 'Before Market Open':
            sorted.append(stock)
    for stock in stocks:
        if stock[4] == 'Time Not Supplied':
            sorted.append(stock)
    return sorted
