from django import forms
from django.forms import formset_factory
from crispy_forms.bootstrap import InlineRadios, Div
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

class BasicForm(forms.Form):
	GRID_CHOICES=[(1,'Upload Grid from Text File'),(2,'Draw Grid')]
	DIFF_CHOICES=[(4.25e-5,'Fluorescein 4.25e-5'),(1.33e-4,'Na+ 1.33e-4')]
	nr = forms.IntegerField(required=False,label='Number of Rows:', min_value=2,max_value=20,widget=forms.TextInput(attrs={'placeholder': '8'}))
	nc = forms.IntegerField(required=False,label='Number of Columns:', min_value=2,max_value=20,widget=forms.TextInput(attrs={'placeholder': '8'}))
	w = forms.FloatField(label='Channel Width:',help_text='mm',min_value=1e-10,max_value=1000,widget=forms.TextInput(attrs={'placeholder': '0.2'}))
	l = forms.FloatField(label='Channel Length:',help_text='mm',min_value=1e-10,max_value=1000,widget=forms.TextInput(attrs={'placeholder': '1.5'}))
	diffCoeff = forms.FloatField(label='Diffusion Coefficient:',help_text='mm^2/s',min_value=1e-10,max_value=10,widget=forms.TextInput(attrs={'placeholder': '4.25e-5'}))
	#initV = forms.FloatField(label='Inlet Velocity: ',help_text='mm/s')
	input_type = forms.ChoiceField(choices = GRID_CHOICES, widget=forms.RadioSelect)
	input_file = forms.FileField(required=False,label='Input Text File:')
	
	### Render inline radio
	def __init__(self, *args, **kwargs):
		super(forms.Form, self).__init__(*args, **kwargs)
		self.initial['input_type'] = 2
		self.helper = FormHelper()
		self.helper.layout = Layout(Div(InlineRadios('input_type')))

