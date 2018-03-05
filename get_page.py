import requests
from get_page_data import get_table
import bs4
import time 
testurl = 'http://scxx.fgj.wuhan.gov.cn/scxxbackstage/whfcj/channels/854.html'
"""此页是用来获取房管局每日交易的日期和对应的url的后缀.

by : Lkad 2018/03/05 22:21
"""
page_url_base='http://scxx.fgj.wuhan.gov.cn/scxxbackstage/whfcj/channels/854_'
# the download list's post url,+get_end_pg_nm+.html is the complete url to get every day link 
baseurl = 'http://scxx.fgj.wuhan.gov.cn'

def get_end_pg_nm(links):
    # 返回列表分页中的最后一页的编号。
    for i in links:
        if i.text == '末页':
            end_page_link = i.get('href')
    end_page_nm = end_page_link.split("_")[1].split('.')[0]
    return end_page_nm

def get_every_page_day_link(page_list_link):
    # 获取列表页面，每日成交的链接和日期
    result = requests.get(page_list_link)
    result.encoding='GBK'
    soup = bs4.BeautifulSoup(result.text,'html.parser')
    link_all = soup.find_all('a')
    date_link={}
    for i in link_all:
        link_attr = i.attrs
        #print(link_attr)
        if  'service' in link_attr.get('class',['_']):
            link_post = i.get('href')
            text = i.text
            _date = text.split('日')[0].replace("年",'-').replace('月','-')
            date_link[_date]=link_post
    return date_link

    

def get_all_date_link(url):
    #获取所有的日期和对应日期的链接后缀。
    result = requests.get(url)
    result.encoding='GBK'
#    print(result.text)
    soup = bs4.BeautifulSoup(result.text,'html.parser')
    links = soup.find_all('a')
    end_page_nm = get_end_pg_nm(links)
    
#    print(get_every_page_day_link(url))
#get the first page 
    all_date_link=(get_every_page_day_link(url))
    for i in range(2, int(end_page_nm)+1):
        all_date_link=dict(all_date_link,**get_every_page_day_link(page_url_base+str(i)+'.html'))
    return all_date_link

if __name__ == '__main__':
    a=get_all_date_link(testurl)
    print(a)
    all_data=[]
    for _date,_url in a.items():
        try:
            data = get_table(baseurl+_url)
            time.sleep(2)
            all_data.append({_date:data})
            print(_date,data)
        except Exception as e:
            print(e,_date,_url)
