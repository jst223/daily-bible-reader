import datetime
import sys
import requests
import re

from bs4 import BeautifulSoup

def today_string():
    today = datetime.date.today()
    if today.month > 9:
        today_string_out = str(today.month)
    else:
        today_string_out = "0"+str(today.month)
    if today.day > 9:
        today_string_out = today_string_out + str(today.day)
    else:
        today_string_out = today_string_out + "0" + str(today.day)
    year_string = str(today.year)
    today_string_out = today_string_out + year_string[2] + year_string[3]
    return today_string_out

def print_today_bible(daystring):
    bible_reading_url='http://www.usccb.org/bible/readings/' + daystring + '.cfm'

    r = requests.get(bible_reading_url)

    html = r.text
    soup = BeautifulSoup(html, "html.parser")

    for each in soup.find_all(class_="bibleReadingsWrapper"):
        if len(each.text)>50:
            out_text = re.sub(r'</em>|<em>|</br>|<strong>|</strong>|<div>|</div>|<h4>|</h4>|</a>|<div class.*>|<a href=.*', " ", str(each.parent))
            out_text2 = re.sub(r'<br>', ' ', out_text)
            sys.stdout.write(str(out_text2))
        else:
            return "TWO"
    return "OK"
        
print (datetime.date.today())
rtn = print_today_bible(today_string())

if rtn=="TWO": # for the feast of Assumption etc ?
    print("Vigil Mass:")
    print_today_bible(today_string()+"-vigil")
    print("Day Mass:")
    print_today_bible(today_string()+"-day-mass")
