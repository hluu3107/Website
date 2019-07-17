from django.urls import path
from . import views
urlpatterns = [
	path('',views.user_input, name='user_input'),
	path('draw',views.draw,name='draw'),
	path('tutorial',views.tutorial,name='tutorial'),
	path('contact',views.contact,name='contact'),
]
