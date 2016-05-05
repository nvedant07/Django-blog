from django.shortcuts import render
from .forms import *
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.core.urlresolvers import resolve,reverse,get_script_prefix
from django.views.decorators.csrf import csrf_exempt
import os
import string
import random
import shutil
import time

def username_present(username):
    if User.objects.filter(username=username).exists():
        return True

    return False
def pass_generator(size=10,chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))



def firstpage(request):
	form=signinform(request.POST or None)
	return render(request,"signin.html",{"heading":"Sign In","form":form})

def signin(request):
	form=signinform(request.POST or None)
	context={
	"heading":"Sign In", 
	"form":form 
	}
	if form.is_valid():
		username=form.cleaned_data.get("email")
		password=form.cleaned_data.get("password")
		auth=authenticate(username=username,email=username,password=password)
		if auth is not None:
			login(request,auth)
			user=User.objects.get(username=username)
			global name
			name=user.first_name
			global username_unique
			username_unique=user.username
			template="home.html"
			context={"name":name}
			return render(request,template,context)
		else:
			template="signin.html"
			context={
			"heading":"Username and password does not match", 
			"form":form 
			}
			return render(request,template,context)
	else:
		template="signin.html"
		return render(request,template,context)

@login_required(login_url='signin')
def home(request):
	context={"name":name}
	return render(request,"home.html",context)

def signup(request):
 	form=signupform(request.POST or None)
 	context={
 	"heading":"Sign Up",
 	"form":form
 	}
 	template="signup.html"
 	return render(request,template,context)

def signupvalidation(request):
 	form=signupform(request.POST or None)
 	
 	context={
	"heading":"Sign Up",
	"form":form
 	}
	 	
 	if form.is_valid():
 		p=form.cleaned_data.get("password")
 		rp=form.cleaned_data.get("re_type_password")
 		username=form.cleaned_data.get("email")
 		first_name=form.cleaned_data.get("firstname")
 		last_name=form.cleaned_data.get("lastname")
 		# num_results = User.objects.filter(email = cleaned_info['username']).count()
 		
 		if((p==rp) and username_present(username)==False):
 			user=User.objects.create_user(username,username,p)
 			user.first_name=first_name
 			user.last_name=last_name
 			user.save()
 			os.mkdir(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username)
 			os.mkdir(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username+"/myblogs")
 			os.mkdir(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username+"/bookmarked")
 			new_form=signinform(request.POST or None)
 			context={
 			"heading":"Succesful Sign Up! Sign in here:",
 			"form":new_form
 			}
 			template="signin.html"
 			return render(request,template,context)
 		elif(p!=rp):
 			context={
 			"heading":"Passwords don't match",
 			"form":form
 			}
 			template="signup.html"
 			return render(request,template,context)
 		else:
 			context={
 			"heading":"Email already exists",
 			"form":form
 			}
 			template="signup.html"
 			return render(request,template,context)	
 	else:
 		template="signup.html"
 		return render(request,template,context)	

@login_required(login_url='signin')
def Logout(request):
	logout(request)
	form=signinform(request.POST or None)
	context={
	"heading":"Sign In", 
	"form":form 
	}
	return render(request, "signin.html", context)

def forgotpassword(request):
	form=passform(request.POST or None)
	context={
	"heading":"Forgot password",
	"form":form
	}
	if form.is_valid():
		form_email=form.cleaned_data.get("email")

		if(username_present(form_email)==True):
			password=pass_generator()
			subject='New password'
			sender=settings.EMAIL_HOST_USER
			receiver=[form_email]
			message="New password for %s is: %s"%(form_email,password) 
			u=User.objects.get(username=form_email)
			u.set_password(password)
			u.save()
			send_mail(subject,
		 			message,
		  			sender,
	    			receiver,
	     			fail_silently=False)
			context={
			"heading":"New password sent",
			"form":form
			}
		else:
			context={
			"heading":"Email is not registered",
			"form":form
			}
	return render(request,"passforgot.html",context)

