# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 09:56:25 2019
复现课程代码1 bfs&dfs
@author: us
"""
import re
'''
regular expression
[a-z] [A-Z]

colou?r: ? zero or one of its previous character

: zero or more of its previous character
 +: one or more .:match any single 
 ^:start of the line $:end of the line | [cat|dog] : cat or dog (da): make the string da like a character

runoo+b，可以匹配 runoob、runooob、runoooooob 等，
+ 号代表前面的字符必须至少出现一次（1次或多次）。

runoo*b，可以匹配 runob、runoob、runoooooob 等，
* 号代表字符可以不出现，也可以出现一次或者多次（0次、或1次、或多次）。

colou?r 可以匹配 color 或者 colour，
? 问号代表前面的字符最多只可以出现一次（0次、或1次）。
'''
coordination_source = """
{name:'兰州', geoCoord:[103.73, 36.03]},
{name:'嘉峪关', geoCoord:[98.17, 39.47]},
{name:'西宁', geoCoord:[101.74, 36.56]},
{name:'成都', geoCoord:[104.06, 30.67]},
{name:'石家庄', geoCoord:[114.48, 38.03]},
{name:'拉萨', geoCoord:[102.73, 25.04]},
{name:'贵阳', geoCoord:[106.71, 26.57]},
{name:'武汉', geoCoord:[114.31, 30.52]},
{name:'郑州', geoCoord:[113.65, 34.76]},
{name:'济南', geoCoord:[117, 36.65]},
{name:'南京', geoCoord:[118.78, 32.04]},
{name:'合肥', geoCoord:[117.27, 31.86]},
{name:'杭州', geoCoord:[120.19, 30.26]},
{name:'南昌', geoCoord:[115.89, 28.68]},
{name:'福州', geoCoord:[119.3, 26.08]},
{name:'广州', geoCoord:[113.23, 23.16]},
{name:'长沙', geoCoord:[113, 28.21]},
//{name:'海口', geoCoord:[110.35, 20.02]},
{name:'沈阳', geoCoord:[123.38, 41.8]},
{name:'长春', geoCoord:[125.35, 43.88]},
{name:'哈尔滨', geoCoord:[126.63, 45.75]},
{name:'太原', geoCoord:[112.53, 37.87]},
{name:'西安', geoCoord:[108.95, 34.27]},
//{name:'台湾', geoCoord:[121.30, 25.03]},
{name:'北京', geoCoord:[116.46, 39.92]},
{name:'上海', geoCoord:[121.48, 31.22]},
{name:'重庆', geoCoord:[106.54, 29.59]},
{name:'天津', geoCoord:[117.2, 39.13]},
{name:'呼和浩特', geoCoord:[111.65, 40.82]},
{name:'南宁', geoCoord:[108.33, 22.84]},
//{name:'西藏', geoCoord:[91.11, 29.97]},
{name:'银川', geoCoord:[106.27, 38.47]},
{name:'乌鲁木齐', geoCoord:[87.68, 43.77]},
{name:'香港', geoCoord:[114.17, 22.28]},
{name:'澳门', geoCoord:[113.54, 22.19]}
"""

l = "color or colour"
pattern = re.compile("colou?r")
pattern.findall(l)

def get_city_info(city_coordination):
    # 将coordination_source整理为格式化数据
    city_location = {}
    for line in city_coordination.split("\n"):
        # 跳过部分
        if line.startswith("//"): continue
        if line.strip() == "":continue
            
        city = re.findall("name:'(\w+)'",line)[0]
        # \w  匹配字母、数字、下划线。等价于'[A-Za-z0-9_]'
        x_y = re.findall("Coord:\[(\d+.\d+),\s(\d+.\d+)\]",line)[0]
        # \d  匹配一个数字字符。等价于 [0-9]  \s  匹配任何空白字符，包括空格、制表符、换页符等等
        x_y = tuple(map(float,x_y))
        city_location[city] = x_y
    return city_location

city_info = get_city_info(coordination_source)

# ============ Compute distance between cities=================================
import math

def geo_distance(origin, destination):
    """
    Calculate the Haversine distance.
    通过经纬度计算城市间距离（拷贝）

    Parameters
    ----------
    origin : tuple of float
        (lat, long)
    destination : tuple of float
        (lat, long)

    Returns
    -------
    distance_in_km : float

    Examples
    --------
    >>> origin = (48.1372, 11.5756)  # Munich
    >>> destination = (52.5186, 13.4083)  # Berlin
    >>> round(distance(origin, destination), 1)
    504.2
    """
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1) # 将角度转换为弧度
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)) #返回给定的 X 及 Y 坐标值的反正切值
    d = radius * c

    return d

def get_city_distance(city1,city2):
    return geo_distance(city_info[city1],city_info[city2])

c = get_city_distance("杭州","上海")
print(c)

#-==========================Draw the graph=====================================
import networkx as nx #用python构建复杂网络
import matplotlib.pyplot as plt

#%matplotlib inline
'''
G = nx.Graph() # 创建无向图
G.add_node('a')                  #添加一个节点1
G.add_nodes_from(['b','c','d','e'])    #加点集合
G.add_cycle(['f','g','h','j'])         #加环

G = nx.DiGraph() # 创建有向图

G = nx.MultiGraph() # 创建多重无向图

G = nx.MultiDigraph() # 创建多重有向图

G.clear() #清空图
'''

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

city_info.keys()
city_graph = nx.Graph() # 创建无向图
city_graph.add_nodes_from(list(city_info.keys()))#加点集合
nx.draw(city_graph, city_info, with_labels=True, node_size=10)
#draw(G[, pos, ax, hold])

 
#Build connection between. 
#Let's assume that two cities are connected if their distance is less than 700 km.
threshold = 700   # defined the threshold
from collections import defaultdict
def build_connection(city_info):
    cities_connection = defaultdict(list) #提供默认值
    cities = list(city_info.keys())
    for c1 in cities:
        for c2 in cities:
            if c1 == c2 : continue
            # 两两比较，遇到相同的跳过
            if get_city_distance(c1,c2) < threshold:
                cities_connection[c1].append(c2)
    return cities_connection

cities_connection = build_connection(city_info)
#获取某城市与其相连的城市
cities_connection

#=========================Draw connection graph================================
cities_connection_graph = nx.Graph(cities_connection) # 创建无向图,有连接
nx.draw(cities_connection_graph,city_info,with_labels=True,node_size=10)
#==========================BFS 1 version========================================
def search_1(graph,start,destination):
    pathes = [[start]]
    visited = set()
    
    while pathes:
        path = pathes.pop(0) #弹出元素
        froniter = path[-1]
        
        if froniter in visited: continue
            
        successsors = graph[froniter]
        
        for city in successsors:
            if city in path: continue  # check loop
            
            new_path = path+[city]
            
            pathes.append(new_path)  # bfs
            #pathes = [new_path] + pathes #****************dfs*****************
            
            if city == destination:
                return new_path
        visited.add(froniter)

c = search_1(cities_connection,"上海","香港")
print(c)

#==================Optimal search using variation of BFS=======================
def search_2(graph,start,destination,search_strategy):
    pathes = [[start]]  #维护的list
    #visited = set()   #是否经历过，有过就不用搜索了，这里重排，有visited可能找不到最优解
    while pathes:
        path = pathes.pop(0)#把第一个路径拿出来
        froniter = path[-1]#看这条路径中最后的点是否连接其他的点
        #if froniter in visited : continue
        #if froniter == destination:
        #    return path
        successsors = graph[froniter]#把连接的点放入successors
        
        for city in successsors:
            if city in path: continue  # check loop
            
            new_path = path+[city]
            
            pathes.append(new_path)  #bfs
            
        pathes = search_strategy(pathes)
       # visited.add(froniter)
        if pathes and (destination == pathes[0][-1]):
            # 这条路经过重排之后是最短的 并且最后一个点是终点
            # 如果最优解经过重排正好在第二个有visited会遗漏
            # 例子：上海-》香港，如果有visited会找不到最优
            return pathes[0]  

def sort_by_distance(pathes):
    def get_distance_of_path(path):
        distance = 0
        for i,_ in enumerate(path[:-1]):
            distance += get_city_distance(path[i],path[i+1])
        return distance
    return sorted(pathes,key=get_distance_of_path)        
        
def get_distance_of_path(path):
    distance = 0
    for i,_ in enumerate(path[:-1]):
        distance += get_city_distance(path[i],path[i+1])
    return distance

c = get_distance_of_path(["北京","济南","上海"])
print(c)
x = search_2(cities_connection,"北京","上海",search_strategy=sort_by_distance)
print(x)


