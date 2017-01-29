import sys
import math

if len(sys.argv) != (1+1):
	print('1: prediction')
	exit(-1)
loc_pred = sys.argv[1]

rmse = 0
count = 0
with open('MovieLens.ans','r') as f:
	with open(loc_pred,'r') as g:
		for line in f:
			line2 = g.readline()
			ans = float(line)
			pred = float(line2)
			rmse += pow(ans-pred,2)
			count += 1
print('rmse: %f\n' % math.sqrt(rmse/count))