#!/usr/bin/env python3 
# -*- coding:utf-8 -*-

import treePlotter
from math import log
import operator


# 计算给定数据集的信息熵
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():     #为 所有可能分类创建字典
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob,2)   # 以2为底数求对数
    return shannonEnt

# 创建数据
def createDataSet():
    dataSet = [[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
    lables = ['no surfacing','flippers']
    return dataSet,lables

# 依据特征划分数据集  axis代表第几个特征  value代表该特征所对应的值  返回的是划分后的数据集
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

# 选择最好的数据集(特征)划分方式  返回最佳特征下标
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1   # 特征个数
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0; bestFeature = -1
    for i in range(numFeatures):   # 遍历特征 第i个
        featureSet = set([example[i] for example in dataSet])   # 第i个特征取值集合
        newEntropy= 0.0
        for value in featureSet:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)   # 该特征划分所对应的entropy
        infoGain = baseEntropy - newEntropy
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

# 多数表决的方法决定叶子节点的分类 ----  当所有的特征全部用完时仍属于多类
def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.key():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key = operator.itemgetter(1), reverse = True)  # 排序函数 operator中的
    return sortedClassCount[0][0]

# 创建树的函数代码   python中用字典类型来存储树的结构 返回的结果是myTree-字典
def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):    # 类别完全相同则停止继续划分  返回类标签-叶子节点
        return classList[0]
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)       # 遍历完所有的特征时返回出现次数最多的
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]    # 得到的列表包含所有的属性值
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
    return myTree

def classify(inputTree, featLabels, testVec):
    """classify(给输入的节点进行分类)
    Args:
        inputTree  决策树模型
        featLabels Feature标签对应的名称
        testVec    测试输入的数据
    Returns:
        classLabel 分类的结果值，需要映射label才能知道名称
    """
    firstStr = list(inputTree.keys())[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    print('firstStr:',firstStr,'---','secondDict:',secondDict,'---','featIndex',featIndex)
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key],featIndex,testVec)
            else:
                classLabel = secondDict[key]
    return classLabel


# 决策树的存储
def storeTree(inputTree, filename):   # pickle序列化对象，可以在磁盘上保存对象
    import pickle
    fw = open(filename, 'wb')
    pickle.dump(inputTree, fw)
    fw.close()


def grabTree(filename):               # 并在需要的时候将其读取出来
    import pickle
    fr = open(filename,'rb')
    return pickle.load(fr)


if __name__=='__main__':
    # myDat,lables = createDataSet()
    # print(myDat)
    # print(lables)
    myTree = treePlotter.retrieveTree(1)
    # print(myTree)
    # classify(myTree,lables,[1,0])
    storeTree(myTree,'classifierStorage.txt')
    print(grabTree('classifierStorage.txt'))