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
    keyvalue['dfwds'] = '[{"wdcode":"zb","valuecode":"A0203"}]'
    keyvalue['k1'] = str(gettime())

    # 发出请求，使用get方法
    r = requests.post(url, headers=headers, params=keyvalue)

#以上为爬取数据部分，下面是将数据存入数据库文件中

    year = []
    first = []
    second = []
    third = []
    data = json.loads(r.text)
    data_one = data['returndata']['datanodes']
    for value in data_one:
        if 'A020302_sj' in value['code']:
            if (float(value['data']['data'])) != 0:
                year.append(value['code'][-4:])
                first.append(float(value['data']['data']))
        if 'A020303_sj' in value['code']:
            if (float(value['data']['data'])) != 0:
                second.append(float(value['data']['data']))
        if 'A020304_sj' in value['code']:
            if (float(value['data']['data'])) != 0:
                third.append(float(value['data']['data']))


    conn = sqlite3.connect('production.db')
    print("Opened database successfully")
    c = conn.cursor()
    c.execute('''CREATE TABLE PRODUCTION
           (ID INT PRIMARY KEY     NOT NULL,
            year INT NOT NULL,
            first FLOAT NOT NULL,
            second FLOAT NOT NULL,
            third FLOAT NOT NULL);''')
    print("Production Table Created!")
    conn.commit()
    conn.close()

    conn = sqlite3.connect('production.db')
    c = conn.cursor()

    for i in range(0,len(year)):
        sql = "INSERT INTO PRODUCTION (ID, YEAR, FIRST, SECOND, THIRD) \
        VALUES (%d, %d, %f, %f, %f);" % (i, int(year[i]), float(first[i]), float(second[i]),float(third[i]))
        print(sql)
        c.execute(sql)

    conn.commit()
    print("Records created successfully")
    conn.close()

#以上为存储数据库文件部分，下面为读取数据库文件并画图

    year2 = []
    first2 = []
    second2 = []
    third2 = []

    conn = sqlite3.connect('production.db')
    c = conn.cursor()
    c.execute("select * from PRODUCTION;")
    data = c.fetchall()
    conn.commit()
    conn.close()

    for row in data:
        year2.append(row[1])
        first2.append(row[2])
        second2.append(row[3])
        third2.append(row[4])

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # 加载中文字体
    my_font = fm.FontProperties(fname="C:\Windows\Fonts\simkai.ttf")

    x, = plt.plot(year2, first2)
    y, = plt.plot(year2, second2)
    z, = plt.plot(year2, third2)
    plt.legend(handles=[x, y, z], labels=['第一产业', '第二产业', '第三产业'], loc='lower right', prop=my_font)
    plt.xlabel(u'年份')
    plt.ylabel(u'%')
    plt.title(u'十年内三次产业构成变化折线图')
    plt.show()

    labels = '第一产业', '第二产业', '第三产业'
    fracs = [float(int(first2[0])), float(int(second2[0])), float(int(third2[0]))]
    plt.axis('equal')
    plt.title(u'2017年三次产业构成图')
    explode = [0, 0, 0]
    ##autopct ='%.0f%%'是将百分比(0表示取零位小数)显示出来,explode= explode 是将饼图部分凸显出来。#shadow 显示阴影。
    plt.pie(fracs, labels=labels, autopct='%.2f%%', explode=explode)
    plt.show()
