# -*- coding: utf-8 -*-
# /usr/bin/python
# 作者：Slash
# 实验日期：20200119
# Python版本：3.7
# 主题：基于深度优先和宽度优先的搜索算法的简单实现

import pandas as pd
from pandas import Series, DataFrame

# 城市信息：city1 city2 path_cost
_city_info = None

# 按照路径消耗进行排序的FIFO,低路径消耗在前面
_frontier_priority = []


# 节点数据结构
class Node:
    def __init__(self, state, parent, action, path_cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost


def main():
    global _city_info
    import_city_info()
    
    while True:
        src_city = input('input src city\n')
        dst_city = input('input dst city\n')
        #得到某个result,子节点.state=dst_city
        result = breadth_first_search(src_city, dst_city)
        if not result:
            print('from city: %s to city %s search failure' % (src_city, dst_city))
        else:
            print('from city: %s to city %s search success' % (src_city, dst_city))
            path = []
            #这是一个回溯的过程，将result的状态从目的地到原点一步步添加到path
            while True:
                path.append(result.state)
                if result.parent is None:
                    break
                result = result.parent
            size = len(path)
            for i in range(size):
                if i < size - 1:
                    #print()默认打印一行且后面加换行，end=''意为末尾不换行
                    print('%s->' % path.pop(), end='')
                else:
                    print(path.pop())


def import_city_info():
    global _city_info
    data = [{'city1': 'Oradea', 'city2': 'Zerind', 'path_cost': 71},
            {'city1': 'Oradea', 'city2': 'Sibiu', 'path_cost': 151},
            {'city1': 'Zerind', 'city2': 'Arad', 'path_cost': 75},
            {'city1': 'Arad', 'city2': 'Sibiu', 'path_cost': 140},
            {'city1': 'Arad', 'city2': 'Timisoara', 'path_cost': 118},
            {'city1': 'Timisoara', 'city2': 'Lugoj', 'path_cost': 111},
            {'city1': 'Lugoj', 'city2': 'Mehadia', 'path_cost': 70},
            {'city1': 'Mehadia', 'city2': 'Drobeta', 'path_cost': 75},
            {'city1': 'Drobeta', 'city2': 'Craiova', 'path_cost': 120},
            {'city1': 'Sibiu', 'city2': 'Fagaras', 'path_cost': 99},
            {'city1': 'Sibiu', 'city2': 'Rimnicu Vilcea', 'path_cost': 80},
            {'city1': 'Rimnicu Vilcea', 'city2': 'Craiova', 'path_cost': 146},
            {'city1': 'Rimnicu Vilcea', 'city2': 'Pitesti', 'path_cost': 97},
            {'city1': 'Craiova', 'city2': 'Pitesti', 'path_cost': 138},
            {'city1': 'Fagaras', 'city2': 'Bucharest', 'path_cost': 211},
            {'city1': 'Pitesti', 'city2': 'Bucharest', 'path_cost': 101},
            {'city1': 'Bucharest', 'city2': 'Giurgiu', 'path_cost': 90},
            {'city1': 'Bucharest', 'city2': 'Urziceni', 'path_cost': 85},
            {'city1': 'Urziceni', 'city2': 'Vaslui', 'path_cost': 142},
            {'city1': 'Urziceni', 'city2': 'Hirsova', 'path_cost': 98},
            {'city1': 'Neamt', 'city2': 'Iasi', 'path_cost': 87},
            {'city1': 'Iasi', 'city2': 'Vaslui', 'path_cost': 92},
            {'city1': 'Hirsova', 'city2': 'Eforie', 'path_cost': 86}]
            
    _city_info = DataFrame(data, columns=['city1', 'city2', 'path_cost'])
# print(_city_info)


def breadth_first_search(src_state, dst_state):
    global _city_info
    
    node = Node(src_state, None, None, 0)
    frontier = [node]
    explored = []

    while True:
        if len(frontier) == 0:
            return False
        #pop(0)取第一个元素。pop()取最后一个元素。pop(0)类似于popleft()
        node = frontier.pop(0)
        explored.append(node.state)
        # 目标测试
        if node.state == dst_state:
            return node
        if node.parent is not None:
            print('deal node:state:%s\tparent state:%s\tpath cost:%d' % (node.state, node.parent.state, node.path_cost))
        else:
            print('deal node:state:%s\tparent state:%s\tpath cost:%d' % (node.state, None, node.path_cost))
        
        # 遍历子节点
        for i in range(len(_city_info)):
            dst_city = ''
            if _city_info['city1'][i] == node.state:
                dst_city = _city_info['city2'][i]
            elif _city_info['city2'][i] == node.state:
                dst_city = _city_info['city1'][i]
            if dst_city == '':
                continue
            #将dst_city定义为叶子节点，node为父节点，node.path_cost在87行已经定义为0
            child = Node(dst_city, node, 'go', node.path_cost + _city_info['path_cost'][i])
            print('\tchild node:state:%s path cost:%d' % (child.state, child.path_cost))
            if child.state not in explored and not is_node_in_frontier(frontier, child):
                frontier.append(child)
                print('\t\t add child to child')


def is_node_in_frontier(frontier, node):
    for x in frontier:
        if node.state == x.state:
            return True
    return False


if __name__ == '__main__':
    main()
