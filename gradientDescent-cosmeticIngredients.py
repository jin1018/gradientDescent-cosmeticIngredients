"""
Implementation of Gradient Descent
Multivariate Linear Regression

analyze the ingredients of cosmetic products
relationship between the ingredients & price and the ingredients & rating
sephora_data_foundation.txt: created by a scraper function (sephora_scrape.py)

Results are displayed at the end of this file
"""
from __future__ import division
import copy
import numpy as np
import matplotlib.pyplot as plt

#Build a list of all the ingredients that are observed
with open("sephora_data_foundation") as f:
	lines = f.readlines()
f.close()
#print(lines[0])#['MAKE UP FOR EVER Ultra HD Invisible Cover Foundation', '1.01', '43', '3.5493', '[,]\n']
#print(len(lines))#2240

allProductsInfo=[]
products_ing=[]
for i in lines:
	info_eachProduct = i.split("|")
	allProductsInfo.append(info_eachProduct)
	#print(info_eachProduct)
	products_ing.append(info_eachProduct[4])
	#print(info_eachProduct[4])
#print(products_ing)
#print(len(products_ing))#240
#There are 240 products in the sephora_data_foundation.txt file

for i in range(0,len(products_ing)):
	products_ing[i] = products_ing[i].replace("[","")
	products_ing[i] = products_ing[i].replace("]","")
	#print(products_ing[i])
	temp=products_ing[i].split(",")
	products_ing[i]=temp

allIngredients=[]
for i in products_ing:
	#print(i)
	for j in i:
		if not(j in allIngredients):
			allIngredients.append(j)

#print(len(allIngredients))#There are 1188 different ingredients
#Count frequency of each ingredient an delete from the list if it appears too few times
freq_ing=[]
for i in allIngredients:
	count=0
	#print(i)
	for j in products_ing:
		for k in j:
			#print k
			if i==k:
				count = count+1
	freq_ing.append(count)
#print(len(freq_ing))#1188
#print(freq_ing)

for i in range(0,len(freq_ing)-1):#Need to delete the bigger indices first(from the back of list), otherwise it gets messed up
	#print freq_ing[i]
	if freq_ing[len(freq_ing)-1-i]<2:
		#print freq_ing[i]
		delItem=allIngredients.index(allIngredients[len(freq_ing)-1-i])
		del allIngredients[delItem]
#print(len(allIngredients))#Now, its 408
#print allIngredients


#Create feature vectors
#number of features are the number of types of ingredients
#if a certain ingredient is present, the corresponding index of the vector is 1 (otherwise, 0)
fv=[]#list of all feature vectors
for p in products_ing:
	eachProductFV=[]
	for i in allIngredients:
		if i in p:
			eachProductFV.append(1)#ingredient is present
		else:
			eachProductFV.append(0)#ingredient is not present
	fv.append(eachProductFV)

#print(len(fv))#there are 240 products
#print(fv[0])
#print(fv[1])
#fv is the X matrix (design Matrix)

def isfloat(value):
  try:
    float(value)
    return True
  except:
    return False

def isInt(value):
  try:
    int(value)
    return True
  except:
    return False

#1.
#when Y= price Per size (USD Per OZ)
y_price=[]
indexDel=[]#because size is unavailable
for i in range(0,len(allProductsInfo)):
	p=allProductsInfo[i]
	#print(p[1])
	if isfloat(p[1]):
		p_size=float(p[1])
	elif isInt(p[1]):
		p_size=int(p[1])
	else:
		indexDel.append(i)

	p_price=float(p[2])
	pricePerOunce=p_price/p_size
	y_price.append(pricePerOunce)

#print(y_price)
#print(len(y_price))#240

#delete data where the size of price is unavailable
indexDel.reverse()#Need to delete the bigger indices first(from the back of list)

x_ing_price = copy.deepcopy(fv)
for i in indexDel:
	del y_price[delItem]
	del x_ing_price[delItem]
