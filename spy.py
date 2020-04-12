from urllib.parse import urlencode
import requests
from lxml import etree
import MySQLdb


ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240"
match_id = ""
info_list = []
book_list = []

def get_content(url):
    with requests.request('GET',url,headers = {'User-agnet':ua}) as res:
        content = res.text
        html = etree.HTML(content)
        return html


#盘口数据
def bookie_data(url):
    html = get_content(url)
    tr_path = '/html/body/table[@id="odds"]/tr[not(@companyid)]'
    td_path = './td[not(@id="td_14" or @id="td_15" or @id="td_16")]'
    data = html.xpath(tr_path)
    # print(len(data))

    for num in range(2,len(data)):
        res = data[num].xpath(td_path)
        tup = (match_id,)
        for i in range(0,len(res)):
            if(i != 1 and i != 8):
                tx = res[i].xpath('string(.)').strip()
                print(tx)
                temptup = (tx,)
                tup = tup + temptup
        book_list.append(tup)
        
        # print(book_list)
        

#比赛信息
def game_info(url):
    html = get_content(url)
    game_time = html.xpath('/html/body/div[@class="header"]/div[@class="analyhead"]/div[@class="vs"]/div[1]/text()')
    home = html.xpath('/html/body/div[@class="header"]/div[@class="analyhead"]/div[@class="home"]/a/text()')
    guest = html.xpath('/html/body/div[@class="header"]/div[@class="analyhead"]/div[@class="guest"]/a/text()')
    score = html.xpath('/html/body/div[@class="header"]/div[@class="analyhead"]/div[@class="vs"]/div[@id="headVs"]/div[@class="end"]/div[@class="score"]/text()')
    # print(game_time[1].strip())
    # print(home[0])
    # print(guest[0])
    # print(score[0])
    # print(score[1])
    tup = (match_id,game_time[1].strip(),home[0],guest[0],score[0],score[1])
    info_list.append(tup)
    # print(info_list)
    

# 10月份：362243-362307 11月份:
for m_id in range(362243,362307):
    url = "http://nba.win007.com/odds/AsianOdds_n.aspx?id={}".format(m_id)
    match_id = str(m_id)
    game_info(url)
    bookie_data(url)

conn = MySQLdb.connect(
        host = '127.0.0.1',
        port = 3306,
        user = 'root',
        passwd = '3989313hsj+',
        db = 'nba_data',
    )
cur = conn.cursor()  
sql1 = "insert into nba2019_2020 values(%s,%s,%s,%s,%s,%s)"
sql2 = "insert into handicap_info values(%s,%s,%s,%s,%s,%s,%s,%s)"
cur.executemany(sql1,info_list)
cur.executemany(sql2,book_list)
cur.close()
conn.commit()
conn.close()