
##################################################user-based cosine similarity and pearson similarity#####################################
#bias for user based collaborative filtering
def gen_bias_usercf(bias,user):
	return float(bias[user][0])/bias[user][1]
#cosine similarity for user based collaborative filtering
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
	
	try:
		final = float(score)/total
	except ZeroDivisionError:
		final = 1
	### scaling
	if final > 5:
		final = 5
	if final < 0:
		final = 0
	return final
	

#pearson similarity for user basd collaborative filtering
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

################################################item-based collaborative filtering####################################################
#item based collaborative filtering for predicting values
		################################################user-based collaborative filtering####################################################
#user based collaborative filtering to predict the values
def user_cf():
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
	with open('recSysTest.txt','r') as f:
		with open('recSysTestOut_usercf.txt','w+') as g:
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
				# count += 1
				# if (count % 1000) == 0:
				# 	print(count)

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
	print ('RMSE for user based collaborative filtering: %f\n' % math.sqrt(rmse/count))
			
				
				
				
	################################################user-based bias prediction####################################################
def user_bias():
		### calculate user bias
	bias = {}
	with open('train_all_txt.txt','r') as f:
		for line in f:
			words = line.split()
			user = int(words[0])

			rating = int(words[2])
			if user not in bias.keys():
				bias[user] = [rating,1]
			else:
				bias[user][0] += rating
				bias[user][1] += 1
			'''
			calculate the bias while reading the file one by one!
			You should let the bias be the dictionary mapping user into 
			a list structure that the first element is the total rating
			and the second element is the number of ratings of the user
			
			Guide:
			If the user is not in the key of the bias
			(can be determined by [if user not in bias.keys()] clause)
			You should initialize a list corresponding the user.
			ex: bias[user] = [rating,1]
			If the user is already in the key
			You can just add the value of the total ratings and total number of ratings
			'''
	### predicting
	count = 0
	rmse = 0
	g = open('recSysTestOut_userbias.txt','w+')
	with open('recSysTest.txt','r') as f:
		for line in f:
			words = line.split()
			user = int(words[0])
			item = int(words[1])
			pred = float(bias[user][0])/bias[user][1]
			g.write('%d %d %d\n' %(user, item,  int(round(pred))))
	g.close()		

	### calculate training RMSE
	rmse = 0
	count = 0
	with open('train_all_txt.txt','r') as f:
		for line in f:
			words = line.split()
			user = int(words[0])
			rating = int(words[2])
			pred = float(bias[user][0])/bias[user][1]
			rmse += pow(rating-pred,2)
			count += 1
	print ('RMSE for user_bias: %f\n' % math.sqrt(rmse/count))


		################################################item-based bias prediction####################################################
def item_bias():

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

	g = open('recSysTestOut_itembias.txt','w+')
	with open('recSysTest.txt','r') as f:
		for line in f:
			words = line.split()
			
			user = int(words[0])
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
	print ('RMSE for item_bias: %f\n' % math.sqrt(rmse/count))
			

		################################################global bias prediction####################################################
def global_bias():
	### calculate global bias
	### first element for total score, second element for the amount of ratings
	bias = [0,0]   
	with open('train_all_txt.txt','r') as f:
		for line in f:
			words = line.split()
			rating = int(words[2])
			bias[0] += rating
			bias[1] += 1

	### predicting
	rmse = 0
	g = open('recSysTestOut_globalbias.txt','w+')
	with open('recSysTest.txt','r') as f:
		for line in f:
			words = line.split()
			user = int(words[0])
			item = int(words[1])
			pred = float(bias[0])/bias[1]
			g.write('%d %d %d\n' %(user, item,  int(round(pred))))
	g.close()	

	### calculate training RMSE
	ans = float(bias[0])/bias[1]
	rmse = 0 
	count = 0 
	with open('train_all_txt.txt','r') as f:
		for line in f:
			words = line.split()
			rating = int(words[2])
			rmse += pow(ans-rating,2)
			count += 1
	### need to be modified in python3
	print ('RMSE for global_bias.py: %f\n' % math.sqrt(rmse/count))
		
#prediction output generation based on the specified format
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