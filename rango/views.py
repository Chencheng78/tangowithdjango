from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from rango.models import Category,Page
from rango.forms import CategoryForm,PageForm,UserForm,UserProfileFrom
from django.contrib.auth import authenticate,login
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

def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
           # print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'rango/login.html', {})
# def user_login(request):
# 	if request.method == 'POST':
# 		username = request.POST.get('username')
# 		password = request.POST.get('password')
# 		user = authenticate(username=username,password=password)
# 		if user:
# 			if user.is_active:
# 				login(request,user)
# 				return HttpResponseRedirect('/rango/')
# 			else:
# 				return HttpResponse("your Rango accout is disabled.")
# 		else:
# 			#print("Invalid login details: {0},{1}".format(username,password))
# 			return HttpResponse("Invalid login detials suppied.")
#
# 	else:
# 		return render(request,'rango/login.html',{})