#!/usr/bin/env python3 
# -*- coding:utf-8 -*-
# Author: Hou-Hou

import apriori

if __name__ == '__main__':

    # C1 = apriori.createC1(dataSet)
    # L1, suppData0 = apriori.scanD(dataSet, list(C1), 0.5)
    # print('L1:', L1)
    # print('supData:', suppData0)

    dataSet = apriori.loadDataSet()
    L,suppData = apriori.apriori(dataSet)
    print('L:', L)
    rules = apriori.generateRules(L, suppData, minConf=0.5)

