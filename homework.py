import requests
import json
import pandas as pd

class Weather(object):

    def __init__(self, city, appcode, token):   #初始化发送请求必需的属性
        self.city = city
        self.appcode = appcode
        self.token = token

    def get_weather(self):
        url = 'http://freecityid.market.alicloudapi.com/whapi/json/alicityweather/briefforecast3days'
        payload = {'cityId': self.city, 'token': self.token}
        headers = {'Authorization': 'APPCODE {}'.format(self.appcode)}
        ans_json = requests.post(url, params=payload, headers=headers)   #向API发送请求，ans_json储存返回的数据
        ans = json.loads(ans_json.content)           #将json格式转化为List格式
        repo = pd.DataFrame(ans['data']['forecast'])  #提取其中有用的部分，即forecast，并将其转化为数据框
       # repo['cityname'] = city_dict[city]
        return repo



def get_weather2(city, city_dict, appcode, token):
        url = 'http://freecityid.market.alicloudapi.com/whapi/json/alicityweather/briefforecast3days'
        payload = {'cityId': city, 'token': token}
        headers = {'Authorization': 'APPCODE {}'.format(appcode)}
        ans_json = requests.post(url, params=payload, headers=headers)  # 向API发送请求，ans_json储存返回的数据
        ans = json.loads(ans_json.content)  # 将json格式转化为List格式
        repo = pd.DataFrame(ans['data']['forecast'])  # 提取其中有用的部分，即forecast，并将其转化为数据框
        repo['cityname'] = city_dict[city]
        return repo

def view(city_dict, appcode, token):
    repos = []
    for city in city_dict:
        repos_times = []
        temp_df = get_weather2(city, city_dict, appcode, token)
        repos_times.append(temp_df)
        city_df = pd.concat(repos_times, ignore_index=True)
        repos.append(city_df)
        res = pd.concat(repos, ignore_index=True)
    return res