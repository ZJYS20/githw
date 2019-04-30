import requests
import time
import json
import matplotlib.pyplot as plt
import sqlite3


# 用来获得 时间戳
def gettime():
    return int(round(time.time() * 1000))


if __name__ == '__main__':
    "一，请求数据"
    # 用来定义头部
    headers = {}
    # 用来传递参数
    keyvalue = {}
    # 目标网址
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

    # 发出请求，使用get方法，这里使用我们自定义的头部和参数
    r = requests.post(url, headers=headers, params=keyvalue)

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


    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.plot(year, first)
    plt.plot(year, second)
    plt.plot(year, third)
    plt.xlabel(u'年份')
    plt.ylabel(u'%')
    plt.title(u'变化情况')
    plt.show()

    labels = 'first', 'second', 'third'
    fracs = [float(int(first[0])), float(int(second[0])), float(int(third[0]))]
    plt.axis('equal')
    explode = [0, 0, 0]
    ##autopct ='%.0f%%'是将百分比(0表示取零位小数)显示出来,explode= explode 是将饼图部分凸显出来。#shadow 显示阴影。
    plt.pie(fracs, labels=labels, autopct='%.2f%%',explode=explode)
    plt.show()

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