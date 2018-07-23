'''
==============
3D scatterplot
==============

Demonstration of a basic scatterplot in 3D.
'''
import matplotlib
matplotlib.use('Agg')
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import random
import joblib
import random
import pickle

fig = plt.figure(figsize=(12,11))
ax = fig.add_subplot(111,projection='3d')

"""
scrs = []
for c1 in [0.5,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95]:
	for c2 in [0.5,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95]:
		for MAX_ITER in range(100,1000):
			print("New ptn : ("+str(c1)+","+str(c2)+","+str(MAX_ITER)+")")
			scrs.append([c1,c2,MAX_ITER,random.random()])
joblib.dump(scrs, "./scrs", pickle.HIGHEST_PROTOCOL)
"""
scrs = joblib.load("/home/lsablayr/stageM1/debates/step2_M1/learning/scrs")
# scrs = joblib.load("./scrs")

firebrick = mpatches.Patch(color='firebrick', label='acc < 0.05')
red = mpatches.Patch(color='red', label='0.05 <= acc < 0.1')
orangered = mpatches.Patch(color='orangered', label='0.1 <= acc < 0.15')
darkorange = mpatches.Patch(color='darkorange', label='0.15 <= acc < 0.2')
orange = mpatches.Patch(color='orange', label='0.2 <= acc < 0.25')
gold = mpatches.Patch(color='gold', label='0.25 <= acc < 0.3')
yellow = mpatches.Patch(color='yellow', label='0.3 <= acc < 0.35')
yellowgreen = mpatches.Patch(color='yellowgreen', label='0.35 <= acc < 0.4')
lawngreen = mpatches.Patch(color='lawngreen', label='0.4 <= acc < 0.45')
limegreen = mpatches.Patch(color='limegreen', label='0.45 <= acc < 0.5')
green = mpatches.Patch(color='green', label='0.5 <= acc < 0.55')
cyan = mpatches.Patch(color='cyan', label='0.55 <= acc < 0.6')
turquoise = mpatches.Patch(color='turquoise', label='0.6 <= acc < 0.65')
lightseagreen = mpatches.Patch(color='lightseagreen', label='0.65 <= acc < 0.7')
teal = mpatches.Patch(color='teal', label='0.75 <= acc < 0.8')
steelblue = mpatches.Patch(color='steelblue', label='0.8 <= acc < 0.85')
mediumblue = mpatches.Patch(color='mediumblue', label='0.85 <= acc < 0.9')
blueviolet = mpatches.Patch(color='blueviolet', label='0.9 <= acc < 0.95')
purple = mpatches.Patch(color='purple', label='0.95 <= acc')

last = ""
max_s = 0
best = ""
x = [0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95]
c1Graph =  {'x': x, 'y': [0 for i in range(len(x))], 'nb': [1 for i in range(len(x))]}
c1Min = {'x': x, 'y': [1.2 for i in range(len(x))]};
c1Max = {'x': x, 'y': [-1 for i in range(len(x))]};

c2Graph =  {'x': x, 'y': [0 for i in range(len(x))], 'nb': [1 for i in range(len(x))]}
c2Min = {'x': x, 'y': [1.2 for i in range(len(x))]};
c2Max = {'x': x, 'y': [-1 for i in range(len(x))]};

maxIterGraph = {'x': range(100,1000), 'y': [0 for i in range(100,1000)], 'nb': [1 for i in range(100,1000)]}
maxIterMin = {'x': x, 'y': [1.2 for i in range(100,1000)]};
maxIterMax = {'x': x, 'y': [-1 for i in range(100,1000)]};

