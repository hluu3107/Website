from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .forms import *
from .process import *

def user_input(request):
	"""This is the input form for grid information
    """
	if request.method == 'POST':
    	# If request if POST get form info
		form = BasicForm(request.POST, request.FILES)
		if form.is_valid():
			data = request.POST.copy()
			if(data.get('input_type')=='1'):
				#Upload text file
				input_file = request.FILES.get('input_file')
				#TODO Verify input file
				nEdge,adjMatrix = process_input(input_file,int(data.get('nr')),int(data.get('nc')))			
				data['nEdge'] = str(nEdge)
				data['adjMatrix'] = json.dumps(adjMatrix)
				request.session['data'] = data
				#return redirect(result)
				request.session['draw'] = False
				return redirect(draw)
			else:
				#Draw grid
				request.session['data'] = data
				request.session['draw'] = True
				return redirect(draw)
		else:
			#TODO form error
			print("Error form")
	else:
		# If request if GET print empty form
		form = BasicForm()
	return render(request,'grid/basic_input.html',{'form': form})

def result(request):
	"""This is the result view with print out grid
    """	
	data = request.session.get('data')
	grid = createGrid(data)		
	solveGrid(grid)
	cString,vString = getResult(grid)	
	data['cString'] = cString
	data['vString'] = vString
	graph = getJsonGraph(grid)
	data['graph'] = graph
	# if request.session['draw']==True:
	# 	del request.session['draw']	
	return render(request,'grid/result.html',{'data':data})
	# else:
	# 	return redirect(user_input)

@csrf_exempt
def grid_input(request):
	"""This is the graphical graph input view
    """
	if request.method == 'POST':
		data = request.session.get('data')
		postdata = request.POST.copy()
		dt = data
		dt['graph'] = postdata.get('graph')
		#if ajax request	
		if(postdata.get('status')=='1'):
			#check if graph is connected. 					
			isValid, adjMatrix, nEdge = verifyInputGraph(data)
			if isValid==False:
				#if not valid output error msg in the same page
				return HttpResponse('0')
			else:
				#if ok simplify the grid, call result go to result page
				data['adjMatrix'] = json.dumps(adjMatrix)
				data['nEdge'] = str(nEdge)
				request.session['data'] = data
				request.session['draw'] = True
				return HttpResponse('1')
	if request.session['draw'] == True:
		### Get size from session variable and render empty grid of given size
		data = request.session.get('data')		
		graph = createEmptyGrid(data)
		### render empty grid		
		return render(request,'grid/input.html',{'graph':graph})
	return redirect(user_input)

@csrf_exempt
def draw(request):
	"""This is the graphical graph input view
    """
	if request.method == 'POST':
    	#if ajax request
		data = request.session.get('data')
		postdata = request.POST.copy()
		data['graph'] = postdata.get('graph')
		if(postdata.get('status')=='1'):
			#check if graph is connected. 					
			isValid, adjMatrix, nEdge = verifyInputGraph(data)
			if isValid==False:
				#if not valid output error msg in the same page
				return HttpResponse('0')
			else:
				data['adjMatrix'] = json.dumps(adjMatrix)
				data['nEdge'] = str(nEdge)
				grid = createGrid(data)		
				solveGrid(grid)
				cString,vString = getResult(grid)
				data['cList'] = cString
				data['vList'] = vString
				graph = getJsonGraph(grid)
				data['graph'] = graph
				return HttpResponse(json.dumps(data))
	elif request.session['draw'] == True:
		### Get size from session variable and render empty grid of given size
		data = request.session.get('data')		
		graph = createEmptyGrid(data)
		data['graph'] = graph
		### render empty grid		
		#return render(request,'grid/draw_grid.html',{'graph':graph})
	elif request.session['draw']==False:
		data = request.session.get('data')
		grid = createGrid(data)		
		solveGrid(grid)
		cString,vString = getResult(grid)
		print(f'c: {cString}), v: {vString}')
		data['cList'] = cString
		data['vList'] = vString
		graph = getJsonGraph(grid)
		data['graph'] = graph
	return render(request,'grid/draw_grid.html',{'data':data})