from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .forms import *
from .process import *

def user_input(request):
	"""This is the input form for grid information
    """
    #TODO error check
	if request.method == 'POST':
    	# If request if POST get form info
		form = BasicForm(request.POST, request.FILES)
		if form.is_valid():
			data = request.POST.copy()
			init = [0] * int(data.get('nc'))
			if not data.get('initV'):				
				data['initV'] = ",".join(map(str,init))
			if not data.get('initC'):
				data['initC'] = ",".join(map(str,init))
			if(data.get('input_type')=='1'):
				#Upload text file
				input_file = request.FILES.get('input_file')
				#TODO Verify input file
				nEdge,adjMatrix = process_input(input_file,int(data.get('nr')),int(data.get('nc')))			
				data['nEdge'] = str(nEdge)
				data['adjMatrix'] = json.dumps(adjMatrix)
				request.session['data'] = data
				request.session['draw'] = False
				return redirect(draw)
			else:
				#Draw grid
				request.session['data'] = data
				request.session['draw'] = True
				return redirect(draw)
		else:
			print("Error form")
	else:
		# If request if GET print empty form
		form = BasicForm()
	return render(request,'grid/basic_input.html',{'form': form})

@csrf_exempt
def draw(request):
	"""This is the graphical graph input view
    """
	if request.method == 'POST':
    	#if ajax request
		data = request.session.get('data')
		postdata = request.POST.copy()
		data['graph'] = postdata.get('graph')
		if postdata.get('status')=='1':
			#check if graph is connected. 					
			isValid, adjMatrix, nEdge = verifyInputGraph(data)
			if isValid==False:
				#if not valid output error msg in the same page
				return HttpResponse('0')
			else:
				data['initC'] = postdata.get('ic')
				data['initV'] = postdata.get('iv')
				data['adjMatrix'] = json.dumps(adjMatrix)
				data['nEdge'] = str(nEdge)
				grid = createGrid(data)		
				solveGrid(grid)
				cString,vString = getResult(grid)
				resultList = list(zip(cString,vString))
				data['resultList'] = resultList
				graph = getJsonGraph(grid)
				data['graph'] = graph
				return HttpResponse(json.dumps(data))		
	elif request.session['draw'] == True:
		### Get size from session variable and render empty grid of given size
		data = request.session.get('data')		
		graph = json.dumps(createEmptyGrid(data))
		initC,initV = processInputCV(data.get('initC'),data.get('initV'))
		data['initC'] = initC
		data['initV'] = initV	
		data['graph'] = graph
		### render empty grid		
		#return render(request,'grid/draw_grid.html',{'graph':graph})
	elif request.session['draw']==False:
		data = request.session.get('data')
		graph = json.dumps(createGridFromFile(data))
		# grid = createGrid(data)		
		# solveGrid(grid)
		# cString,vString = getResult(grid)
		# resultList = zip(cString,vString)
		# data['resultList'] = resultList
		# data['initC'] = grid.initC
		# data['initV'] = grid.initV
		# #print(f'c: {cString}), v: {vString}')		
		# graph = getJsonGraph(grid)
		initC,initV = processInputCV(data.get('initC'),data.get('initV'))
		data['initC'] = initC
		data['initV'] = initV	
		data['graph'] = graph
	return render(request,'grid/draw_grid.html',{'data':data})