for c1,c2,MAX_ITER,s in scrs:
	last = " ("+str(c1)+","+str(c2)+","+str(MAX_ITER)+")"
	
	c1Graph['y'][c1Graph['x'].index(c1)] += s
	c1Graph['nb'][c1Graph['x'].index(c1)] += 1
	c1Min[c1Min['x'].index(c1)] = min(c1Min[c1Min['x'].index(c1)], s)
	c1Max[c1Max['x'].index(c1)] = max(c1Max[c1Max['x'].index(c1)], s)
	
	c2Graph['y'][c2Graph['x'].index(c2)] += s
	c2Graph['nb'][c2Graph['x'].index(c2)] += 1
	c2Min[c2Min['x'].index(c2)] = min(c2Min[c2Min['x'].index(c2)], s)
	c2Max[c2Max['x'].index(c2)] = max(c2Max[c2Max['x'].index(c2)], s)
	
	maxIterGraph['y'][maxIterGraph['x'].index(MAX_ITER)] += s
	maxIterGraph['nb'][maxIterGraph['x'].index(MAX_ITER)] += 1
	maxIterMin[maxIterMin['x'].index(MAX_ITER)] = min(maxIterMin[maxIterMin['x'].index(MAX_ITER)], s)
	maxIterMax[maxIterMax['x'].index(MAX_ITER)] = max(maxIterMax[maxIterMax['x'].index(MAX_ITER)], s)
	
	if s > max_s:
		best = "Max("+str(c1)+","+str(c2)+","+str(MAX_ITER)+" : "+str(s)+")"
		max_s = s
	if MAX_ITER in [100, 250, 500, 750, 999]:
		print("Adding point :",c1,c2,MAX_ITER,"value", s)
		if s < 0.05:
			c = 'firebrick'
		else:
			if s < 0.1:
				c = 'red'
			else:
				if s < 0.15:
					c = 'orangered'
				else:
					if s < 0.2:
						c = 'darkorange'
					else:
						if s < 0.25:
							c = 'orange'
						else:
							if s < 0.3:
								c = 'gold'
							else:
								if s < 0.35:
									c = 'yellow'
								else:
									if s < 0.4:
										c = 'yellowgreen'
									else:
										if s < 0.45:
											c = 'lawngreen'
										else:
											if s < 0.5:
												c = 'limegreen'
											else:
												if s < 0.55:
													c = 'green'
												else:
													if s < 0.6:
														c = 'cyan'
													else:
														if s < 0.65:
															c = 'turquoise'
														else:
															if s < 0.7:
																c = 'lightseagreen'
															else:
																if s < 0.75:
																	c = 'teal'
																else:
																	if s < 0.8:
																		c = 'steelblue'
																	else:
																		if s < 0.85:
																			c = 'mediumblue'
																		else:
																			if s < 0.9:
																				c = 'blue'
																			else:
																				if s < 0.95:
																					c = 'blueviolet'
																				else:
																					c = 'purple'
				ax.scatter(MAX_ITER, c2, c1, c=c, marker='o', s=125)
				if c in ['mediumblue', 'blue', 'blueviolet', 'purple']:
					ax.text(MAX_ITER, c2, c1, '%s' % (str(round(s,2))), size=10, zorder=5, color='k')

plt.title("Accuracy for CRF"+last+best)
ax.set_xlabel('MAX_ITER')
ax.set_ylabel('c2')
ax.set_zlabel('c1')
ax.legend(handles=[firebrick, red, orangered, darkorange, orange, gold, yellow, yellowgreen, lawngreen, limegreen, green, cyan, turquoise, lightseagreen, teal, steelblue, mediumblue, blueviolet, purple],loc='upper center', bbox_to_anchor=(0.5, -0.01), fancybox=True, shadow=True, ncol=5, title="Accuracy Colors")
fig.savefig("graph.png")

for i in range(len(c1Graph['x'])):
	c1Graph['y'][i] /= c1Graph['nb'][i]

for i in range(len(c2Graph['x'])):
	c2Graph['y'][i] /= c2Graph['nb'][i]

for i in range(len(maxIterGraph['x'])):
	maxIterGraph['y'][i] /= maxIterGraph['nb'][i]

fig = plt.figure(figsize=(12,11))
ax = fig.add_subplot(311)
ax.plot(c1Graph['x'], c1Graph['y'])
ax.plot(c1Min['x'], c1Min['y'])
ax.plot(c1Max['x'], c1Max['y'])
ax.set_xlabel("c1")
ax.set_ylabel("Mean accuracy")
ax.legend(["Moy", "Min", "Max"])

ax2 = fig.add_subplot(312)
ax2.plot(c2Graph['x'], c2Graph['y'])
ax.plot(c2Min['x'], c2Min['y'])
ax.plot(c2Max['x'], c2Max['y'])
ax2.set_xlabel("c2")
ax2.set_ylabel("Mean accuracy")
ax2.legend(["Moy", "Min", "Max"])

ax3 = fig.add_subplot(313)
ax3.plot(maxIterGraph['x'], maxIterGraph['y'])
ax.plot(maxIterMin['x'], maxIterMin['y'])
ax.plot(maxIterMax['x'], maxIterMax['y'])
ax3.set_xlabel("maxIter")
ax3.set_ylabel("Mean accuracy")
ax3.legend(["Moy", "Min", "Max"])

fig.savefig("accuracies.png")

