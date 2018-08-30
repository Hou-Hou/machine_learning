#!/usr/bin/env python3 
# -*- coding:utf-8 -*-
# Author: Hou-Hou

"""
在源数据集合中，有一个^hkosarak.dat文件,它包含将近100万条记录。该文件中的每一行包含某个用户浏览过的新闻
报道。一些用户只看过一篇报道，而有些用户看过2498篇报道。用户和报道被编码成整数
"""

import fpGrowth

parsedDat = [line.split() for line in open('datas/kosarak.dat').readlines()]
initSet = fpGrowth.createInitSet(parsedDat)
myFPtree, myHeaderTab = fpGrowth.createTree(initSet, 100000)
print(myFPtree)
myFreqList = []
fpGrowth.mineTree(myFPtree, myHeaderTab, 100000, set([]), myFreqList)