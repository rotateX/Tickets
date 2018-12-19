import requests
import re
from pprint import pprint

url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9058'
response = requests.get(url)
stations = dict(re.findall(r'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text))
#pprint(stations, indent=4)
names = stations.keys()
telecodes = stations.values()
#print(names)
#print(telecodes)

