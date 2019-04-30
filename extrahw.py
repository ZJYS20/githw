import requests
import time
import json
import matplotlib.pyplot as plt
import sqlite3
import matplotlib.font_manager as fm

# 获得时间戳
def gettime():
    return int(round(time.time() * 1000))

if __name__ == '__main__':
    "一，请求数据"
    # 定义头部
    headers = {}
    # 传递参数
    keyvalue = {}

    url = 'http://data.stats.gov.cn/easyquery.htm'

    # 头部填充
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                            'AppleWebKit/537.36 (KHTML, like Gecko)' \
                            'Chrome/73.0.3683.86 Safari/537.36'

    # 参数填充
    keyvalue['m'] = 'QueryData'
    keyvalue['dbcode'] = 'hgnd'
    keyvalue['rowcode'] = 'zb'
    keyvalue['colcode'] = 'sj'
    keyvalue['wds'] = '[]'
    keyvalue['dfwds'] = '[{"wdcode":"zb","valuecode":"A0301"}]'
    keyvalue['k1'] = str(gettime())

    # 发出请求，使用get方法
    r = requests.get(url, headers=headers, params=keyvalue)

    # 以上为爬取数据部分，下面是将数据存入数据库文件中

    year = []
    population = []
    men = []
    women = []

    print(r.text)
    data = json.loads(r.text)
    data_one = data['returndata']['datanodes']
    for value in data_one:
        if 'A030101_sj' in value['code']:
            year.append(value['code'][-4:])
            population.append(int(value['data']['strdata']))
        if 'A030102_sj' in value['code']:
            men.append(int(value['data']['strdata']))
        if 'A030103_sj' in value['code']:
            women.append(int(value['data']['strdata']))

    conn = sqlite3.connect('population.db')
    print("Opened database successfully")
    c = conn.cursor()
    c.execute('''CREATE TABLE POPULATION
           (ID INT PRIMARY KEY     NOT NULL,
            year INT NOT NULL,
            total INT NOT NULL,
            men INT NOT NULL,
            women INT NOT NULL);''')
    print("Population Table Created!")
    conn.commit()
    conn.close()

    conn = sqlite3.connect('population.db')
    c = conn.cursor()

    for i in range(0,len(year)):
        sql = "INSERT INTO POPULATION (ID, YEAR, TOTAL, MEN, WOMEN) \
        VALUES (%d, %d, %d, %d,%d);" % (i, int(year[i]), int(population[i]), int(men[i]),int(women[i]))
        print(sql)
        c.execute(sql)

    conn.commit()
    print("Records created successfully")
    conn.close()

    # 以上为存储数据库文件部分，下面为读取数据库文件并画图

    year2 = []
    population2 = []
    women2 = []
    men2 = []
    men_proportion = []
    women_proportion = []

    conn = sqlite3.connect('population.db')
    c = conn.cursor()
    c.execute("select * from POPULATION;")
    data = c.fetchall()
    conn.commit()
    conn.close()

    for row in data:
        year2.append(row[1])
        population2.append(row[2])
        men2.append(row[3])
        women2.append(row[4])

    for i in range(0,len(year2)):
        men_proportion.append(float(int(men2[i]))/float(int(population2[i])))
        women_proportion.append(float(int(women2[i])) / float(int(population2[i])))

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # 加载中文字体
    my_font = fm.FontProperties(fname="C:\Windows\Fonts\simkai.ttf")

    plt.bar(year2, population2)
    plt.xlabel(u'年份')
    plt.ylabel(u'万人')
    plt.title(u'年末总人口')
    plt.show()

    x, = plt.plot(year2, men_proportion)
    y, = plt.plot(year2, women_proportion)
    plt.legend(handles=[x, y], labels=['男性占比', '女性占比'], loc='lower right', prop=my_font)
    plt.xlabel(u'年份')
    plt.ylabel(u'%')
    plt.title(u'男性与女性人口占比对比')
    plt.show()