# -*- coding: utf-8
from urllib.parse import urlencode
import requests
from lxml import etree
import xlrd
import xlwt
from xlutils.copy import copy
import pymysql

 
url = "https://contests.covers.com/Consensus/TopConsensus/NBA/Overall"
ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240"
 
def gener_consensus_insert(data):
    db = pymysql.connect(host='localhost',user='root',password='123456',port=3306,db='BP20200309')
    cursor = db.cursor()
    for item in data:
        table = 'consensus'
        keys = ','.join(item.keys())
        values = ','.join(['%s']*len(item))
        sql = 'insert into {table}({keys}) VALUES({values})'.format(table=table,keys=keys,values=values)
        try:
            if cursor.execute(sql,tuple(item.values())):
                print('写入数据库成功')
                db.commit()
        except Exception as e:
            print("写入数据库失败",e)
            db.rollback()       
    db.close()
def write_excel_xls(path, sheet_name, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlwt.Workbook()  # 新建一个工作簿
    sheet = workbook.add_sheet(sheet_name)  # 在工作簿中新建一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.write(i, j, value[i][j])  # 像表格中写入数据（对应的行和列）
    workbook.save(path)  # 保存工作簿
    print("xls格式表格写入数据成功！")
def write_excel_xls_append(path, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(i+rows_old, j, value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入
    new_workbook.save(path)  # 保存工作簿
    print("xls格式表格【追加】写入数据成功！")

with requests.request('GET',url,headers = {'User-agent':ua}) as res:
    content = res.text          #获取HTML的内容
    html = etree.HTML(content)  #分析HTML，返回DOM根节点
    team = []
    team2 = []
    handicap =[]
    data = []
    title_key = ['away_team','home_team','handicap','away_select','home_select']
    #cmg_consensus_picks_sorted > div.covers-CoversConsensus-consensusTableContainer > table > tbody > tr:nth-child(2) > td.covers-CoversConsensus-table--matchupColumn
    #cmg_consensus_picks_sorted > div.covers-CoversConsensus-consensusTableContainer > table > tbody > tr:nth-child(2) > td.covers-CoversConsensus-table--matchupColumn > span.covers-CoversConsensus-table--teamBlock > a
    #cmg_consensus_picks_sorted > div.covers-CoversConsensus-consensusTableContainer > table > tbody > tr:nth-child(2) > td:nth-child(4)
    #cmg_consensus_picks_sorted > div.covers-CoversConsensus-consensusTableContainer > table > tbody > tr:nth-child(2) > td:nth-child(3) > span.covers-CoversConsensus-consensusTable--high > span
    teamblock = html.xpath("//div[@class='covers-CoversConsensus-consensusTableContainer']//tr/td[@class='covers-CoversConsensus-table--matchupColumn']/span[@class='covers-CoversConsensus-table--teamBlock']/a")
    for elm in teamblock:
        team.append(elm.attrib.get('title'))
    teamblock2 = html.xpath("//div[@class='covers-CoversConsensus-consensusTableContainer']//tr/td[@class='covers-CoversConsensus-table--matchupColumn']/span[@class='covers-CoversConsensus-table--teamBlock2']/a")
    for elm in teamblock2:
        team2.append(elm.attrib.get('title'))
    handicaps = html.xpath("//div[@class='covers-CoversConsensus-consensusTableContainer']//tr/td[4]/text()")
    for i in range(0,len(handicaps)):
        if i % 2 == 0:
            handicap.append(handicaps[i+1].strip())
    
    scale1 = html.xpath("//div[@class='covers-CoversConsensus-consensusTableContainer']//tr/td[3]/span[1]/span/text()")
    scale2 = html.xpath("//div[@class='covers-CoversConsensus-consensusTableContainer']//tr/td[3]/span[2]/span/text()")
    #cmg_consensus_picks_sorted > div.covers-CoversConsensus-consensusTableContainer > table > tbody > tr:nth-child(2) > td:nth-child(4)
    
    for i in range(0,len(team)):
        tempData = []
        tempData.append(team[i])
        tempData.append(team2[i])
        tempData.append(handicap[i])
        tempData.append(scale1[i])
        tempData.append(scale2[i])
        kv = zip(title_key,tempData)
        data.append(dict(kv))
    print(data)    
    gener_consensus_insert(data)

    # book_name_xls = './covers统计记录.xls'
 
    # sheet_name_xls = 'covers明日统计'
 
    # value_title = [["客队", "主队", "让分", "客队支持率", "主队支持率"]]

    # write_excel_xls(book_name_xls, sheet_name_xls, value_title)

    # write_excel_xls_append(book_name_xls,data)






