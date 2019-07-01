from django.urls import path
from . import views

urlpatterns = [
	# path('',views.form_input, name='form_input'),
	path('',views.user_input, name='user_input'),
	path('result',views.result, name='result'),
	path('input',views.grid_input, name='grid_input'),
	path('draw',views.draw,name='draw'),
]