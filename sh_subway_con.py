# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 12:24:22 2019
上海地铁-构建网络
从上海本地宝 获取站点，构建地铁网络
http://sh.bendibao.com/ditie/
@author: us
"""
from bs4 import BeautifulSoup as bs
import requests
import networkx as nx 
import matplotlib.pyplot as plt
import re 
import time
from subway_location import get_location
import subway_location

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def get_line_station(url):
    # 从网站上爬虫，获取上海地铁有几条线，每条线上有哪些站，每个站可以换乘的线路
    HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer':'https://www.douban.com/accounts/login?source=movie',
    'Cookie':'bid=RD-3z-EM9-U; ap_v=0,6.0; _pk_ses.100001.4cf6=*; __utma=30149280.1286780158.1568533810.1568533810.1568533810.1; __utmc=30149280; __utmz=30149280.1568533810.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; dbcl2="170719751:yMNkbSQ0GIU"; ck=EzrC; _pk_id.100001.4cf6=9c22c3b036952374.1568533809.1.1568533847.1568533809.; __utmt_douban=1; __utmb=30149280.2.10.1568533810; __utma=223695111.1817256674.1568533847.1568533847.1568533847.1; __utmb=223695111.0.10.1568533847; __utmc=223695111; __utmz=223695111.1568533847.1.1.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login; push_noty_num=0; push_doumail_num=0',
    'Connection':'keep-alive Cache-Control: max-age=0'
    }
    
    req = requests.get(url, headers=HEADERS)
    # req.encoding = 'utf8'
    print("Crawling {}".format(url))
    if req.status_code == 200:
        dom = bs(req.text, 'lxml')
        #print(dom)
    container = dom.find('div', {'class': 's-main'})
    container = container.find_all('div', {'class': 'line-list'})
    
    dict_line = {}
    for line in container:
        # 每条地铁线
        line_num = line.find('a', {'target': '_blank'}).text
        
        # line_num = int(re.findall("(\d+)",line_num)[0])
        line_stations = line.find_all('div', {'class': 'station'})
        # 该线的每个station
        list_station = [x.text for x in line_stations]
        list_station_change = []
        
        for x in list_station:
            c = re.findall("(\w+)",x)
            #print(c)
            temp = []
            if c[0] == '你可以在此处换乘':
                for i in range(1,len(c)-1):
                    print(line_num,c[i],c[-1])
                    change_num = re.findall("\w+",c[i])[0]
                    temp.append(change_num)
            list_station_change.append([c[-1],line_num,]+temp)
        dict_line[line_num] = list_station_change
    return dict_line
    
    
url = "http://sh.bendibao.com/ditie/"
dict_line = get_line_station(url)

# 获取所有地铁站的名字
stations = []
for num in dict_line.items():
    print(num[1])
    station = [x[0] for x in num[1]]
    stations = stations + station
    stations = list(set(stations)) #去重
'''
# 获取上海所有地铁站的经纬度 大概耗时6分钟
# 其中金海湖 地铁站API获取的经纬度是错误的，用前后两站的中间数据代替
# 以下直接用获取后的结果

locat_dict = {}
for stat in stations:
    time.sleep(1)  #太快就会返回（0，0）
    temp = get_location1(stat, '上海')
    print(stat,temp)
    locat_dict[stat] = temp
    
# 以下为结果
'''
locat_dict = subway_location.locat_dict #这是以上运行的结果

    
#画图（暂未连线）
station_graph = nx.Graph() # 创建无向图
station_graph.add_nodes_from(list(locat_dict.keys()))#加点集合
plt.rcParams['savefig.dpi'] = 150 #图片像素
plt.rcParams['figure.dpi'] = 150 #分辨率
nx.draw(station_graph, locat_dict, with_labels=True, node_size=2,font_size=3)
plt.savefig("sh_subway.png")

#复杂网络，同一条线路的站点相连，可以换乘的相连
def build_connection(dict_line):
    station_con = {}
    for sub_line in dict_line.keys():
        print(sub_line)
        sub_stations = dict_line[sub_line]
        for i in range(len(sub_stations)):
            print(i)
            # 一条线上的站点前后相互连接,终点站做特殊处理
            if i == 0:
                station_con[sub_stations[i][0]] = [sub_stations[i+1][0]]
            elif i == (len(sub_stations)-1):
                station_con[sub_stations[i][0]] = [sub_stations[i-1][0]]
            else:
                station_con[sub_stations[i][0]] = []
                station_con[sub_stations[i][0]] = station_con[sub_stations[i][0]]+[sub_stations[i+1][0]]
                station_con[sub_stations[i][0]] = station_con[sub_stations[i][0]]+[sub_stations[i-1][0]]
    return station_con

#画图（连线）
station_con = build_connection(dict_line)
station_connection_graph = nx.Graph(station_con) # 创建无向图,有连接
plt.rcParams['savefig.dpi'] = 250 #图片像素
plt.rcParams['figure.dpi'] =250 #分辨率
nx.draw(station_connection_graph,locat_dict,with_labels=True,\
        node_size=2,font_size=2.5,width=0.3,node_color='y')
plt.savefig("sh_subway_con.png")
    
    
    
    
    
    
    
    