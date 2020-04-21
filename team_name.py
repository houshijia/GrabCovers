#-*- coding: utf-8 -*-

from urllib.parse import urlencode
import requests
from lxml import etree
import MySQLdb

ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240"
team_list = []

def get_content(url):
    with requests.request('GET',url,headers = {'User-agnet':ua}) as res:
        content = res.text
        html = etree.HTML(content)
        return html

for i in range(1,31):
    url = "http://nba.win007.com/cn/Team/Summary.aspx?TeamID={}".format(i)
    html = get_content(url)
    # data = html.xpath('/html/body/div[@id="info"]/div[@id="mainTitle"]/tr[1]/td[3]/text()')
    data = html.xpath('/html/head/title/text()')
    name = data[0].strip()
    tup = (name[0:len(name)-6],i)
    team_list.append(tup)

print(team_list)
conn = MySQLdb.connect(
        host = '127.0.0.1',
        port = 3306,
        user = 'root',
        passwd = '3989313hsj+',
        db = 'nba_data',
        charset="utf8",
    )
cur = conn.cursor()  
sql1 = "update team_dict set team_name=%s where id=%s"
cur.executemany(sql1,team_list)
cur.close()
conn.commit()
print("成功")
conn.close()
