import sys
import math

if len(sys.argv)!= (1+1):
	print('1: output file')
	exit(-1)
input = 'train_all_txt.txt'
test_file = 'recSysTest.txt'


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
print ('rmse for global_bias.py: %f\n' % math.sqrt(rmse/count))
	

		
