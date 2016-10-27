from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
	#html= "Rango says hey!" + '<br><a href="/rango/about/">Go to About</a>'
	context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
	return  render(request, 'rango/index.html',context=context_dict)
def about(request):
	#html = "Welcome to the about Page!" + '<br><a href="/rango/">Back to Rango</a>'
	return render(request,'rango/about.html')
