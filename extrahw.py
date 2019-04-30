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
    keyvalue['dfwds'] = '[{"wdcode":"zb","valuecode":"A0301"}]'
    keyvalue['k1'] = '1556605507553'#str(gettime())

    # 发出请求，使用get方法，这里使用我们自定义的头部和参数
    r = requests.get(url, headers=headers, params=keyvalue)

    year = []
    population = []
    men = []
    women = []
    men_proportion = []
    women_proportion = []
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

    for i in range(0,len(year)):
        men_proportion.append(float(int(men[i]))/float(int(population[i])))
        women_proportion.append(float(int(women[i])) / float(int(population[i])))

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

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.bar(year, population)
    plt.xlabel(u'年份')
    plt.ylabel(u'万人')
    plt.title(u'年末总人口')
    plt.show()

    plt.plot(year, men_proportion)
    plt.plot(year, women_proportion)
    plt.xlabel(u'年份')
    plt.ylabel(u'%')
    plt.title(u'男性与女性人口占比对比')
    plt.show()