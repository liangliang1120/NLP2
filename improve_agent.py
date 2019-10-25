# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 22:45:49 2019
(Optional) Improve your agent to make it able to find a path based on different strategies
a. Find the shortest path between two stations.
b. Find the path that requires minimum transfers between two stations.
c. Combine the previous two ideas, find a more suitable path.
@author: us
"""
import sh_subway_con
import math
import subway_location

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

def sort_by_distance(pathes):
    def get_distance_of_path(path):
        distance = 0
        for i,_ in enumerate(path[:-1]):
            distance += get_stat_distance(path[i],path[i+1])
        #print(path, distance)
        return distance
    #print(sorted(pathes,key=get_distance_of_path))
    return sorted(pathes,key=get_distance_of_path)        
        
def get_distance_of_path(path):
    distance = 0
    for i,_ in enumerate(path[:-1]):
        distance += get_stat_distance(path[i],path[i+1])
    return distance

def bfs_lenth(graph,start,destination,search_strategy):
    # Find the shortest path between two stations.
    pathes = [[start]]  #维护的list
    while pathes:
        path = pathes.pop(0)#把第一个路径拿出来
        froniter = path[-1]#看这条路径中最后的点是否连接其他的点
        successsors = graph[froniter]#把连接的点放入successors
        
        for city in successsors:
            if city in path: continue  # check loop
            
            new_path = path+[city]
            
            pathes.append(new_path)  #bfs
            
        pathes = search_strategy(pathes)

        if pathes and (destination == pathes[0][-1]):
            return pathes[0] 




def sort_by_transfers(pathes,dict_line):
    def get_transfers_of_path(path,dict_line):
        # 计算路线换乘次数
        stat_dict = {}
        for stat in path:
            stat_dict[stat] = []
        for stat in path:
            print(stat)
            for line in dict_line.keys():
                for statt in dict_line[line]:
                    if stat in statt:
                        stat_dict[stat].append(line)
        transfer_line = []
        for stat in stat_dict:
            try:
                a
            except:
                a = []
            for line in stat_dict[stat]:
                #print(line)
                if line in a:
                    b = line
                    #print('不换乘',line)
                    transfer_line.append(b)
                    #print('transfer_line ',transfer_line)
            a = stat_dict[stat]
            #print('a',a,stat)
        transfer_num = len(set(transfer_line))
        print('transfer_num',transfer_num)
        return transfer_num
    
    path_transfer_num = {}
    for path in pathes:
        path_transfer_num[str(path)] = get_transfers_of_path(path,dict_line)
    print(path_transfer_num)    
    sorted_way_dict = sorted(path_transfer_num.items(), key=lambda item: item[1], reverse=False)
    sorted_way = []
    for key in sorted_way_dict:
        sorted_way.append(eval(key[0]))
    print('sorted_way',sorted_way)
    return sorted_way

def bfs_transfer(graph,start,destination,dict_line,search_strategy):
    # Find the minium transfers between two stations. 
    pathes = [[start]]  #维护的list
    while pathes:
        path = pathes.pop(0)#把第一个路径拿出来
        froniter = path[-1]#看这条路径中最后的点是否连接其他的点
        successsors = graph[froniter]#把连接的点放入successors
        
        for city in successsors:
            if city in path: continue  # check loop
            print(city)
            new_path = path+[city]
            print(new_path)
            pathes.append(new_path)  #bfs
        #print(pathes)    
        pathes = search_strategy(pathes,dict_line)
        #print('kkk',pathes) 
        if pathes and (destination == pathes[0][-1]):
            return pathes[0] 
        
url = "http://sh.bendibao.com/ditie/"
dict_line = sh_subway_con.get_line_station(url)
station_con = sh_subway_con.build_connection(dict_line)
locat_dict = subway_location.locat_dict

def get_stat_distance(stat1,stat2):
    return geo_distance(locat_dict[stat1],locat_dict[stat2])
#以下10号线和11号线，重合站点支线去重,以免换乘次数增加
line10_stat = ['新江湾城','殷高东路','三门路','江湾体育场','五角场','国权路',
             '同济大学','四平路','邮电新村','海伦路','四川北路','天潼路','南京东路',
             '豫园','老西门','新天地','陕西南路','上海图书馆','交通大学',
             '虹桥路','宋园路','伊犁路','水城路','龙溪路']
line11_stat = ['罗山路','御桥','浦三路','三林东','三林','东方体育中心','龙耀路',
               '云锦路','龙华','上海游泳馆','徐家汇','交通大学','江苏路','隆德路',
               '曹杨路','枫桥路','真如','上海西站','李子园','祁连山路','武威路',
               '桃浦新村','南翔','马陆','嘉定新城']

temp = dict_line['上海地铁10号线支线'].copy()
for stat in dict_line['上海地铁10号线支线']:
    if stat[0] in line10_stat:
        temp.remove(stat)
dict_line['上海地铁10号线支线'] = temp

temp = dict_line['上海地铁11号线支线'].copy()
for stat in dict_line['上海地铁11号线支线']:
    if stat[0] in line11_stat:
        temp.remove(stat)
dict_line['上海地铁11号线支线'] = temp
#dict_line['上海地铁10号线支线'] = list(set(dict_line['上海地铁10号线支线']).difference(set(line10_stat)))
#dict_line['上海地铁11号线支线'] = list(set(dict_line['上海地铁11号线支线']).difference(set(line11_stat)))
'''
for stat in stat_dict:
    if stat in line10_stat:
        stat_dict[stat] = [x for x in stat_dict[stat] if x != '上海地铁10号线支线']
    if stat in line11_stat:
        stat_dict[stat] = [x for x in stat_dict[stat] if x != '上海地铁11号线支线']
'''
#c=get_stat_distance('临平路','桂林路')

#c = get_distance_of_path(['临平路', '海伦路', '宝山路', '上海火车站', '汉中路', '南京西路', '静安寺', '江苏路', '徐家汇', '宜山路', '桂林路'])

#c = bfs_lenth(station_con,"临平路","天潼路",search_strategy=sort_by_distance)
#print("临平路=>桂林路 dfs距离最短路线:",str(c))
# 用bfs计算最短路程的线路，由于节点较多（344个），层次较深，所以运行起来特别慢，
# 十几站的路线站跑了24小时还没出结果，测试用较短路线进行
# 结果: 临平路=>桂林路 dfs路线: ['临平路', '海伦路', '四川北路', '天潼路']


#c = get_transfers_of_path(['中山北路','上海火车站','汉中路','曲阜路','天潼路','四川北路'],dict_line)
c = bfs_transfer(station_con,"中山北路","四川北路",dict_line,search_strategy=sort_by_transfers)
print("中山北路=>四川北路 dfs最少换乘路线:",str(c))



#Combine the previous two ideas, find a more suitable path.
#相比较而言，我更倾向于选择 换乘少的线路，
#因为路程稍微长一点，由于地铁速度较快，时间上影响不大，而换乘更耗费时间精力。


'''
Compare your results with results obtained by using some apps 
such as Baidu map, A map, Google map or Apple map. If there is difference, 
try to explanate it.

距离的估计和百度地图上还是有些许区别，
例如 临平路=>桂林路，python脚本中用公式算10.444km,app中13.7km
差距的地方：
    1.经纬度不准确；
    2.app中计算的是可行道路的长度，不是公式中的直线距离
    3.app中考虑更多的因素，可以选择（时间短、少换乘、少步行）等
    4.app中还会考虑时间因素
另外app中会实时按照路况更新，例如有按道路拥堵程度、晚间停运等信息更新
'''