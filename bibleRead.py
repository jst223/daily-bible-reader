import datetime
import sys
import requests
import re

from bs4 import BeautifulSoup


def today_str():

    today = datetime.date.today()
    if today.month > 9:
        str_out = str(today.month)
    else:
        str_out = "0" + str(today.month)
    if today.day > 9:
        str_out = str_out + str(today.day)
    else:
        str_out = str_out + "0" + str(today.day)
    year_str = str(today.year)
    str_out = str_out + year_str[2] + year_str[3]
    return str_out


def p_today_bbl(day_str):

    usccb_url = 'http://www.usccb.org/bible/readings/'
    bbl_url = usccb_url + day_str + '.cfm'
    print(bbl_url)
    r = requests.get(bbl_url)

    html = r.text
    soup = BeautifulSoup(html, "html.parser")

    slct_str = ".content-body, .content-header > h3, .content-header > div > a"
    for each in soup.select(slct_str):
        if len(str(each.parent)) > 50:
            ptn_txt = "r'</em>|<em>|</br>|<strong>|</strong>|<div>|</div>|"
            ptn_txt = ptn_txt + "<h4>|</h4>|</a>|<br/>|"
            ptn_txt = ptn_txt + "<div¥ class=¥""bibleReadingsWrapper¥"">|"
            ptn_txt = ptn_txt + "<div class=¥""¥"">'"
            out_text = re.sub(ptn_txt, " ", str(each.text))
            out_text2 = re.sub(r'<br>', ' ', out_text)
            print(str(out_text2))
        else:
            return "TWO"
    return "OK"


print(datetime.date.today())
rtn = p_today_bbl(today_str())

if rtn == "TWO":  # for the feast of Assumption etc ?
    print("Vigil Mass:")
    p_today_bbl(today_str() + "-vigil")
    print("Day Mass:")
    p_today_bbl(today_str() + "-day-mass")
