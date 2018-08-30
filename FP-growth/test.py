#!/usr/bin/env python3 
# -*- coding:utf-8 -*-
# Author: Hou-Hou

import fpGrowth

if __name__ == '__main__':
    # rootNode = fpGrowth.treeNode('pyramid', 9, None)
    # rootNode.children['eye'] = fpGrowth.treeNode('eye', 13, None)
    # rootNode.disp()

    simpDat = fpGrowth.loadSimpDat()
    # print('simpDat:', simpDat)

    initSet = fpGrowth.createInitSet(simpDat)
    # print('initSet', initSet)

    myFPtree, myHeaderTab = fpGrowth.createTree(initSet, 3)
    myFPtree.disp()

    freqItems = []
    freqItemList = fpGrowth.mineTree(myFPtree, myHeaderTab, 3, set([]), freqItems)
    print(freqItems)