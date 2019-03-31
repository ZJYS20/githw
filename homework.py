import requests
import pygal


url = 'http://web.juhe.cn:8080/environment/air/cityair?city=hefei&key=d6c360e6a5888b8a4c6d46c8db4ae5a5'
ans = requests.get(url)
print("Status code:",ans.status_code)
response_dict = ans.json()

print('Hefei air condition:', response_dict['result'])
