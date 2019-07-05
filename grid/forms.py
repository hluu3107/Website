from django import forms
from django.forms import formset_factory
from crispy_forms.bootstrap import InlineRadios, Div
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

class BasicForm(forms.Form):
	GRID_CHOICES=[(1,'Upload Text File'),(2,'Draw Grid')]
	nr = forms.IntegerField(label='Number of row:')
	nc = forms.IntegerField(label='Number of col:')
	w = forms.FloatField(label='Channel Width:',help_text='mm')
	l = forms.FloatField(label='Channel Length:',help_text='mm')
	diffCoeff = forms.FloatField(label='Diffusion Coefficient:',help_text='mm^2/s')
	#initV = forms.FloatField(label='Inlet Velocity: ',help_text='mm/s')
	input_type = forms.ChoiceField(choices = GRID_CHOICES, widget=forms.RadioSelect)
	input_file = forms.FileField(required=False,label='Input File (Optional):',help_text='txt file only')
	
	### Render inline radio
	def __init__(self, *args, **kwargs):
		super(BasicForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(Div(InlineRadios('input_type')))
		

class InletSetup(forms.Form):
	inC = forms.FloatField(label='Inlet Concentration:')
	inV = forms.FloatField(label='Inlet Velocity:')
