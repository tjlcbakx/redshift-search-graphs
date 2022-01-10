import numpy as np

def giveMultipleInterpretations(z,J):
	n = 0
	otherZ = 2
	returnArray = []
	while otherZ < 10:
		n += 1
		otherZ = z + (n-J)*(1+z)/J
		if otherZ > 0:
			returnArray.append([n,otherZ])
			# print(str(n) + ' - ' + str(np.round(otherZ,2)))

def giveMultiFactors(a,b):
	multiFac = 1
	for i in range(2,max(a,b)):
		if (a%i == 0) and (b%i == 0):
			multiFac = i
	# print(multiFac)
	if multiFac == 1:
		return min(a,b)
	else:
		return min(a,b)*(multiFac-1)/multiFac- min(a,b)