#print(len(y_price))#Now its 208
#print(len(x_ing_price))#Now its 208
#print(len(fv))#Still 240

#Implement my own Gradient Descent Algorithm
#Plot graph(number of iteration - cost) to see if it converges and whether gradient descent actually works
def gradientDescent_regression(x_data, y_value, learningRate, numberIter):
	"""
	m:number of data
	i:each instance of data
	w:weights[w0,w1,w2,w3 ...]
	Linear Regression Cost Function(Least Squares): J(w) = (1/(2m)) * Sum((w_i*x_i - y_i)^2)

	the objective of gradient descent is to find w that will minimize the cost function(J)

	repeat until converge: w_j = w_j - A*(derivative of J)
	update all w_j SIMULTATNEOUSLY
	Intuition(notes):
	Slope(derivative of J) is 0 for the minimum of J
	Consider the case where there is one parameter for w.(j=0, w =[w_0])
	When slope >0, decrease w_j
	When slope =0, w_j = w_j - 0 (Converges)
	When slope <0, increase w_j	

	A:learing rate
	if A is too small, gradient descent performs too slowly
	is A is too big, may overshoot the minimun

	Linear Regression is ALWAYS a CONVEX function
	(guaranteed that gradient Descent will find the global minimum, not a local minimun)

	-iterative method
	-use the entire batch(all training examples) for each step
	"""

	#w: initialize the weight vector with all 0s(or with random numbers)
	#print len(x_ing_price[0])#408

	w= [0]*(len(x_data[0])+1)#+1 because of the bias term w_0
	for i in range(0,len(x_data)):#add 1 in from of each feature data because of the bias term w_0
		x_data[i].insert(0,1)#inserts infront of the list
	#print len(x_data[0])#409
	#print (x_data[1])

	plotY_Cost=[]
	plotX_iter=[]
	for i in range(1,numberIter+1):
		plotX_iter.append(i)
	for i in range(1,numberIter+1):
		#w_j=w_j - A*(derivative of J)

		#print (w)
		for j in range(0,len(w)):
			dCost=derivativeOfCost(j,w,x_data,y_value)
			w[j]=w[j]-learningRate*dCost#update simultaneously

		cost=costFunctionJ(w,x_data,y_value)
		plotY_Cost.append(cost)
		print("Number of Iteration: "+ str(i)+ ", Cost: " + str(cost))
	#Plot Graph : see how well the gradient descent algorithm works
	plt.plot(plotX_iter, plotY_Cost, 'ro')
	plt.show()

	return w


def costFunctionJ(w,x,y):
	sigma=0
	for i in range(0,len(x)):
		sigma=sigma+(np.dot(w,x[i])-y[i])**2
	return (1/(2*len(x)))*sigma

def derivativeOfCost(j,w,x,y):
	"""
	i: ith vector in x
	j: jth feature in w
	derivative(J)
	=derivative(	(1/(2m)) * Sum( (w * x_i - y_i)^2	)
	= (1/(2m)) * 2 * Sum( (w * x_i - y_i) * (derivative of (w * x_i - y_i)) ) #Chain Rule
	= (1/m) * Sum ( (w * x_i - y_i) * (x_i_j)) )
	"""
	#j: jth feature in w

	sum=0
	#print(len(w))#409
	#print(len(x[1]))#409
	for i in range(0,len(x)):#ith data
		#print(x[i][j])
		sum=sum+(np.dot(w,x[i])-y[i])*x[i][j]

	return (1/(len(w)))*sum


#Run Gradient Descent with X = x_ing_price and Y = y_price
runGDalgo= gradientDescent_regression(x_ing_price,y_price, 2, 500)
#print("weights: ")
print(runGDalgo)

#2.
#when Y= rating

y_rate=[]
indexDel=[]#because rating is unavailable
for i in range(0,len(allProductsInfo)):
	p=allProductsInfo[i]
	#print(p[3])
	p_rate=float(p[3])
	y_rate.append(p_rate)

