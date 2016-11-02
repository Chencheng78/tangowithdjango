from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category,Page
from rango.forms import CategoryForm,PageForm,UserForm,UserProfileFrom
# Create your views here.
def index(request):
	#html= "Rango says hey!" + '<br><a href="/rango/about/">Go to About</a>'
	#context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
	category_list = Category.objects.order_by("-likes")[:5]
	page_list = Page.objects.order_by('-views')[:5]
	context_dict = {'categories': category_list,'pages':page_list}

	return  render(request, 'rango/index.html',context=context_dict)
def about(request):
	#html = "Welcome to the about Page!" + '<br><a href="/rango/">Back to Rango</a>'
	return render(request,'rango/about.html')

def show_category(request,category_name_slug):
	context_dict ={}
	try:
		category = Category.objects.get(slug = category_name_slug)
		pages = Page.objects.filter(category=category)
		context_dict['pages'] = pages
		context_dict['category'] = category
	except Category.DoesNotExist:
		context_dict['category'] = None
		context_dict['pages'] = None
	return render(request, 'rango/category.html',context_dict)

def add_category(request):
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		if form.is_valid():
			form.save(commit=True)

			return index(request)
		else:
			print(form.errors)
	else:
		form = CategoryForm()
	return render(request,'rango/add_category.html',{'form':form})

def add_page(request,category_name_slug):
	try:
		cat = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		cat = None

	if request.method=='POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if cat:
				page = form.save(commit=False)
				page.category = cat
				page.views = 0
				page.save()

				return show_category(request,category_name_slug)
		else: print(form.errors)
	else: form= PageForm()

	context_dict = {'form':form,'category':cat }
	return render(request,'rango/add_page.html',context_dict)

def register(request):
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileFrom(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

				profile.save()

				registered = True
			else:
				print(user_form.errors,profile_form.errors)
	else:
		user_form = UserForm()
		profile_form=UserProfileFrom()

	return  render(request,
	               'rango/register.html',
	               {'user_form':user_form,
	                'profile_form':profile_form,
	                'registered':registered}
	               )

