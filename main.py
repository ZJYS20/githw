import requests
import json
import pandas as pd
import matplotlib.pyplot as plt

from homework import Weather
from homework import view

city_dict = {"2":"北京","39":"上海","394":"洛阳"}
appcode = '21753a4c6306468aa91b0ed3b0920bbd'
token = '''677282c2f1b3d718152c4e25ed434bc4'''

index=input("请输入选择的模式：1或2\n")
if int(index) == 1:
    prompt = "\nPlease enter the city you want to search:"
    prompt += "\nEnter 'quit' to end the program\n"
    city = ""
    city = input(prompt)
    while city != 'quit':
        repo = Weather(city, appcode, token)   #创建实例
        print(repo.get_weather())   #打印显示
        pd.set_option('display.max_columns', None)
        city = input(prompt)
else:
    print(view(city_dict, appcode, token))
    pd.set_option('display.max_columns', None)
