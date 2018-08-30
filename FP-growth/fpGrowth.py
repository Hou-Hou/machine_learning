#!/usr/bin/env python3 
# -*- coding:utf-8 -*-
# Author: Hou-Hou

#  FP树中节点的类定义
class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None  # 用于链接相似的元素项
        self.parent = parentNode  # 指向父节点的指针
        self.children = {}

    def inc(self, numOccur):
        self.count += numOccur

    def disp(self, ind=1):  # 将树以文本形式显示
        print(" " * ind, self.name, " ", self.count)
        for child in self.children.values():
            child.disp(ind+1)


# ================FP树构建函数=============================
def createTree(dataSet, minSup=1):
    headerTable = {}
    for trans in dataSet:  # 遍历一遍扫描数据集并统计每个元素项出现的频度
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]   # + dataSet[trans]？？？

    for k in list(headerTable.keys()):
        if headerTable[k] < minSup:  # 移除不满足最小支持度的元素项
            del headerTable[k]

    freqItemSet = set(headerTable.keys())   # 频繁1项集
    if len(freqItemSet) == 0:  # 没有元素退出
        return None, None

    for k in headerTable:
        headerTable[k] = [headerTable[k], None]  # 扩展头指针表，第一个元素保存计数，第二个元素指向第一个元素项
    retTree = treeNode("Null Set", 1, None)      # 建立根节点

    for tranSet, count in dataSet.items():  # 第二遍，遍历数据集，对每条记录进行处理
        localD = {}
        for item in tranSet:  # 对每条记录中的各个子项赋予其支持度，用于排序
            if item in freqItemSet:  # 若记录在频繁1项集中
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda e: e[1], reverse=True)]  # 对频繁1项集按支持度递减排序
            updateTree(orderedItems, retTree, headerTable, count)  # 排序后，对树进行填充
    return retTree, headerTable

# inTree每个节点的父节点
def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:  # 测试第一个元素项是否作为子节点存在。如果存在的话，则更新该元素项的计数
        inTree.children[items[0]].inc(count)
    else:
        inTree.children[items[0]] = treeNode(items[0], count, inTree)  # 如果不存在，则创建一个新的treeNode并将其作为一个子节点添加到树中
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]  # 树上的新的节点的值更新
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])  # 如果节点已经有了，这两个进行链接下
    if len(items) > 1:
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)  # 添加了首节点，递归添加剩下的节点


# 确保节点链接指向树中该元素项的每一个实例
def updateHeader(nodeToTest, targetNode):
    while nodeToTest.nodeLink != None:
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


# ========简单数据集及数据包装器================================
def loadSimpDat():   # 返回一个事务列表
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat


def createInitSet(dataSet):   # 实现上述从列表到字典的类型转换
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict


# ---------------------------------------------
# --------从一棵FP树中挖掘频繁项集-------------
# ---------------------------------------------

# =========发现以给定元素项结尾的所有路径的函数=================
def ascendTree(leafNode, prefixPath):
    if leafNode.parent != None:  # 迭代上溯整颗树
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)


def findPrefixPath(basePat, treeNode):
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats


# ===============递归查找频繁项集的mineTree函数=================
# 为每一个条件模式基创建对应的条件FP树
# inTree和headerTable是由createTree()函数生成的数据集的FP树
# preFix请传入一个空集合（set([])），将在函数中用于保存当前前缀
# freqItemList请传入一个空列表（[]），将用来储存生成的频繁项集
def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda e: e[1][0])]  # 从头指针表的底端开始

    for basePat in bigL:  # bigL为头指针，basePat为“t”,"r"等等
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])  # 创建条件模式基
        # print('basePat', basePat, '的', 'condPattBases条件模式集为：', condPattBases)

        myCondTree, myHead = createTree(condPattBases, minSup)  # 以条件模式基构建条件FP树，得到的结果用于下一次迭代

        if myHead != None:  # myHead由createTree函数得到，本质是头指针表变量
            print("conditional tree for: ", newFreqSet)
            myCondTree.disp(1)
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)
    return freqItemList