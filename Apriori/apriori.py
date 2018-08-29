#!/usr/bin/env python3 
# -*- coding:utf-8 -*-
# Author: Hou-Hou

# 作用：创建测试数据集
# 输入：无
# 输出：数据集
def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]


# ------------------------
# 构建频繁项集
# ------------------------

# 作用：构建所有候选项集的集合
# 输入：数据集
# 输出：所有候选项集的集合
def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    # frozenset对C1中每个项构建一个不变集合，之后可以将这些集合作为字典键值使用
    return map(frozenset, C1)  # forzenset()是冻结的集合，是不可变的，存在哈希值


# 作用：找出满足最低要求的相集
# 输入：数据集，候选项集列表，感兴趣项集的最小支持度
# 输出：满足最低要求的相集
def scanD(D, Ck, minSupport):    # 注意：-----python3中， for循环遍历D和Ck时，D和Ck必须为list，为map时会出错
    # print('D--:',list(D))
    ssCnt = {}
    D = list(D)
    Ck = list(Ck)
    # 如果Ck是D的一部分，则增加字典中对应的计数值
    for tid in D:   # 遍历数据集中每条数据
        for can in Ck:
            if can.issubset(tid):  # A.issubset(B),判断集合A是不是集合B的子集
                # if not ssCnt.has_key(can):   has_key方法在python2中是可以使用的，在python3中删除了
                #  dict.has_key(key)，has_key() 函数用于判断键是否存在于字典中，如果键在字典dict里返回true，否则返回false
                if not can in ssCnt:
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    # numItems = float(len(D)) In Python 3, map returns a map object not a list,计算长度len(),会报错：
    # TypeError: object of type 'map' has no len()
    numItems = float(len(D))  # 数据集的项数
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key] / numItems  # 计算支持度
        if support >= minSupport:
            retList.insert(0, key)  # 在列表的首部插入新的集合
        supportData[key] = support  # 保存候选集中每条记录及其支持度
    return retList, supportData


# 作用：创建候选项集Ck
# 输入：频繁项集列表Lk，项集元素个数k
# 输出：候选项集Ck
def aprioriGen(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        # j从i+1开始，防止出现j小于i的情况，多建立相同候选项集
        for j in range(i + 1,lenLk):
            # 前k-2个项相同时，将两个集合合并
            L1 = list(Lk[i])[:k - 2]
            L2 = list(Lk[j])[:k - 2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    return retList


# 作用：找出数据集的频繁项集
# 输入：数据集，感兴趣项集的最小支持度
# 输出：频繁项集，项集的支持度值
def apriori(dataSet, minSupport=0.5):
    C1 = createC1(dataSet)
    D = map(set, dataSet)
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]  # L将包含满足最小支持度，即经过筛选的所有频繁n项集，这里添加频繁1项集
    # print('L:', L)
    k = 2
    while len(L[k - 2]) > 0:  # k=2开始，由频繁1项集生成频繁2项集，直到下一个打的项集为空
        Ck = aprioriGen(L[k - 2], k)
        # print('Ck:', Ck)   # 调试
        D1 = map(set, dataSet)      # 为了保证每次调用函数scanD()时不改变原始dataSet表的内容，使用新变量D1代替原始列表。
        Lk, supK = scanD(D1, Ck, minSupport)  # 每次增加频繁项集的大小，Apriori算法都会重新扫描整个数据集D ---- 缺点
        # print('Lk:', Lk)   # 调试
        supportData.update(supK)  # supportData为字典，存放每个项集的支持度，并以更新的方式加入新的supK
        L.append(Lk)
        k += 1
    return L, supportData


# ------------------------
#  挖掘关联规则
# ------------------------
# 作用：关联规则生成主函数
# 输入：频繁项集，项集的支持度值，最小可信度阈值
# 输出：包含可信度的规则列表
# 该函数遍历L中的每一个频繁项集,并对每个频繁项集创建只包含单个元素集合的列表Hl
def generateRules(L, supportData, minConf=0.7):
    bigRuleList = []     # 函数最后要生成一个包含可信度的规则列表，后面可以基于可信度对它们进行排序
    for i in range(1, len(L)):  # 因为无法从单元素项集中构建关联规则，所以要从包含两个或者更多元素的项集开始规则构建过程
        for freqSet in L[i]:  # freqSet = frozenset({2, 3})等L[i]中的元素
            H1 = [frozenset([item]) for item in freqSet]
            # H1将集合freqSet化为集合的列表：如将frozenset({2, 3})转化为[frozenset({2}), frozenset({3})]
            if i > 1:  # 如果频繁项集的元素数目超过2 ，那么会考虑对它做进一步的合并
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            # 只计算i = 1部分
            else:       # 如果项集中只有两个元素，那么使用函数calcCcnf()来计算可信度值
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList

# freqSet：[frozenset({2, 3}), frozenset({3, 5}), frozenset({2, 5}), frozenset({1, 3})], [frozenset({2, 3, 5})]


# 作用：计算可信度
# 输入：freqSet = frozenset({2, 3})；H = [frozenset({2}), frozenset({3})]；
# 输出：
def calcConf(freqSet, H, supportData, br1, minConf=0.7):
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        if conf >= minConf:
            print(freqSet - conseq, '-->', conseq, 'conf:', conf)  # 如果某条规则满足最小可信度值，那么将这些规则输出到屏幕
            br1.append((freqSet - conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH


# 作用：如果频繁项集的元素数目超过2 ，那么对它做进一步的合并
# 输入：频繁项集，可以出现在规则右部的元素列表H
# 输出：
def rulesFromConseq(freqSet, H, supportData, br1, minConf=0.7):
    m = len(H[0])  # 计算频繁集的大小
    if len(freqSet) > (m + 1):
        Hmp1 = aprioriGen(H, m + 1)
        Hmp1 = calcConf(freqSet, Hmp1, supportData, br1, minConf)
        if len(Hmp1) > 1:
            rulesFromConseq(freqSet, Hmp1, supportData, br1, minConf)