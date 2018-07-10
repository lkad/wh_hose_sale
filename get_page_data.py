import bs4
import requests
testurl = 'http://fgj.wuhan.gov.cn/mrxjspfcjtjqk/44139.jhtml'
"""
本页通过遍历日期和对应的页面链接，来获取表格数据，然后保存在mysql中
by lkad 2018/03/05

"""
import pymysql
mysql_config={'user': 'whhouse',
        'password': 'Zz0099.',
        'db': 'wuhan_house',
        'charset': 'utf8',
        'host': '192.168.8.109'
        }
def get_table(url):
# 获取页面数据
    headers = {'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    result = requests.get(url, headers=headers)
    result.encoding='utf-8'
    result_bs = bs4.BeautifulSoup(result.text, 'html.parser')
    tbody = result_bs.tbody
    #先获取第一个tbody标签所有内容。
#    print(tbody)
    atr = tbody.findAll('tr')
    #在tbody 里面搜索所有的tr标签
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
                'area': tds[0].getText(),
                'normal_trad_nm': tds[1].getText(),
                'normal_trad_vol': tds[2].getText(),
                'business_trad_nm': tds[3].getText(),
                'business_trad_vol': tds[4].getText(),
                'office_trad_nm': tds[5].getText(),
                'office_trad_vol': tds[6].getText(),
                'other_trad_nm': tds[7].getText(),
                'toher_trad_vol': tds[8].getText()
                })
        id+=1

    return table_content

def exist_date(date,curso):
    sql = "select 1 from new_table where trad_date = '%s'" % date
    curso.execute(sql)
    # curso.execute('commit')
    row=curso.rowcount

    if row > 4:
        return True

    else:
        return  False



def save_to_sql(Date,url):
    data = get_table(url)
    conn = pymysql.connect(**mysql_config)
    curso = conn.cursor()
    if not exist_date(Date, curso):

        for i in data:
            sql = "insert into new_table (trad_date,area,normal_trad_nm,normal_trad_vol,business_trad_nm," \
                  'business_trad_vol,office_trad_nm,office_trad_vol,other_trad_nm,toher_trad_vol) values ("%s","%s",%s,%s,%s,%s,%s,%s,%s,%s) ' % (
            Date, i['area'], i['normal_trad_nm'], i['normal_trad_vol'], i['business_trad_nm'], i['business_trad_vol'],
            i['office_trad_nm'], i['office_trad_vol'], i['other_trad_nm'], i['toher_trad_vol'])
            curso.execute(sql)
            curso.execute('commit')
        conn.close()




if __name__ == '__main__':
    save_to_sql('2012-05-05',testurl)
    for i in get_table(testurl):
        print(i)
