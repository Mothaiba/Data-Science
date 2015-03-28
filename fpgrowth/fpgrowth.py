import numpy as np
import scipy as sp
import math
from Queue import Queue
from collections import defaultdict

"""
    to use, just call the function:
    
                frequent_Pattern_fpGrowth(listOfTrans,min_sup,show_support = False)
                 
    type of 'transactions' is array of arrays ( e.g: [ [1,2,3],[1,2],[3,5,1] ] )
                           or array of tuples ( e.g: [ (1,2,3),(1,2),(3,5,1) ] )
                           
    min_sup can be an int (absolute minimum support)
                or a float ( relative minimum support) - in this case,
                        it will be converted to absolute support
    
    this will return A GENERATOR of (pattern, support)   if show_support == True
                                     pattern             otherwise

"""



"""
    A function to check the progress of writing code
    Here, I print:
        the support of each item
        List of transactions 
        the FPTree
        the itemTrace
"""
maxInt = 0
def check_Progress(data,FPTree,itemsSupport,prioList,itemTrace):
    print '----------------------------------------------------------------------'
    print 'We are checking here'
    print '--------------------------'
    print 'Support of each item: ',itemsSupport.items()
    print 'priority List (ascending): ',prioList
    print 'List of pre-processed transactions: ',data.items()
    q = Queue()
    q.put(FPTree)
    while not q.empty():
        curr= q.get()
        print 'this node is ',curr.name,
        if curr.parent != None:
            print ',it\'s parent is:',curr.parent.name,
        else:
            print ',it doesn\'t have parent',
        print ',',curr.quantity,'transactions through this'
        print 'it has children: ', curr.children.keys()
        for item in curr.children:
            q.put(curr.children[item])
        print '--------------------------'
    print 'Check for itemTrace --------------------------------'
    for key in itemTrace.keys():
        curr = itemTrace[key]
        print 'We are observing item ',curr.now.name
        while curr!=None:
            print 'Node: ',curr.now.name,'that has children:'
            for key in curr.now.children:
                print '   ',curr.now.children[key].name
            curr = curr.next
        print '-----------------------------'

"""
    this function converts list of transactions to dictionary of transactions
"""
def pre_process(Trans):
    dictOfTrans = defaultdict(int)
    for tran in Trans:
        dictOfTrans[tuple(tran)] += 1
    return dictOfTrans


def frequent_Pattern_fpGrowth(listOfTrans,min_sup,show_support = False):
    """ if min_sup is float (i.e the relative minimum support ), automatically convert it
                 to absolute minimum support
    """    
    if type(min_sup)==float:
        min_sup = math.ceil(min_sup*len(listOfTrans))
    """
        maxInt = infinity. It helps mining pattern from FPTree
    """
    global maxInt
    maxInt = len(listOfTrans) + 1
    dictOfTrans = pre_process(listOfTrans)
    frequentPattern = find_pattern(dictOfTrans,min_sup)
    if show_support:
        for pattern_support in frequentPattern:
            if pattern_support != ([],maxInt):            
                yield pattern_support
    else:
        for pattern, support in frequentPattern:
            if pattern != []:
                yield pattern

"""
    Main function, mining frequent pattern from FPTree
"""
def find_pattern(transactions,min_sup):
    if len(transactions) == 0:
        yield [],maxInt
        return
    itemsSupport = getItemsSupport(transactions)
    prioDict,prioList = getItemPriority(itemsSupport,min_sup)
    data = getFilteredData(transactions,prioDict,min_sup)
    FPTree,itemTrace = buildTree(data)
#    check_Progress(data,FPTree,itemsSupport,prioList,itemTrace)
    
    for item in prioList:
        newTrans = defaultdict(int)
        curr = itemTrace[item]
        supOfThisItem = 0
        while True:
            traceNode = curr.now
            times = traceNode.quantity
            supOfThisItem += times
            newTran = []
            while traceNode.parent.name != 'NULL':
                traceNode = traceNode.parent
                newTran.append(traceNode.name)
            if len(newTran) >0:
                newTrans[tuple(newTran)] += times
            if curr.next == None:
                break
            else:
                curr = curr.next

        smallFPattern = find_pattern(newTrans,min_sup)
        for pattern,sub_sup in smallFPattern:
            pattern.append(item)
            yield (pattern,min(sub_sup,supOfThisItem))

    yield [],maxInt
    
def getItemsSupport(transactions):
    """
    count support for each item in all transactions
    """
    itemsSupport = defaultdict(lambda: 0)
    for transaction,times in transactions.items():
        for item in transaction:
            itemsSupport[item] += times
    return itemsSupport

def getFilteredData(transactions,prioDict,min_sup):
    """
    return list of transactions that:
        Removed items that have support < min_sup
        Sort items in each transaction according to their support
    """
    data = defaultdict(int)
    for transaction,times in transactions.items():
        filteredTran = list(filter(lambda item: item in prioDict,transaction))
        filteredTran.sort(key = lambda item: prioDict[item], reverse = True)
        if len(filteredTran) >0:
            data[tuple(filteredTran)] += times    
    return data

class FPNode(object):
    def __init__(self,parent,name,quantity):
        self.name = name
        self.quantity = quantity
        self.children = {}
        self.parent = parent
        
class traceNode(object):
    def __init__(self,treeNode):
        self.next = None
        self.last = self
        self.now = treeNode

"""
    This function return priority of each item as itemPrio
    According to it, we will:
        First, prioDict helps sort items in each transaction by ascending priority
        Second, prioList helps define the order of item in recursion process 
"""
def getItemPriority(itemsSupport,min_sup):
    prioList = sorted(itemsSupport, key = lambda k: itemsSupport[k])
    prioList = filter(lambda item: itemsSupport[item] >= min_sup, prioList)
    prioDict = {} 
    cnt = 0
    for i in prioList:
        prioDict[i]= cnt
        cnt += 1
    return prioDict,prioList

"""
    this function build FPTree
"""
def buildTree(data):
    FPTree = FPNode(None,'NULL',0)    
    itemTrace = {}
    for transaction,times in data.items():
        currNode = FPTree
        for item in transaction:
            if currNode.children.has_key(item):
                currNode = currNode.children[item]
                currNode.quantity += times
            else:
                currNode.children[item] = FPNode(currNode,item,times)
                currNode = currNode.children[item]
                
                if itemTrace.has_key(item):
                    lastTraceItem = itemTrace[item].last
                    lastTraceItem.next = traceNode(currNode)
                    itemTrace[item].last = lastTraceItem.next
                else:
                    itemTrace[item] = traceNode(currNode)
                    
    return FPTree,itemTrace





transList2 =[
    [1,2,3],
    [2,4,1,5],
    [3,1,5]

]
transList = [
    [2,3,4,5],
    [3,6,2,1,5],
    [1,2,5,6],
    [5,6,1,2,7],
    [2,1,3]
]
res = []
gen = frequent_Pattern_fpGrowth(transList2,1)
for p in gen:
    res.append(p)
#res.remove(([],maxInt))
#for pattern,sup in res:
#    pattern.sort()
res.sort()
print 'Frequent Patterns: '
print res
    








