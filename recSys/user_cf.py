import sys
import math

def gen_bias_usercf(bias,user):
	return float(bias[user][0])/bias[user][1]
def cosine_sim_usercf(user,item,user_map,item_map,bias):
	total = 0 
	score = 0
	for u in item_map[item]:
		compare = set(user_map[user].keys()).intersection(user_map[u].keys())
		if len(compare) == 0:
			continue
		'''
		calculate the similarity score
		and then calculate the rating
		Save the rating into final 
		'''
	final = float(score)/total
	try:
		final = float(score)/total + gen_bias_usercf(bias,user)
	except ZeroDivisionError:
		final = 1
	### scaling
	if final > 5:
		final = 5
	if final < 0:
		final = 0
	return final
	
	
def pearson_sim_usercf(user,item,user_map,item_map,bias):
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
		score += sim * (user_map[u][item]) - gen_bias_usercf(bias,u)
		total = total + sim
	final = float(score)/total+ gen_bias_usercf(bias,user)

	if final > 5:
		final = 5
	if final < 0:
		final = 0
	return final	


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
		if item not in item_map.keys():
			item_map[item] = set([user])
		else:
			item_map[item].add(user)
		if user not in user_map.keys():
			user_map[user] = {}
			user_map[user][item] = rating
		else:
			user_map[user][item] = rating
		### construct user bias
		if user not in bias.keys():
			bias[user] = [rating,1]
		else:
			bias[user][0] += rating
			bias[user][1] += 1
		### global bias
		global_bias += rating
		global_count += 1
global_bias = float(global_bias)/global_count

	
# cosine similarity	
with open('recSysTestOut_usercf.txt','r') as f:
	with open('recrSysTestOut_usercf.txt','w+') as g:
		count = 0
		for line in f:
			words = line.split()
			user = int(words[0])
			item = int(words[1])
			
			### cold start item
			if item not in item_map.keys():
				g.write('%d %d %d\n' %(user, item,  int(round(global_bias))))
				continue
			pred = cosine_sim_usercf(user,item,user_map,item_map,bias)
			#pred = pearson_sim_usercf(user,item,user_map,item_map,bias)
			g.write('%d %d %d\n' %(user, item,  int(round(pred))))
			count += 1
			if (count % 1000) == 0:
				print(count)

### Calculate training RMSE				
with open('train_all_txt.txt','r') as f:
	count = 0
	rmse = 0 
	for line in f:
		words = line.split()
		user = int(words[0])
		item = int(words[1])
		rating = int(words[2])
		pred = cosine_sim_usercf(user,item,user_map,item_map,bias)
		rmse += pow(rating-pred,2)
		count += 1
print ('rmse: %f\n' % math.sqrt(rmse/count))
		
			
			
				