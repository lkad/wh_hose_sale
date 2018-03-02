import bs4
import requests
testurl = 'http://scxx.fgj.wuhan.gov.cn/scxxbackstage/whfcj/contents/854/24689.html'

def get_table(url):
    result = requests.get(url)
    result.encoding='gbk'
    result_bs = bs4.BeautifulSoup(result.text, 'html.parser')
    tbody = result_bs.tbody
#    print(tbody)
    atr = tbody.findAll('tr')
#    print(atr)
    id = 0
    table_content=[]
    for tr in atr:
        if id >1:
            tds = tr.findAll('td')
#            print(tds)
            if tds[0].getText() == '合计':
                break
            table_content.append({
                '区域': tds[0].getText(),
                '商品住宅成交数':tds[1].getText(),
                '商品住宅成交面积':tds[2].getText(),
                '写字楼成交数':tds[3].getText(),
                '写字楼成交面积':tds[4].getText(),
                '商业成交数': tds[5].getText(),
                '商业成交面积': tds[6].getText(),
                '其他成交数':tds[7].getText(),
                '其他成交面积': tds[8].getText()
                })
        id+=1

    return table_content


if __name__ == '__main__':
    for i in get_table(testurl):
        print(i)
