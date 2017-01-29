import sys
import math



### calculate user bias
bias = {}
with open('train_all_txt.txt','r') as f:
	for line in f:
		words = line.split()
		item = int(words[1])
		rating = int(words[2])
		if item not in bias.keys():
			bias[item] = [rating,1]
		else:
			bias[item][0] += rating
			bias[item][1] += 1

### just for testing

g = open('ecSysTestOut_itembias.txt','w+')
with open('recSysTest.txt','r') as f:
	for line in f:
		words = line.split()
		item = int(words[1])
		if item in bias.keys():
			pred = float(bias[item][0])/bias[item][1]
		else: ### for cold start items
			pred = 2.5
		g.write('%d %d %d\n' %(user, item,  int(round(pred))))
g.close()

### calculate training RMSE
rmse = 0
count = 0
with open('train_all_txt.txt','r') as f:
	for line in f:
		words = line.split()
		item = int(words[1])
		rating = int(words[2])
		pred = float(bias[item][0])/bias[item][1]
		rmse += pow(rating-pred,2)
		count += 1
print ('rmse for item_bias: %f\n' % math.sqrt(rmse/count))
		


		

		
