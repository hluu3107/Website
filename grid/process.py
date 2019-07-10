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
	nEdge,adjMatrix = reduceGrid(adjMatrix,nr,nc)
	initCl = data.get('initC').split(",")
	initVl = data.get('initV').split(",")
	initC = {}
	initV = {}
	for i in range(1,nc+1):
		initC[i] = float(initCl[i-1])
		initV[i] = float(initVl[i-1])
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

#produce fix graph
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

def createGridFromFile(data):
	nEdge,adjMatrix = getMatrixJson(data)
	nr = int(data.get('nr'))
	nc = int(data.get('nc'))
	graph = createEmptyGrid(data)
	eclickcolor = "#fbaf08"
	for edge in graph["edges"]:
		source = int(edge["source"])
		target = int(edge["target"])
		if source < target and source in adjMatrix[target]:
			edge["selected"] = True
			edge["color"] = eclickcolor
	for node in graph["nodes"]:
		n = int(node["id"])
		if adjMatrix[n]:
			node["color"] = eclickcolor
	return graph

def createEmptyGrid(data):
	nr = int(data.get('nr'))
	nc = int(data.get('nc'))
	nodes = []
	edges = []
	nsize = 2
	nColor = "#e1e8f0"	
	eclickcolor = "#fbaf08"
	inColor = "#00a0a0"
	esize = 0.5
	nNode = int((nr+2) * nc)
	# create nodes
	for i in range(1,nNode+1):
		node = {"id": str(i), "x": (i-1)%nc, "y":int((i-1)/nc), "size": nsize, "color":nColor}
		# create labels for input
		if i in range(1,nc+1):
			node["label"] = "I" + str(i)
			#node["color"] = inColor
		# create labels for ouput
		if i in range(nNode-nc+1,nNode+1):
			node["label"] = "O" + str(i-(nc*(nr+1)))
			#node["color"] = inColor
		nodes.append(node)	

	#create normal edges
	for snode in range(nc+1,nNode-nc+1):
		#create horizontal edges
		if snode%nc!=0:
			edge = {"id": str(snode)+"-"+str(snode+1), "source": str(snode), "target": str(snode+1), \
			"size": esize, "selected": False, "mutable": True,"color": nColor}
			edges.append(edge)
		#create vertical edges
		if int((snode-1)/nc) <= nr:
			edge = {"id": str(snode)+"-"+str(snode+nc), "source": str(snode), "target": str(snode+nc), "size": esize, \
			"mutable": True, "selected": False,"color": nColor}
			edges.append(edge)	
	
	#create only vertical edges for input
	for snode in range(1,nc+1):
		edge = {"id": str(snode)+"-"+str(snode+nc), "source": str(snode), "target": str(snode+nc), "size": esize, \
			"mutable": True, "selected": False, "color": nColor}		
		edges.append(edge)
	
	graph = {"nodes": nodes, "edges": edges}
	return graph

def verifyInputGraph(data):
	adjMatrix, nEdge = getMatrixInput(data.get('graph'))
	nr = int(data.get('nr'))
	nc = int(data.get('nc'))
	nNode = int((nr+2) * nc)
	inNodes = []
	outNodes = []
	
	for i in range(1,nc+1):
		if adjMatrix[i]:
			inNodes.append(i)
	# if no input
	if not inNodes:
		return False,adjMatrix, nEdge
	
	for i in range(nNode-nc+1,nNode+1):
		if adjMatrix[i]:
			outNodes.append(i)
	# if no input
	if not outNodes:
		return False,adjMatrix, nEdge

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

def reduceGrid(adjMatrix,nr,nc):
	time = [0]
	nNode = int((nr+2) * nc)
	originalIn = []
	for i in range(1,nc+1):
		if adjMatrix[i]:
			originalIn.append(i)
	originalOut = []
	for i in range(nNode-nc+1,nNode+1):
		if adjMatrix[i]:
			originalOut.append(i)

	#connect inputs
	for i in range(1,nc):
		adjMatrix[i].append(i+1)
		adjMatrix[i+1].append(i)
	#connect outputs
	for i in range(nNode-nc+1,nNode):
		adjMatrix[i].append(i+1)
		adjMatrix[i+1].append(i)
	#connect input and output
	adjMatrix[1].append(nNode-nc+1)
	adjMatrix[nNode-nc+1].append(1)
	adjMatrix[nc].append(nNode)
	adjMatrix[nNode].append(nc)
	cc = getConnectedComponent(adjMatrix)
	#print(cc)
	#remove component not connect to input
	for comp in cc:
		if 1 not in comp:
			for v in comp:
				for n in adjMatrix[v]:
					adjMatrix[n].remove(v)
				adjMatrix[v] = []	
	#find biconnected components
	bc = findBiconnected(adjMatrix,time)
	#print(f'bi connected comp {bc}')
	mc = []
	for comp in bc:
		if all(x in comp for x in list(range(1,nc+1))) and all(x in comp for x in  list(range(nNode-nc+1,nNode+1))):
			mc = comp
			break
	#print(f'main comp {mc}')
	time = [0]
	ap = findArticulationPoints(adjMatrix,time)
	#print(f'articulation points {ap}')
	mains = list(set(ap)&set(mc))
	#print(f'removed points {mains}')
	for comp in bc:
		if comp==mc:
			continue
		for v in comp:
			if v not in mains:
				for u in adjMatrix[v]:
					adjMatrix[u].remove(v)
				adjMatrix[v]=[]
	#remove added edges
	adjMatrix[1].remove(nNode-nc+1)
	adjMatrix[nNode-nc+1].remove(1)
	adjMatrix[nc].remove(nNode)
	adjMatrix[nNode].remove(nc)

	for i in range(1,nc+1):
		if i not in originalIn:
			adjMatrix[i] = []
		else:
			adjMatrix[i] = [i+nc]
	for i in range(nNode-nc+1,nNode+1):
		if i not in originalOut:
			adjMatrix[i] = []
		else:
			adjMatrix[i] = [i-nc]
	#print(adjMatrix)
	#count edges again
	nEdges = 0
	for v,neighbors in adjMatrix.items():
		nEdges+=len(neighbors)
	return int(nEdges/2),adjMatrix

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
			bccHelper(key,parent,low,disc,st,adjMatrix,time,bc)
		if st:
			comp = []
			while st:
				w = st.pop()
				comp.append(w)
			bc.append(comp)
	bcv = []
	for list in bc:
		vset = set()
		for (u,v) in list:
			vset.add(u)
			vset.add(v)
		bcv.append(vset)	
	return bcv

def bccHelper(node,parent,low,disc,st,adjMatrix,time,bc):
	children = 0
	disc[node] = time[0]
	low[node] = time[0]
	time[0] += 1
	for v in adjMatrix.get(node):
		if disc[v]==-1:
			parent[v] = node
			children+=1
			st.append((node,v))
			bccHelper(v,parent,low,disc,st,adjMatrix,time,bc)

			low[node] = min(low[node],low[v])
			if parent[node]==-1 and children > 1 or parent[node]!= -1 and low[v] >= disc[node]:
				w = -1
				comp = []
				while w!=(node,v):
					w = st.pop()
					comp.append(w)
				bc.append(comp)
		elif v!=parent[node] and low[node] > low[v]:
			low[node] = min(low[node],disc[v])
			st.append((node,v))

def processInputCV(data):
	nc = int(data.get('nc'))
	initC = {}
	initV = {}
	for i in range(1,nc+1):
		initC[i] = 0
		initV[i] = 0
	return initC, initV
