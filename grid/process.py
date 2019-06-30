from .grid import *
import json
import queue
import math
def createGrid(data):
	nEdge,adjMatrix = getMatrixJson(data)
	w = float(data.get('w'))
	l = float(data.get('l'))
	diffCoeff = float(data.get('diffCoeff'))
	nr = int(data.get('nr'))
	nc = int(data.get('nc'))
	#nNode = int(size * size + nIn + nOut)
	#nEdge = reduceGrid(adjMatrix,nIn,nOut,nNode)
	cstring = data.get('initC').split(",")
	vstring = data.get('initV').split(",")
	initC = {}
	initV = {}
	count = 1
	for c in cstring:
		if c=='x':
			initC[count] = 0
			initV[count] = 0
		else:
			initC[count] = float(c)
			initV[count] = float(vstring[count-1])
		count+=1
	print(f'c: {initC}')
	print(f'v: {initV}')	
	grid = Grid(nr,nc,nEdge,w,l,diffCoeff,adjMatrix,initV,initC)
	return grid

def solveGrid(grid):
	grid.solveFlow()
	grid.solveConcentration()

def getMatrixJson(data):
	matrix = json.loads(data.get('adjMatrix'))
	order = []
	nr = int(data.get('nr'))
	nc = int(data.get('nc'))
	for i in range(-1,-nc-1,-1):
		order.append(i)
	for i in range(nc,0,-1):
		order.append(i)
	adjMatrix = {}
	count = 0
	for node,neighbors in matrix.items():
		neighbors.sort(key=lambda x:order.index(x-int(node)))
		adjMatrix[int(node)] = neighbors
		count += len(neighbors)
	return int(count/2),adjMatrix

def getMatrixInput(data):
	graph = json.loads(data)
	nodes = graph.get('nodes')
	edges = graph.get('edges')
	adjMatrix = {}
	for node in nodes:
		adjMatrix[int(node['id'])] = []
	for edge in edges:
		if(edge['selected']==True):
			name = edge['id'].split('-')
			snode = int(name[0])
			enode = int(name[1])
			adjMatrix[snode].append(enode)
			adjMatrix[enode].append(snode)
	#print(adjMatrix)
	return adjMatrix, len(edges)

def getJsonGraph(grid):
	nodes = []
	edges = []
	nodenumber = 1
	nsize = 2
	nColor = "#6ed3cf"
	esize = 0.5
	nr = grid.nRow
	nc = grid.nCol
	nNode = grid.nNode
	# create nodes
	for i in range(1,grid.nNode+1):
		node = {"id": str(i), "x": (i-1)%nc, "y":int((i-1)/nc), "size": nsize, "color":nColor}
		nodes.append(node)
		#print(f'id: {i}, x: {(i-1)%nc}, y: {int((i-1)/nc)}')
	#create edges
	edgen = 1
	for snode,neighbors in grid.adjMatrix.items():
		for enode in neighbors:
			if snode < enode:
				edge = {"id": str(snode)+"-"+str(enode), "source": str(snode), "target": str(enode), "size": esize, "selected": False}
				edgen = edgen+1
				edges.append(edge)
	graph = {"nodes": nodes, "edges": edges}
	jsong = json.dumps(graph)
	#print(jsong)
	return jsong

