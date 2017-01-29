import numpy as np
from numpy.testing import assert_equal
from shutil import rmtree
import os, tempfile

d = {}
count = 0
itemarray = []
userarray=[]
PredictMatrix=[]
rddarray=[]
with open("train_all_txt.txt", 'r') as f:
    for line in f:
        user,item,rating =  line.split()
        d[int(user), int(item)] = int(rating)
   
g = open('MovieLens.test','w+')
for i in range(1,944):
    for j in range(1,1683): 
        if (i, j) not in d:
            g.write("%d %d\n" %(i, j))
            g.flush()
g.close()