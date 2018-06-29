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

fig = plt.figure(figsize=(12,11))
ax = fig.add_subplot(111,projection='3d')
plt.title("Accuracy for CRF")

scrs = joblib.load("/home/lsablayr/stageM1/debates/step2_M1/learning/scrs")

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

for c1,c2,MAX_ITER,s in scrs:
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
ax.set_xlabel('MAX_ITER')
ax.set_ylabel('c2')
ax.set_zlabel('c1')
ax.legend(handles=[firebrick, red, orangered, darkorange, orange, gold, yellow, yellowgreen, lawngreen, limegreen, green, cyan, turquoise, lightseagreen, teal, steelblue, mediumblue, blueviolet, purple],loc='upper center', bbox_to_anchor=(0.5, -0.01), fancybox=True, shadow=True, ncol=5, title="Accuracy Colors")
fig.savefig("graph.png")
