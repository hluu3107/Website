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
    	# If request is POST get form info
		form = BasicForm(request.POST, request.FILES)
		if form.is_valid():
			data = request.POST.copy()
			if(data.get('input_type')=='1'):
				#Upload text file
				input_file = request.FILES.get('input_file')
				#TODO Verify input file
				nEdge,adjMatrix,nr,nc = process_input(input_file)
				nEdge,adjMatrix = reduceGrid(adjMatrix,nr,nc)			
				data['nEdge'] = str(nEdge)
				data['adjMatrix'] = json.dumps(adjMatrix)
				data['nr'] = str(nr)
				data['nc'] = str(nc)
				request.session['data'] = data
				request.session['draw'] = False
				return redirect(draw)
			else:
				#Draw grid
				request.session['data'] = data
				request.session['draw'] = True
				return redirect(draw)
		# else:
		# 	print("Error form")
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
				isInletValid, initC, initV = validateInlet(data)	
				if isInletValid==1:
					return HttpResponse('1')
				if isInletValid==2:
					return HttpResponse('2')
				data['adjMatrix'] = json.dumps(adjMatrix)
				data['nEdge'] = str(nEdge)				
				grid = createGrid(data,initC,initV)
				data['adjMatrix'] = json.dumps(grid.adjMatrix)
				data['nEdge'] = grid.nEdge			
				graph = json.dumps(createGridFromFile(data))				
				solveGrid(grid)
				cString,vString = getResult(grid)
				resultList = list(zip(cString,vString))
				data['resultList'] = resultList
				data['graph'] = graph
				return HttpResponse(json.dumps(data))
		elif postdata.get('status')=='2':
			isValid, adjMatrix, nEdge = verifyInputGraph(data)
			nr = int(data.get('nr'))
			nc = int(data.get('nc'))
			content = exportToFile(nr,nc,adjMatrix)
			filename = "mygrid.txt"
			response = HttpResponse(content, content_type='text/plain')
			# response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
			return HttpResponse(json.dumps(content))
	data = request.session.get('data')
	data["draw"] = request.session['draw']
	if request.session['draw'] == True:	
		graph = json.dumps(createEmptyGrid(data))
	elif request.session['draw']==False:
		graph = json.dumps(createGridFromFile(data))
	else:
		return redirect(user_input)
	data['graph'] = graph
	#create empty inlet fields
	initC,initV = processInputCV(data)
	data['initC'] = initC
	data['initV'] = initV	
	return render(request,'grid/draw_grid.html',{'data':data})

def tutorial(request):
	return render(request,'grid/tutorial.html')

def contact(request):
	return render(request,'grid/contact.html')

@csrf_exempt
def download(request):
	if request.method == 'POST':
		data = request.session.get('data')
		postdata = request.POST.copy()
		data['graph'] = postdata.get('graph')
		isValid, adjMatrix, nEdge = verifyInputGraph(data)
		nr = int(data.get('nr'))
		nc = int(data.get('nc'))
		content = exportToFile(nr,nc,adjMatrix)
		return HttpResponse(content)
	return redirect(user_input)