
# coding: utf-8

# In[24]:

from __future__ import division
import sys
import math
import numpy as np


trainArray = {}

#resultArray = np.zeros((944,1683))
with open('train_all_txt.txt','r') as t:
    for line in t:
        user, item, rating =  line.split()
        trainArray[int(user), int(item)] = int(rating)
###############################################################################################
testArray = {}
with open('recSysTestOut_itemcf.txt','r') as o:
    for line in o:
        user, item, rating =  line.split()
        testArray[int(user), int(item)] = int(rating)

with open('RecSysOutput_itemcf.txt', 'w+') as out:
    for user in range(1,944):
        for item in range(1,1683):
            if (user, item) not in trainArray: 
                out.write('%d %d %d\n' %(user, item,  testArray[user,item]))
            else:
                out.write('%d %d %d\n' %(user, item,  trainArray[user,item]))



###############################################################################################
testArray = {}
with open('recSysTestOut_usercf.txt','r') as o:
    for line in o:
        user, item, rating =  line.split()
        testArray[int(user), int(item)] = int(rating)

with open('RecSysOutput_usercf.txt', 'w+') as out:
    for user in range(1,944):
        for item in range(1,1683):
            if (user, item) not in trainArray: 
                out.write('%d %d %d\n' %(user, item,  testArray[user,item]))
            else:
                out.write('%d %d %d\n' %(user, item,  trainArray[user,item]))

###############################################################################################
testArray = {}
with open('recSysTestOut_userbias.txt','r') as o:
    for line in o:
        user, item, rating =  line.split()
        testArray[int(user), int(item)] = int(rating)

with open('RecSysOutput_userbias.txt', 'w+') as out:
    for user in range(1,944):
        for item in range(1,1683):
            if (user, item) not in trainArray: 
                out.write('%d %d %d\n' %(user, item,  testArray[user,item]))
            else:
                out.write('%d %d %d\n' %(user, item,  trainArray[user,item]))



###############################################################################################
testArray = {}
with open('recSysTestOut_itembias.txt','r') as o:
    for line in o:
        user, item, rating =  line.split()
        testArray[int(user), int(item)] = int(rating)

with open('RecSysOutput_itembias.txt', 'w+') as out:
    for user in range(1,944):
        for item in range(1,1683):
            if (user, item) not in trainArray: 
                out.write('%d %d %d\n' %(user, item,  testArray[user,item]))
            else:
                out.write('%d %d %d\n' %(user, item,  trainArray[user,item]))






###############################################################################################
testArray = {}
with open('recSysTestOut_globalbias.txt','r') as o:
    for line in o:
        user, item, rating =  line.split()
        testArray[int(user), int(item)] = int(rating)

with open('RecSysOutput_globalbias.txt', 'w+') as out:
    for user in range(1,944):
        for item in range(1,1683):
            if (user, item) not in trainArray: 
                out.write('%d %d %d\n' %(user, item,  testArray[user,item]))
            else:
                out.write('%d %d %d\n' %(user, item,  trainArray[user,item]))