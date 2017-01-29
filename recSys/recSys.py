from __future__ import division
from numpy.testing import assert_equal
from shutil import rmtree
import sys
import math
import numpy as np
import os, tempfile

#Generating test set for matrix completion problem to predict the rating
def recSysTestgen():
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
	   
	g = open('recSysTest.txt','w+')
	for i in range(1,944):
	    for j in range(1,1683): 
	        if (i, j) not in d:
	            g.write("%d %d\n" %(i, j))
	            g.flush()
	g.close()

#bias for the item based collaborative filtering. 
def gen_bias_itemcf(bias,item):
	return float(bias[item][0])/bias[item][1]

#cosine similarity for item based collaborative filtering
def cosine_sim_itemcf(user,item,user_map,item_map,bias):
	total = 0 
	score = 0
	for u in user_map[user]:
		compare = set(item_map[item].keys()).intersection(item_map[u].keys())
		if len(compare) == 0:
			continue
		up = 0 
		down1 = 0
		down2 = 0
		for i in compare:
			r1 = item_map[u][i]
			r2 = item_map[item][i]
			up += r1*r2
			down1 += pow(r1,2)
			down2 += pow(r2,2)
		down1 = math.sqrt(down1)
		down2 = math.sqrt(down2)
		sim = float(up) / (down1*down2) 
		score += sim * (item_map[u][user]- gen_bias_itemcf(bias,u))
		total = total + sim
	try:
		final = float(score)/total + gen_bias_itemcf(bias,user)
	except ZeroDivisionError:
		final = 1
	### scaling
	if final > 5:
		final = 5
	if final < 0:
		final = 0
	return final
	
#pearson similarity for item based collaborative filtering	
def pearson_sim_itemcf(user,item,user_map,item_map,bias):
	total = 0 
	score = 0
	for u in item_map[item]:
		compare = set(user_map[user].keys()).intersection(user_map[u].keys())
		if len(compare) == 0:
			continue
		up = 0 
		down1 = 0
		down2 = 0
		for i in compare:
			r1 = user_map[u][i] - float(bias[u][0])/bias[u][1]
			r2 = user_map[user][i] - float(bias[user][0])/bias[user][1]
			up += r1*r2
			down1 += pow(r1,2)
			down2 += pow(r2,2)
		if (down1==0) or (down2==0):
			continue
		down1 = math.sqrt(down1)
		down2 = math.sqrt(down2)
		sim = float(up) / (down1*down2)
		score += sim * (user_map[u][item]- gen_bias_itemcf(bias,u)) 
		total = total + sim
	final = float(score)/total+ gen_bias_itemcf(bias,user)

	if final > 5:
		final = 5
	if final < 0:
		final = 0
	return final	

def item_cf():
		### construct the item_map and user_map
	item_map = {}
	user_map = {}
	bias = {}
	global_bias = 0
	global_count = 0
	with open('train_all_txt.txt','r') as f:
		for line in f:
			words = line.split()
			user = int(words[0])
			item = int(words[1])
			rating = int(words[2])
			if user not in user_map.keys():
				user_map[user] = set([item])
			else:
				user_map[user].add(item)
			if item not in item_map.keys():
				item_map[item] = {}
				item_map[item][user] = rating
			else:
				item_map[item][user] = rating
			### construct user bias
			if item not in bias.keys():
				bias[item] = [rating,1]
			else:
				bias[item][0] += rating
				bias[item][1] += 1
			### global bias
			global_bias += rating
			global_count += 1
	global_bias = float(global_bias)/global_count

		
	# cosine similarity	for item based collaborative filtering
	with open('recSysTest.txt','r') as f:
		with open('recSysTestOut_itemcf.txt','w+') as g:
			count = 0
			for line in f:
				words = line.split()
				user = int(words[0])
				item = int(words[1])
				
				### for representing the cold start problem, based on the item bias
				if item not in item_map.keys():
					g.write('%d %d %d\n' %(user, item,  int(round(global_bias))))
					continue
				pred = cosine_sim_itemcf(user,item,user_map,item_map,bias)
				#pred = pearson_sim_itemcf(user,item,user_map,item_map,bias)
				g.write('%d %d %d\n' %(user, item,  int(round(pred))))
				

	### Calculate training RMSE	for item based collaborative filtering			
	with open('train_all_txt.txt','r') as f:
		count = 0
		rmse = 0 
		for line in f:
			words = line.split()
			user = int(words[0])
			item = int(words[1])
			rating = int(words[2])
			pred = cosine_sim_itemcf(user,item,user_map,item_map,bias)
			rmse += pow(rating-pred,2)
			count += 1
	print ('RMSE for item based collaborative filtering: %f\n' % math.sqrt(rmse/count))
			

#Output file generation for combining the predicted file as well as the training set
def recSysOutputgen():

	trainArray = {}

	#resultArray = np.zeros((944,1683))
	with open('train_all_txt.txt','r') as t:
	    for line in t:
	        user, item, rating =  line.split()
	        trainArray[int(user), int(item)] = int(rating)
	
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




#main function for item based collaborative filtering
def main():
	recSysTestgen()
	item_cf()
	recSysOutputgen()

if __name__ == "__main__":
    main()
		

	#####################################################		
				
					