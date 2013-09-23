import sys
import csv

import numpy as np



if __name__ == '__main__':

	ground_truth = sys.argv[1]
	candidate = sys.argv[2]

	#: loading data also: genfromtxt
	g_frame, g_x1, g_y1, g_x2, g_y2 = np.loadtxt(	ground_truth,
													dtype='i8',
					        						delimiter=',',
										     		unpack=True,
										     		usecols=(0,1,2,3,4),
										     		)
	# print g_x1

	c_frame, c_x1, c_y1, c_x2, c_y2 = np.loadtxt( 	candidate,
					        						delimiter=',',
										     		unpack=True,
										     		usecols=(0,1,2,3,4),
										     		)

	ovMax = np.arange(0.3, 1.05, 0.05)
	

