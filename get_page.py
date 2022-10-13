import requests
from get_page_data import get_table,save_to_sql
import bs4
import time 
testurl = "http://fgj.wuhan.gov.cn/xxgk/xxgkml/sjfb/mrxjspfcjtjqk/index.shtml"
"""此页是用来获取房管局每日交易的日期和对应的url的后缀.

by : Lkad 2018/03/05 22:21
"""
page_url_base='http://fgj.wuhan.gov.cn/xxgk/xxgkml/sjfb/mrxjspfcjtjqk/index_'
# the download list's post url,+get_end_pg_nm+.html is the complete url to get every day link 
baseurl = 'http://scxx.fgj.wuhan.gov.cn'




def get_every_page_day_link(page_list_link):
    # 获取列表页面，每日成交的链接和日期
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    result = requests.get(page_list_link,headers=headers)
    result.encoding='utf-8'
    soup = bs4.BeautifulSoup(result.text,'html.parser')
    link_all = soup.find_all('a')
    date_link={}
    for i in link_all:
        link_attr = i.attrs
        link_content = i.contents
        # print(link_attr)
        if  '建商品房网签备案统计情况' in i.text:
            link_post = i.get('href')
            text = i.text
            _date = text.split('日')[0].replace("年",'-').replace('月','-')
            if '-' in _date:

                date_link[_date]=link_post
        
    return date_link


def get_all_date_link(url):
    #获取所有的日期和对应日期的链接后缀。
    # headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

    # result = requests.get(url,headers=headers)
    # result.encoding='utf-8'
#    print(result.text)
    # soup = bs4.BeautifulSoup(result.text,'html.parser')
    # links = soup.find_all('a')
    end_page_nm = 67
    
#    print(get_every_page_day_link(url))
#get the first page 
    # all_date_link=(get_every_page_day_link(url))
    all_date_link = {}
    for i in range(1, end_page_nm):
        temp_link = get_every_page_day_link(page_url_base+str(i)+'.shtml')
        all_date_link=dict(**all_date_link,**temp_link)
        print("xxx")
    return all_date_link


if __name__ == '__main__':
    a=get_all_date_link(testurl)
    # print(a)
    all_data=[]
    for _date,_url in a.items():
        try:
            save_to_sql(_date, _url)
            time.sleep(2)
            # all_data.append({_date:data})
            # print(_date,data)
        except Exception as e:
            print(e,_date,_url)