@login_required(login_url='signin')
def changepassword(request):
	form=changepassform(request.POST or None)
	context={
	"heading":"Change Password",
	"form":form
	}
	if form.is_valid():
		# username=form.cleaned_data.get("email")
		password=form.cleaned_data.get("current_password")
		np=form.cleaned_data.get("new_password")
		npr=form.cleaned_data.get("re_type_new_password")
		auth=authenticate(username=username_unique,email=username_unique,password=password)
		if auth is not None and np==npr:
			u=User.objects.get(username=username_unique)
			u.set_password(np)
			u.save()
			context={
			"heading":"Password changed sucessfully!",
			"form":form
			}
			a=authenticate(username=username_unique,email=username_unique,password=np)
			login(request,a)
		elif auth is None:
			context={
			"heading":"Username and password do not match",
			"form":form
			}
		elif auth is not None and np!=npr:
			context={
			"heading":"New passwords do not match",
			"form":form
			}
	return render(request,"passchange.html",context)

@login_required(login_url='signin')
def delaccount(request):
	u=User.objects.get(username=username_unique)
	u.delete()
	shutil.rmtree(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique)
	form=signinform(request.POST or None)
	return render(request,"signin.html",{"heading":"Sign In","form":form})	

global my_blogs_filenames
my_blogs_filenames=[]
global my_blogs                ##FIX THIS URGENTLY!
my_blogs=[]
global timestamp
timestamp={}
global link_text
link_text=[]

@login_required(login_url='signin')
def write(request):
	form=newblog(request.POST or None)
	context={
	"heading":"Now Writing...",
	"form":form
	}

	if form.is_valid():
		filename=form.cleaned_data.get("title")
		data=form.cleaned_data.get("content")
		count=0
		for some_file in my_blogs:
			if filename==some_file:
				count+=1
		my_blogs.append(filename)
		if count>0:	
			f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/myblogs/"+filename+"--"+str(count)+".txt",'w')
			f.write(data)
			f.close()
			now = time.strftime("%c")
			my_blogs_filenames.append(filename+"--"+str(count))
			timestamp[filename+"--"+str(count)]=now
		else:
			f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/myblogs/"+filename+".txt",'w')
			f.write(data)
			f.close()
			now = time.strftime("%c")
			my_blogs_filenames.append(filename)
			timestamp[filename]=now
		context={
		"heading":"Saved!",
		"form":form
		}
		return render(request,"write.html",context)
	else:
		return render(request,"write.html",context)

@login_required(login_url='signin')
def myblogs(request):
	file_list=my_blogs_filenames
	context={
	'file_list':file_list
	}
	return render(request,"myblogs.html",context)

@login_required(login_url='signin')
@csrf_exempt
def read(request):
	link_text.append(request.body)	
	if (len(link_text)==2):
		name=link_text[0]
	else:
		name=link_text[-2]
	# blog=str(request)
	# blog=blog.lstrip("<WSGIRequest: GET '/read")
	# blog=blog.lstrip("\%3D")
	# blog=blog.rstrip("'>")
	# t=list(blog)
	# for i in range (len(t)):
	# 	if t[i]=="%":
	# 		if t[i+1]=='2' and t[i+2]=='0':
	# 			t[i]=' '
	# 			t[i+1]=''
	# 			t[i+2]=''
	# name=''
	# for c in t:
	# 	name+=c

	u=User.objects.get(username=username_unique)
	author_name=u.first_name+" "+u.last_name
	
	time=timestamp[name]
	
	f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/myblogs/"+name+".txt",'r')
	temp=[]
	i=0
	for line in f:
		temp.append(line.rstrip('\n'))
	context={
	"title":name,
	"temp":temp,
	"author_name":author_name,
	"timestamp":time
	}

	return render(request,"read.html",context)

