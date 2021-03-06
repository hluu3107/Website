import numpy as np
from collections import defaultdict

def process_input(inputFile):
	#process input file and return adjacency matrix	
	f = ''
	adj_matrix = {}
	count = 0
	order = []
	for line in inputFile:
		f = f + line.decode()
	f = f.splitlines()
	nr = int(f[0])
	nc = int(f[1])
	for i in range(-1,-nc-1,-1):
		order.append(i)
	for i in range(nc,0,-1):
		order.append(i)
	for i in range(2,len(f)):
		line = f[i]
		st = line.split(":")
		node1 = int(st[0])		
		st2 = st[1].strip().split(",")
		adj_matrix[node1] = []
		if st2!=['']:
			neighbors =list(map(int,st2))
			neighbors.sort(key=lambda x:order.index(x-node1))						
			adj_matrix[node1] = neighbors
		count += len(adj_matrix[node1])
	return int(count/2),adj_matrix,nr,nc

def list_diff(list1,list2):
	return [item for item in list1 if item not in list2]

def getSlope(p1,p2):
	#vertical line
	if np.all(abs(p1.x-p2.x)<1e-9):
		return None
	else:
		return (p2.y-p1.y)/(p2.x-p1.x)

#calculate area from list of points
def calculateAreaPoints(allPoints,w):
	area = 0
	for i in range(0,len(allPoints)-1):
		p1 = allPoints[i]
		p2 = allPoints[i+1]
		w = p2.x-p1.x
		if abs(allPoints[i+1].y-allPoints[i].y) < 1e-9:
			#rectangle
			area = area + w*p1.y
		else:
			#trapezoid
			area = (p1.y+p2.y)*w/2	
	return are

def calculateTime(s,v):
	if abs(v)<1e-9:
		return 0
	else:
		return abs(s/v)

def getResult(grid):
	sumout = 0
	string = ""
	concentration_list = []
	velocity_list = []
	for i in range(grid.nNode-grid.nCol+1,grid.nNode+1):
		if not grid.adjMatrix[i]:
			concentration_list.append(0)
			velocity_list.append(0)
			continue
		(u,v) = (i,grid.adjMatrix[i][0])
		c = grid.concentration[i].calculateConcentration()
		vel = grid.velocity[(v,u)]
		sumout = sumout + c*vel
		#print(f'C{i}= {c:.4f}, V{u}-{v}= {vel:.4f}')
		concentration_list.append(c)
		velocity_list.append(vel)
	# cString = ",".join(map(lambda x: "%.4f" % x,concentration_list))
	# vString = ",".join(map(lambda x: "%.4f" % x,velocity_list))
	return concentration_list,velocity_list