def getJsonGraph2(grid):
	nodes = []
	edges = []
	nodenumber = 1
	nsize = 2
	nColor = "#e1e8f0"	
	eclickcolor = "#e62739"
	esize = 0.5
	size = grid.size
	nIn = 2
	nOut = 3
	nNode = grid.nNode
	# create input nodes
	if(size>=7):
		node1 = {"id": str(nIn-1), "x": 2, "y": 0, "size": nsize, "color":nColor}
		node2 = {"id": str(nIn), "x": size-3, "y": 0, "size": nsize, "color":nColor}
	else:
		node1 = {"id": str(nIn-1), "x": 1, "y": 0, "size": nsize, "color":nColor}
		node2 = {"id": str(nIn), "x": size-2, "y": 0, "size": nsize, "color":nColor}

	# node1 = {"id": "1", "x": 2, "y": 0, "size": nsize, "color":nColor}
	# node2 = {"id": "2", "x": grid.size-3, "y": 0, "size": nsize, "color":nColor}
	nodes.extend([node1,node2])
	# create normal nodes
	for i in range(grid.nIn+1,grid.nNode-grid.nOut+1):
		node = {"id": str(i), "x": (i-3)%grid.size, "y":int((i-3)/grid.size+1), "size": nsize, "color":nColor}
		nodes.append(node)
	#create output nodes
	nodeo1 = {"id": str(grid.nNode-2), "x": 0, "y": grid.size+1, "size": nsize, "color":nColor}
	nodeo2 = {"id": str(nNode-1), "x": int(size/2), "y": size+1, "size": nsize, "color":nColor}
	#nodeo2 = {"id": str(grid.nNode-1), "x": int((grid.size+1)/2), "y": grid.size+1, "size": nsize, "color":nColor}
	nodeo3 = {"id": str(grid.nNode), "x": grid.size-1, "y": grid.size+1, "size": nsize, "color":nColor}
	nodes.extend([nodeo1,nodeo2,nodeo3])
	
	#create edges
	for snode,neighbors in grid.adjMatrix.items():
		for enode in neighbors:
			if snode < enode:
				edge = {"id": str(snode)+"-"+str(enode), "source": str(snode), "target": str(enode), "size": esize, "selected": True \
						,"color": eclickcolor,"mutable": False}				
				edges.append(edge)
	graph = {"nodes": nodes, "edges": edges}
	jsong = json.dumps(graph)
	#print(jsong)
	return jsong

def createEmptyGrid(data):
	size = int(data.get('size'))
	nIn = 2
	nOut = 3
	nodes = []
	edges = []
	nsize = 2
	nColor = "#e1e8f0"	
	eclickcolor = "#e62739"
	esize = 0.5
	nNode = int(size * size + nIn + nOut)
	# create input nodes
	if(size>=7):
		node1 = {"id": str(nIn-1), "x": 2, "y": 0, "size": nsize, "color":nColor}
		node2 = {"id": str(nIn), "x": size-3, "y": 0, "size": nsize, "color":nColor}
	else:
		node1 = {"id": str(nIn-1), "x": 1, "y": 0, "size": nsize, "color":nColor}
		node2 = {"id": str(nIn), "x": size-2, "y": 0, "size": nsize, "color":nColor}

	nodes.extend([node1,node2])

	# create normal nodes
	for i in range(nIn+1,nNode-nOut+1):
		node = {"id": str(i), "x": (i-3)%size, "y":int((i-3)/size+1), "size": nsize, "color":nColor}
		nodes.append(node)
	#create output nodes
	nodeo1 = {"id": str(nNode-2), "x": 0, "y": size+1, "size": nsize, "color":nColor}
	nodeo2 = {"id": str(nNode-1), "x": int(size/2), "y": size+1, "size": nsize, "color":nColor}
	nodeo3 = {"id": str(nNode), "x": size-1, "y": size+1, "size": nsize, "color":nColor}
	nodes.extend([nodeo1,nodeo2,nodeo3])
	
	#create input edges
	if(size>=7):
		ine1 = {"id": str(nIn-1)+"-"+str(nIn+3), "source":str(nIn-1), "target":str(nIn+3), "size": esize, \
			"selected": True, "color": eclickcolor, "mutable": False}
		ine2 = {"id": str(nIn)+"-"+str(size), "source":str(nIn), "target":str(size), "size": esize, \
			"selected": True, "color": eclickcolor, "mutable": False}
	else:
		ine1 = {"id": str(nIn-1)+"-"+str(nIn+2), "source":str(nIn-1), "target":str(nIn+2), "size": esize, \
			"selected": True, "color": eclickcolor, "mutable": False}
		ine2 = {"id": str(nIn)+"-"+str(size+1), "source":str(nIn), "target":str(size+1), "size": esize, \
			"selected": True, "color": eclickcolor, "mutable": False}
	edges.extend([ine1,ine2])

	#create normal edge
	for snode in range(nIn+1,nNode-nOut+1):
		#create horizontal edges
		if (snode-nIn)%size!=0:
			edge = {"id": str(snode)+"-"+str(snode+1), "source": str(snode), "target": str(snode+1), \
			"size": esize, "selected": False, "mutable": True}
			edges.append(edge)
		#create vertical edges
		if int((snode-nIn-1)/size+1) <= (size-1):
			edge = {"id": str(snode)+"-"+str(snode+size), "source": str(snode), "target": str(snode+size), "size": esize, \
			"mutable": True, "selected": False}
			edges.append(edge)
	#create output edges
	oute1 = {"id": str(nNode-2)+"-"+str(nNode-2-size), "source":str(nNode-2), "target":str(nNode-2-size), "size": esize, \
			"selected": True, "color": eclickcolor, "mutable": False}
	oute2 = {"id": str(nNode-1)+"-"+str(nNode-2-int((size+1)/2)), "source":str(nNode-1), "target":str(nNode-2-int((size+1)/2)), "size": esize, \
			"selected": True, "color": eclickcolor, "mutable": False}
	oute3 = {"id": str(nNode)+"-"+str(nNode-nIn-1), "source":str(nNode), "target":str(nNode-nIn-1), "size": esize, \
			"selected": True, "color": eclickcolor, "mutable": False}
	edges.extend([oute1,oute2,oute3])

	# for node in nodes:
	# 	node["x"] = node["x"]+1
	# 	node["y"] = node["y"]+1
	
	graph = {"nodes": nodes, "edges": edges}
	return json.dumps(graph)

