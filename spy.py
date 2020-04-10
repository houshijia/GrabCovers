from urllib.parse import urlencode
import requests
from lxml import etree

url = "http://nba.win007.com/odds/AsianOdds_n.aspx?id=362541"
ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240"


def get_content():
    with requests.request('GET',url,headers = {'User-agnet':ua}) as res:
        content = res.text
        html = etree.HTML(content)
        return html


#庄家数据
def bookie_data():
    html = get_content()
    tr_path = '/html/body/table[@id="odds"]/tr[not(@companyid)]'
    td_path = './td[not(@id="td_14" or @id="td_15" or @id="td_16")]'
    data = html.xpath(tr_path)
    print(len(data))

    for num in range(2,len(data)):
        res = data[num].xpath(td_path)
        for i in range(0,len(res)):
            if(i != 1 and i != 8):
                tx = res[i].xpath('string(.)').strip()
                print(tx)


#比赛数据
def game_info():
    html = get_content()
    game_time = html.xpath('/html/body/div[@class="header"]/div[@class="analyhead"]/div[@class="vs"]/div[1]/text()')
    home = html.xpath('/html/body/div[@class="header"]/div[@class="analyhead"]/div[@class="home"]/a/text()')
    guest = html.xpath('/html/body/div[@class="header"]/div[@class="analyhead"]/div[@class="guest"]/a/text()')
    score = html.xpath('/html/body/div[@class="header"]/div[@class="analyhead"]/div[@class="vs"]/div[@id="headVs"]/div[@class="end"]/div[@class="score"]/text()')
    print(game_time[1])
    print(home)
    print(guest)
    print(score)
    # print(score[1])


game_info()
bookie_data()

