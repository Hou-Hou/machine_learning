#!/usr/bin/env python3 
# -*- coding:utf-8 -*-

import treePlotter
import trees

if __name__ == '__main__':
    myTree = treePlotter.retrieveTree(1)
    # print(myTree)
    # classify(myTree,lables,[1,0])
    trees.storeTree(myTree,'classifierStorage.txt')
    print(trees.grabTree('classifierStorage.txt'))

    fr = open('lenses.txt')
    lenses = [inst.strip().split('\t') for inst in fr.readlines()]
    lensesLabels = ['age', 'prescript', 'astigmatic', 'tear_rate']
    lensesTree = trees.createTree(lenses, lensesLabels)
    print(lensesTree)
    treePlotter.createPlot(lensesTree)