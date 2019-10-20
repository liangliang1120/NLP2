# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 09:56:22 2019
理论题目
@author: us
"""
'''
2. 回答以下理论题目
2.1 What conditions are required to make the BFS return the optimal solution ?
Ans:cost要大于等于0 ；要把维护的list按照cost进行排序       


2.2 Is there a way to make DFS find the optimal solution ?
    (You may need to read some material about iterative DFS)
Ans:可以把所有路径都走一遍，寻找最优解。
    获取解之后标记，不用恢复初始状态，直到找出所有解，可以比较得出最优解。


2.3 In what conditions BFS is a better choice than DFS and vice versa ?
Ans:求解“是否有解”之类的问题最好用DFS；求解“最优”、“最短距离”等问题用BFS
    BFS适用于节点的子节点个数不多，并且树的层次不会太深的情况。反之可以选择DFS
    
    
2.4 When can we use machine learning ?
Ans:1网购推荐；2发电厂预测发电量；3人脸识别；4语音识别；5无人驾驶

2.5 What is the gradient of a function ?
Ans:为了求loss最小要用到梯度下降。函数在某一点的梯度就是函数在改点的最快下降方向的偏导。
    x=x-α（Δy/Δx)
    沿着梯度方向走可以使y越来越小。
    learning rate太大可能出现震荡，找不到最低点；太小可能会学习太慢，优化很慢

2.6 How can we find the maximum value of a function using the information of gradient ?
Ans:可以在函数前加上负号；或者修改梯度函数x=x+α（Δy/Δx)，相当于梯度上升。
'''
