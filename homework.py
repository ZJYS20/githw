import requests
import json
import pandas as pd

class Weather():
    def get_df(cityId, cityname_dict, appcode):
        token = '''677282c2f1b3d718152c4e25ed434bc4'''
        appcode = '21753a4c6306468aa91b0ed3b0920bbd'
        url = 'http://freecityid.market.alicloudapi.com/whapi/json/alicityweather/briefforecast3days'
        payload = {'cityId': cityId, 'token': token}
        headers = {'Authorization': 'APPCODE {}'.format(appcode)}
        r = requests.post(url, params=payload, headers=headers)
        content_json = json.loads(r.content)
        df = pd.DataFrame(content_json['data']['forecast'])
        df['cityname'] = cityname_dict[cityId]
        return df


    def get_dfs(cityname_dict, appcode):
        dfs = []
        for cityId in cityname_dict:
            dfs_times = []
            temp_df = get_df(cityId, cityname_dict, appcode)
            dfs_times.append(temp_df)
            city_df = pd.concat(dfs_times,ignore_index=True)
            dfs.append(city_df)
        return dfs
