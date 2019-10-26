# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 21:43:29 2019
使用bfs和dfs搜索从一个站点到达另一个站点的路线
Build the search agent
or example, if you use Beijing subway graoh, and you run:
>>> search("奥体中心“，”天安门“）
You should get the result as follows: 奥体中心 -> A ->B ->C ... -> 天安门
@author: us
"""
import sh_subway_con 


def bfs(graph,start,destination):
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
            #pathes = [new_path] + pathes #dfs
            
            if city == destination:
                return new_path
        visited.add(froniter)

def dfs(graph,start,destination):
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
            
            #pathes.append(new_path)  # bfs
            pathes = [new_path] + pathes #dfs
            
            if city == destination:
                return new_path
        visited.add(froniter)


if __name__=='__main__':           
    
    url = "http://sh.bendibao.com/ditie/"
    dict_line = sh_subway_con.get_line_station(url)
    station_con = sh_subway_con.build_connection(dict_line)

    c = bfs(station_con,"临平路","桂林路")
    print("临平路=>桂林路 bfs路线:",str(c)) # 相当于找到所坐站数最少的
    
    c = dfs(station_con,"临平路","桂林路")
    print("临平路=>桂林路 dfs路线:",str(c))
    
    '''
    结果
    临平路=>桂林路 bfs路线: ['临平路', '海伦路', '宝山路', '上海火车站', '汉中路', '南京西路', '静安寺', '江苏路', '徐家汇', '宜山路', '桂林路']
    临平路=>桂林路 dfs路线: ['临平路', '海伦路', '邮电新村', '四平路', '曲阳路', '虹口足球场', '西藏北路', '中兴路', '曲阜路', '天潼路', '国际客运中心', '提篮桥', '大连路', '江浦公园', '宁国路', '隆昌路', '爱国路', '复兴岛', '东陆路', '巨峰路', '杨高北路', '金京路', '申江路', '金海路', '金吉路', '金桥', '台儿庄路', '蓝天路', '芳甸路', '杨高中路', '世纪大道', '商城路', '小南门', '陆家浜路', '马当路', '新天地', '淮海中路', '南京西路', '自然博物馆', '汉中路', '江宁路', '长寿路', '武宁路', '隆德路', '金沙江路', '中山公园', '延安西路', '虹桥路', '交通大学', '徐家汇', '上海游泳馆', '龙华', '龙华中路', '大木桥路', '嘉善路', '陕西南路', '常熟路', '肇嘉浜路', '东安路', '上海体育场', '上海体育馆', '漕宝路', '龙漕路', '漕溪路', '宜山路', '桂林路']
    '''
