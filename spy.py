from urllib.parse import urlencode
import requests
from lxml import etree

url = "http://nba.win007.com/odds/AsianOdds_n.aspx?id=362243"
ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240"


def get_content():
    with requests.request('GET',url,headers = {'User-agnet':ua}) as res:
        content = res.text
        html = etree.HTML(content)
        return html

def one_tr(html,num):
        td_path = '/html/body/table[@id="odds"]/tr[{}]/td[not(@id="td_14" or @id="td_15" or @id="td_16")]'.format(num)
        data = html.xpath(td_path)
        for elem in data:
            txt = elem.xpath('string(.)').strip()
            print(txt)
        # print(data)

def all_tr():
    html = get_content()
    tr_path = '/html/body/table[@id="odds"]/tr[not(@style="display:none;")]'
    data = html.xpath(tr_path)
    print(len(data))
    for num in range(3,len(data)+1):
        one_tr(html,num)

all_tr()
