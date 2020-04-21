#-*- coding: utf-8 -*-
from urllib.parse import urlencode
import requests
from lxml import etree
import pandas as pd

ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240"

def get_content(url):
    with requests.request('GET',url,headers = {'User-agnet':ua}) as res:
        content = res.text
        html = etree.HTML(content)
        return html

def get_avg(a,b):
    return (float(a) + float(b))/2

# /html/body/div[3]/div[3]/table/tbody/tr[3]/td[1]/table/tbody/tr[3]/td[5]
# url = "http://nba.win007.com/analysis/326362.htm"
url = "http://score.nowscore.com/nbaAnalysis/326121.html"
html = get_content(url)
#平均分
h_score_avg = html.xpath('//div[@id="teammain"]/table/tr[3]/td[1]/table/tr[3]/td[5]/text()')
h_lost_avg = html.xpath('//div[@id="teammain"]/table/tr[3]/td[1]/table/tr[3]/td[6]/text()')
g_score_avg = html.xpath('//div[@id="teammain"]/table/tr[3]/td[2]/table/tr[3]/td[5]/text()')
g_lost_avg = html.xpath('//div[@id="teammain"]/table/tr[3]/td[2]/table/tr[3]/td[6]/text()')

#各自主客平均分
hh_score_avg = html.xpath('//div[@id="teammain"]/table/tr[3]/td[1]/table/tr[4]/td[5]/text()')
hh_lost_avg = html.xpath('//div[@id="teammain"]/table/tr[3]/td[1]/table/tr[4]/td[6]/text()')
gg_score_avg = html.xpath('//div[@id="teammain"]/table/tr[3]/td[2]/table/tr[5]/td[5]/text()')
gg_lost_avg = html.xpath('//div[@id="teammain"]/table/tr[3]/td[2]/table/tr[5]/td[6]/text()')


print(h_score_avg,h_lost_avg,g_score_avg,g_lost_avg)
print(hh_score_avg,hh_lost_avg,gg_score_avg,gg_lost_avg)
hga1 = get_avg(h_score_avg[0],g_lost_avg[0])
hga2 = get_avg(h_lost_avg[0],g_score_avg[0])

hhgga1 = get_avg(hh_score_avg[0],gg_lost_avg[0])
hhgga2 = get_avg(hh_lost_avg[0],gg_score_avg[0])

print(get_avg(h_score_avg[0],g_lost_avg[0]))
print(get_avg(h_lost_avg[0],g_score_avg[0]))
print(hga1+hga2)
print(hhgga1+hhgga2)