#print(y_rate)
#print(len(y_rate))#240

#Run Gradient Descent with X = x_ing_price and Y = y_price
runGDalgo_rate= gradientDescent_regression(fv,y_rate, 1.7, 500)
#print("weights: ")
print(runGDalgo_rate)




"""
Results
1. Train data where X represents ingredients and Y represents price Per ounce with learning rate = 2, 500 iterations)
Number of Iteration: 1, Cost: 942.387494555
Number of Iteration: 2, Cost: 891.242380663
Number of Iteration: 3, Cost: 860.321440029
Number of Iteration: 4, Cost: 837.726475101
Number of Iteration: 5, Cost: 819.951994927
Number of Iteration: 6, Cost: 805.458377951
Number of Iteration: 7, Cost: 793.359969089
Number of Iteration: 8, Cost: 783.077546936
.....

Number of Iteration: 494, Cost: 659.178460962
Number of Iteration: 495, Cost: 659.177546048
Number of Iteration: 496, Cost: 659.176639818
Number of Iteration: 497, Cost: 659.175742189
Number of Iteration: 498, Cost: 659.174853075
Number of Iteration: 499, Cost: 659.173972393
Number of Iteration: 500, Cost: 659.173100059
With more iterations, the cost would decrease to a value closer to zero

The ingredients with the greastest weights:
(Products with these ingredients tend to be more expensive)
barium sulfate
iron oxide (ci 77491)
cyclomethicone
ptfe
polysorbate 60
polysilicone2
acetyl hexapeptide8
cyclohexasiloxane
stearalkonium hectorite
hydroxyethylcellulose
coconut alkanes

The ingredients with the smallest weights:
(Products with these ingredients tend to be less expensive)
phenyl trimethicone
aluminum dimyristate
tetrasodium edta
sorbitan sesquiisostearate
hydrogenated lecithin
disteardimonium hectorite
polyglyceryl6 polyricinoleate
sorbitol
propyl gallate
silybum marianum (milk thistle) seed extract
cococaprylate/caprate

2. Train data where X represents ingredients and Y represents rating with learning rate = 1.7, 500 iterations)
Number of Iteration: 1, Cost: 0.167852689217
Number of Iteration: 2, Cost: 0.159959515762
Number of Iteration: 3, Cost: 0.154322937304
Number of Iteration: 4, Cost: 0.150005043669
Number of Iteration: 5, Cost: 0.14653881781
Number of Iteration: 6, Cost: 0.14366584898
Number of Iteration: 7, Cost: 0.141229207628
Number of Iteration: 8, Cost: 0.139126353205
.....
Number of Iteration: 494, Cost: 0.112514712539
Number of Iteration: 495, Cost: 0.112514627269
Number of Iteration: 496, Cost: 0.112514542798
Number of Iteration: 497, Cost: 0.112514459116
Number of Iteration: 498, Cost: 0.112514376215
Number of Iteration: 499, Cost: 0.112514294085
Number of Iteration: 500, Cost: 0.112514212719
With more iterations, the cost would decrease to a value closer to zero

The ingredients with the greastest weights:
(Products with these ingredients tend to be receive higher ratings)
polyglyceryl4 isostearate
cyclohexasiloxane
titanium dioxide
alcohol
magnesium myristate
polyglyceryl2 triisostearate
peg9 polydimethylsiloxyethyl dimethicone
isostearic acid
methicone
sorbitan sesquiisostearate
alphaisomethyl ionone

The ingredients with the smallest weights:
(Products with these ingredients tend to be receive low ratings)
tocopherol
cera microcristallina (microcrystalline wax)
methyl methacrylate crosspolymer
peg/ppg14/7 dimethyl ether
dicalcium phosphate
isohexadecane
stearic acid
ascorbic acid
cyclopentasiloxane
ethoxydiglycol
polyhydroxystearic acid
bismuth

"""
