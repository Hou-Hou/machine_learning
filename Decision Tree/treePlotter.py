#!/usr/bin/env python3 
# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt

# ------使用文本注解绘制树节点------
decisionNode = dict(boxstyle="sawtooth",fc="0.8")  # boxstyle为文本框的类型，sawtooth是锯齿形，fc是边框线粗细
leafNode = dict(boxstyle="round4",fc="0.8")
arrow_args = dict(arrowstyle="<-")

# 绘制带箭头的注解
# nodeTxt：节点的文字标注, centerPt：节点中心位置，
# parentPt：箭头起点位置（上一节点位置）, nodeType：节点属性
def plotNode(nodeTxt,centerPt,parentPt,nodeType):
    '''
    下面这个函数原型是class matplotlib.axes.Axes()的成员函数annotate()
    该函数的作用是为绘制的图上指定的数据点xy添加一个注释nodeTxt, 注释的位置由xytext指定
    创建一个描述  annotate(s, xy, xytext=None, xycoords='data',textcoords='data', arrowprops=None, **kwargs)
    s : 描述的内容
    xy : 加描述的点
    xytext : 标注的位置，xytext=(30,-30),表示从标注点x轴方向上增加30，y轴方向上减30的位置
    xycoords 、textcoords: xycoords来指定点xy坐标的类型，textcoords指定xytext的类型，xycoords和textcoords的取值如下：
        ‘figure points’：此时坐标表示坐标原点在图的左下角的数据点
        ‘figure pixels’：此时坐标表示坐标原点在图的左下角的像素点
        ‘figure fraction’：此时取值是小数，范围是([0, 1], [0, 1])
                             ，在图的最左下角时xy是(0, 0), 最右上角是(1, 1)
                            ，其他位置按相对图的宽高的比例取小数值
        ‘axes points’：此时坐标表示坐标原点在图中坐标的左下角的数据点
        ‘axes pixels’：此时坐标表示坐标原点在图中坐标的左下角的像素点
        ‘axes fraction’：类似‘figure fraction’，只不过相对图的位置改成是相对坐标轴的位置
        ‘data’：此时使用被注释的对象所采用的坐标系（这是默认设置），被注释的对象就是调用annotate这个函数
                 那个实例，这里是ax1，是Axes类，采用ax1所采用的坐标系
       ‘offset points’：此时坐标表示相对xy的偏移（以点的个数计），不过一般这个是用在textcoords
       ‘polar’：极坐标类型，在直角坐标系下面也可以用，此时坐标含义为(theta, r)
    fontsize : 字体大小，这个没什么好说的
    arrowstyle : 箭头样式'->'指向标注点 '<-'指向标注内容 还有很多'-'
                '->' 	head_length=0.4,head_width=0.2
                '-[' 	widthB=1.0,lengthB=0.2,angleB=None
                '|-|' 	widthA=1.0,widthB=1.0
                '-|>' 	head_length=0.4,head_width=0.2
                '<-' 	head_length=0.4,head_width=0.2
                '<->' 	head_length=0.4,head_width=0.2
                '<|-' 	head_length=0.4,head_width=0.2
                '<|-|>' 	head_length=0.4,head_width=0.2
                'fancy' 	head_length=0.4,head_width=0.4,tail_width=0.4
                'simple' 	head_length=0.5,head_width=0.5,tail_width=0.2
    arrowprops：含义为连接数据点和注释的箭头的类型，该参数是dictionary类型，该参数含有一个名为arrowstyle的键，
            一旦指定该键就会创建一个class matplotlib.patches.FancyArrowPatch类的实例
            该键取值可以是一个可用的arrowstyle名字的字符串，也可以是可用的class matplotlib.patches.ArrowStyle类的实例
            具体arrowstyle名字的字符串可以参考http: // matplotlib.org / api / patches_api.html  # matplotlib.patches.FancyArrowPatch
            里面的class matplotlib.patches.FancyArrowPatch类的arrowstyle参数设置
            函数返回一个类class matplotlib.text.Annotation()的实例
    '''
    createPlot.ax1.annotate(nodeTxt,xy=parentPt,xycoords='axes fraction',xytext=centerPt,
                            textcoords='axes fraction',va="center",ha="center",
                            bbox=nodeType,arrowprops=arrow_args)

# def createPlot():
#     fig = plt.figure(1,facecolor='white')
#     fig.clf()
#     createPlot.ax1 = plt.subplot(111,frameon=False)
#     plotNode('a decision node',(0.5,0.1),(0.1,0.5),decisionNode)
#     plotNode('a leaf node',(0.8,0.1),(0.3,0.8),leafNode)
#     plt.show()

# --------获取叶节点的数目和树的层数---------
def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            numLeafs += getNumLeafs(secondDict[key])
        else:
            numLeafs += 1
    return numLeafs

def getTreeDepth(myTree):
    maxDepth = 0                          # myTree: {'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}}
    firstStr = list(myTree.keys())[0]     # myTree.keys(): ['no surfacing']  list(myTree.keys())[0]: no surfacing
    secondDict = myTree[firstStr]         # {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            thisDepth = 1+ getTreeDepth(secondDict[key])
        else:
            thisDepth = 1
        if thisDepth > maxDepth:
            maxDepth = thisDepth
    return maxDepth

def retrieveTree(i):
    listOfTrees = [{'no surfacing':{0:'no',1:{'flippers':{0:'no',1:'yes'}}}},
                   {'no surfacing':{0:'no',1:{'flippers':{0:{'head':{0:'no',1:'yes'}},1:'no'}}}}
                   ]
    return listOfTrees[i]

# 在父子节点间填充文本信息
# cntrPt:子节点位置, parentPt：父节点位置, txtString：标注内容
def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0]-cntrPt[0])/2.0 + cntrPt[0]
    yMid = (parentPt[1]-cntrPt[1])/2.0 + cntrPt[1]
    createPlot.ax1.text(xMid,yMid,txtString)

# 绘制树形图
# myTree：树的字典, parentPt:父节点, nodeTxt：节点的文字标注
def plotTree(myTree,parentPt,nodeTxt):
    # 计算宽与高
    numLeafs = getNumLeafs(myTree)
    depth = getTreeDepth(myTree)
    firstStr = list(myTree.keys())[0]
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW, plotTree.yOff)
    # 标记子节点属性值
    plotMidText(cntrPt,parentPt,nodeTxt)  # 在父子节点间填充文本信息
    plotNode(firstStr,cntrPt,parentPt,decisionNode)  # 画根节点  #绘制带箭头的注解
    secondDict = myTree[firstStr]
    # 减少y偏移: 按比例减少全局变量plotTree.yOff，并标注此处将要绘制子节点.这些节点即可以是叶子节点也可以是判断节点，此处需要只保存绘制图形的轨迹
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            plotTree(secondDict[key],cntrPt,str(key))  # 递归绘制树形图
        else:
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            plotNode(secondDict[key],(plotTree.xOff,plotTree.yOff),cntrPt,leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0 / plotTree.totalD

# 创建绘图区: createPlot（）是主函数，创建绘图区，计算树形图的尺寸大小，它调用plotTree（）等函数，plotTree（）递归画出整个树形图。
def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plotTree.totalW = float(getNumLeafs(inTree)) # 树的宽度
    plotTree.totalD = float(getTreeDepth(inTree)) # 树的深度
    plotTree.xOff = -0.5/plotTree.totalW; plotTree.yOff = 1.0;
    plotTree(inTree, (0.5,1.0), '')
    plt.show()

if __name__=='__main__':
    myTree = retrieveTree(0)
    createPlot(myTree)

