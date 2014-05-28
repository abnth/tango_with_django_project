from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse

def index(request):
    context=RequestContext(request)
    category_list=Category.objects.order_by('-likes')[:5]
    context_dict={'categories':category_list}
    return render_to_response('rango/index.html',context_dict,context)
def about(request):
	context=RequestContext(request)
	context_dict={'message':"this is the message from about voew to about template"}
	return render_to_response("rango/about.html",context_dict,context)

def category(request,category_name_url):
	context=RequestContext(request)
	category_name_url=category_name_url.replace('_',' ')
	#fetch the category pages
	print category_name_url
	category=Category.objects.get(name=category_name_url)
	pages=Page.objects.filter(category=category)
	#pages is a list of pages
	category_dict={'pages':pages}
	category_dict['category']=category
	return render_to_response('rango/category.html',category_dict,context)#view name goes here
def add_category(request):
	context=RequestContext(request)
	if(request.method=='POST'):
		form=CategoryForm(request.POST)
		if(form.is_valid()):
			#valid form save it in db
			form.save(commit=True)
			return index(request)#no need to call render to response as we are already in the views file.that has to be called from a viiew to a template
		else:
			#invalid form ; redisplay the form by calling the related template
			#context_dict={'form':form}
			#return render_to_response('display_form.html',context_dict,context)
			print form.errors #print errors to terminal
	else:
		#the request method was not post or there has been an error
		form= CategoryForm()		
		context_dict={'form':form}
		return render_to_response('rango/add_category.html',context_dict,context)#the add_category template is in the rango directory within the template folder so goes the rango/.. thing


#adding a new page to a category
#def add_page(request,category_name_url):
	#context=RequestContext(request)
	#category_name=category_name_url.replace('_',' ')
	#if request.method=="POST":
		#have to create a new form
		#form=PageForm(request.POST)
		#now after checking category exists do 
from rango.forms import PageForm

def add_page(request, category_name_url):
    context = RequestContext(request)

    category_name = category_name_url.replace('_',' ')
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            # This time we cannot commit straight away.
            # Not all fields are automatically populated!
            page = form.save(commit=False)#form.save returns an instance of the form to work 

            # Retrieve the associated Category object so we can add it.
            # Wrap the code in a try block - check if the category actually exists!
            try:
                cat = Category.objects.get(name=category_name)
                page.category = cat
            except Category.DoesNotExist:
                # If we get here, the category does not exist.
                # Go back and render the add category form as a way of saying the category does not exist.
                return render_to_response('rango/add_category.html', {}, context)

            # Also, create a default value for the number of views.
            page.views = 0

            # With this, we can then save our new model instance.
            page.save()

            # Now that the page is saved, display the category instead.
            return category(request, category_name_url)
        else:
            print form.errors
    else:
        form = PageForm()

    return render_to_response( 'rango/add_page.html',
            {'category_name_url': category_name_url,
             'category_name': category_name, 'form': form},
             context)



def register(request):
	context=RequestContext(request)
	registered = False
	if(request.method=="POST"):
		#process the form
		user_form=UserForm(data=request.POST)
		profile_form=UserProfileForm(data=request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			user=user_form.save()
			user.set_password(user.password)
			user.save()#hashing the pwd
			profile=profile_form.save(commit=False)	
			profile.user=user#This is where we populate the user attribute of the UserProfileForm form, which we hid from users
			if 'picture' in request.FILES:
				profile.picture=request.FILES['picture']
			profile.save()
			registered=True
		else:
			print user_form.errors, profile_form.errors
	else:
		user_form=UserForm()
		profile_form=UserProfileForm()
	return render_to_response(
            'rango/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

def user_login(request):
    context=RequestContext(request)
    if request.method=="POST":
	#process the login
	#get uname
	username=request.POST['username']
	password=request.POST['password']
	user= authenticate(username=username,password=password)   #authentticate
	if user:
	    if user.is_active:
		login(request,user)
		return HttpResponseRedirect("/rango/")
	    else:
		print "inactive user.cannot login"
		return HttpResponse("your account is inactive can't log you in")
	else:
	    #if auhenticated ie a user object is returned then login and redirect to home; else display the error
	    print "invalid username and password"
	    return HttpResponse("wrong login details")
	    
    else:
	#the form has to be displayed
	return render_to_response('rango/login.html',{},context)