def verifyInputGraph(data):
	adjMatrix, nEdge = getMatrixInput(data.get('graph'))
	size = int(data.get('size'))
	# nIn = int(data.get('nIn'))
	# nOut = int(data.get('nOut'))
	nIn = 2
	nOut = 3
	nNode = int(size * size + nIn + nOut)
	inNodes = []
	outNodes = []
	for i in range(1,nIn+1):
		inNodes.append(i)
	for i in range(nNode-nOut+1,nNode+1):
		outNodes.append(i)
	#get graph cc
	cc = getConnectedComponent(adjMatrix)
	inout = inNodes + outNodes	
	#check if inout is sublist of each connected comp
	for comp in cc:
		if all(node in comp for node in inout):			
			#connected
			return True, adjMatrix, nEdge
		if any(node in comp for node in inout):
			break
	#not connected
	print(inout)
	print(cc)
	return False, adjMatrix, nEdge

def reduceGrid2(adjMatrix,nIn,nOut,nNode):
	time = [0]
	#connect inputs
	for i in range(1,nIn):
		adjMatrix[i].append(i+1)
		adjMatrix[i+1].append(i)
	#connect outputs
	for i in range(nNode-nOut+1,nNode):
		adjMatrix[i].append(i+1)
		adjMatrix[i+1].append(i)
	#TODO: check if connect input with output is nescessary?
	#connect input and output
	adjMatrix[1].append(nNode-nOut+1)
	adjMatrix[nNode-nOut+1].append(i)
	adjMatrix[2].append(nNode)
	adjMatrix[nNode].append(2)
	bc = findBiconnected(adjMatrix,time)
	print(bc)

def reduceGrid(adjMatrix,nIn,nOut,nNode):
	time = [0]
	# for node,neighbors in adjMatrix.items():
	# 	print(f'node {node}: {neighbors}')
	#connect inputs
	for i in range(1,nIn):
		adjMatrix[i].append(i+1)
		adjMatrix[i+1].append(i)
	#connect outputs
	for i in range(nNode-nOut+1,nNode):
		adjMatrix[i].append(i+1)
		adjMatrix[i+1].append(i)
	#TODO: check if connect input with output is nescessary?
	#connect input and output
	adjMatrix[1].append(nNode-nOut+1)
	adjMatrix[nNode-nOut+1].append(i)
	adjMatrix[2].append(nNode)
	adjMatrix[nNode].append(2)

	ap = findArticulationPoints(adjMatrix,time)
	#print(ap)
	#remove added edges:
	for i in range(1,nIn):
		adjMatrix[i].remove(i+1)
		adjMatrix[i+1].remove(i)
	for i in range(nNode-nOut+1,nNode):
		adjMatrix[i].remove(i+1)
		adjMatrix[i+1].remove(i)
	adjMatrix[1].remove(nNode-nOut+1)
	adjMatrix[nNode-nOut+1].remove(i)
	adjMatrix[2].remove(nNode)
	adjMatrix[nNode].remove(2)

	q = queue.Queue()
	s = {}
	for v in adjMatrix.keys():
		s[v] = 0
	counter = 0
	for n1 in ap:
		visited = {}
		for v in adjMatrix.keys():
			visited[v] = False
		q.queue.clear()
		for i in range(1,nIn+1):
			q.put(i)
		for i in range(nNode-nOut+1,nNode+1):
			q.put(i)
		while q.empty()==False:
			node = q.get()
			for n2 in adjMatrix[node]:
				if visited[n2]==False and s[n2]==counter:
					visited[n2]=True
					s[n2]+=1
					if n2!=n1:
						q.put(n2)
		counter+=1
	
	newList = []
	for v in adjMatrix.keys():
		if s[v]==len(ap):
			newList.append(v)
	#print(f'new list is {newList}')
	nEdge = 0
	for v,neighbors in adjMatrix.items():
		if v not in newList:
			adjMatrix[v] = []
			continue
		removed = []
		for n in neighbors:
			if n not in newList:
				removed.append(n)
		newneighbors = [n for n in neighbors if n not in removed]
		nEdge += len(newneighbors)
		adjMatrix[v] = newneighbors
	# for v,neighbors in grid.adjMatrix.items():
	# 	print(f'{v}: {neighbors}')
	#update number of edges
	nEdge = int(nEdge/2)
	return nEdge

