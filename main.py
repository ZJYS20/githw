import requests
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

url = 'http://web.juhe.cn:8080/environment/air/cityair?city=hefei&key=d6c360e6a5888b8a4c6d46c8db4ae5a5'
ans = requests.get(url)
print("Status code:",ans.status_code)
response_dict = ans.json()

print('Hefei Air Condition:', response_dict['result'])

dates, AQIs = [], []
for i in range(1,14):
    dates.append(response_dict[''])
    AQIs.append(response_dict[''])

my_style = LS('#333366', base_style = LCS)

my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.title_font_size = 24
my_config.label_font_size = 14
my_config.major_label_font_size = 18
my_config.truncate_label = 15
my_config.show_y_guides = False
my_config.width = 1000

chart = pygal.Bar(my_config, style=my_style)
chart.title = 'Hefei Air Condition in Last Two Weeks '
chart.x_labels = dates

chart.add('', AQIs)
chart.render_to_file('results.svg')

