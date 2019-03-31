import requests
import json
import pandas as pd
import matplotlib.pyplot as plt

from main import Weather

appcode = '21753a4c6306468aa91b0ed3b0920bbd'

cityname_dict = {}
dfs = get_dfs(cityname_dict, appcode)
# df = pd.DataFrame(content_json['data']['forecast'])
plt.show()