# code taken from https://www.geeksforgeeks.org/connected-components-in-an-undirected-graph/
def getConnectedComponent(adjMatrix):
	visited = {}
	cc = []
	for key in adjMatrix.keys():
		visited[key] = False
	for v in adjMatrix.keys():
		if visited[v]==False:
			temp = []
			cc.append(dfsHelper(temp,v,visited,adjMatrix))
	return cc

def dfsHelper(temp,v,visited,adjMatrix):
	visited[v] = True
	temp.append(v)
	for neighbor in adjMatrix.get(v):
		if visited[neighbor]==False:
			temp = dfsHelper(temp,neighbor,visited,adjMatrix)
	return temp

# code taken from https://www.geeksforgeeks.org/articulation-points-or-cut-vertices-in-a-graph/
def findArticulationPoints(adjMatrix,time):
	visited = {}
	parent = {}
	ap = {}
	disc = {}
	low = {}
	for key in adjMatrix.keys():
		visited[key] = False
		parent[key] = -1
		ap[key] = False
		disc[key] = float("Inf")
		low[key] = float("Inf")

	for key in adjMatrix.keys():
		if visited[key]==False:
			apHelper(key,visited,parent,ap,disc,low,adjMatrix,time)
	result = []
	for key in ap.keys():
		if ap[key]==True:
			result.append(key)
	return result

def apHelper(node,visited,parent,ap,disc,low,adjMatrix,time):
	children = 0
	visited[node] = True
	disc[node] = time[0]
	low[node] = time[0]
	time[0] += 1

	for v in adjMatrix.get(node):
		if visited[v]==False:
			parent[v]=node
			children += 1
			apHelper(v,visited,parent,ap,disc,low,adjMatrix,time)
			# Check if the subtree rooted with v has a connection to 
            # one of the ancestors of u 
			low[node] = min(low[node],low[v])
			# u is an articulation point in following cases 
            # (1) u is root of DFS tree and has two or more chilren. 
			if parent[node]==-1 and children > 1:
				ap[node] = True
			#(2) If u is not root and low value of one of its child is more 
            # than discovery value of u.
			if parent[node]!=-1 and low[v] >= disc[node]:
				ap[node] = True
		elif v!=parent[node]:
			low[node] = min(low[node],disc[v])

# code taken from https://www.geeksforgeeks.org/biconnected-components/
def findBiconnected(adjMatrix,time):
	disc = {}
	low = {}
	parent = {}
	st = []
	bc = []
	for key in adjMatrix.keys():
		disc[key] = -1
		parent[key] = -1
		low[key] = -1
	for key in adjMatrix.keys():
		if disc[key]==-1:
			bccHelper(key,parent,low,disc,st,adjMatrix,time)
		while st:
			bc.append(st.pop())
	return bc
def bccHelper(node,parent,low,disc,st,adjMatrix,time):
	children = 0
	disc[node] = time[0]
	low[node] = time[0]
	time[0] += 1
	for v in adjMatrix.get(node):
		if disc[v]==-1:
			parent[v] = node
			children+=1
			st.append((node,v))
			bccHelper(v,parent,low,disc,st,adjMatrix,time)

			low[node] = min(low[node],low[v])
			if parent[node]==-1 and children > 1 or parent[node]!= -1 and low[v] >= disc[node]:
				w = -1
				while w!=(node,v):
					w = st.pop()
		elif v!=parent[node] and low[node] > low[v]:
			low[node] = min(low[node],disc[v])
			st.append((node,v))

  