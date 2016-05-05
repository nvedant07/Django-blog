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
 			f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username+"/timestamp.txt",'w')
 			f.close()
 			f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username+"/my_blogs_titles.txt",'w')
 			f.close()
 			f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username+"/my_blogs_filenames.txt",'w')
 			f.close()
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
		f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/my_blogs_titles.txt")
		
		for line in f:
			if filename==line.rstrip('\n'):
				count+=1
		f.close()
		f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/my_blogs_titles.txt",'a')
		f.write(filename+"\n")
		
		if count>0:	
			f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/myblogs/"+filename+"--"+str(count)+".txt",'w')
			f.write(data)
			f.close()
			now = time.strftime("%c")
			f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/my_blogs_filenames.txt",'a')
			f.write(filename+"--"+str(count)+"\n")
			f.close()
			f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/timestamp.txt",'a')
			f.write(filename+"--"+str(count)+":"+str(now)+"\n")
			f.close()
		else:
			f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/myblogs/"+filename+".txt",'w')
			f.write(data)
			f.close()
			now = time.strftime("%c")
			f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/my_blogs_filenames.txt",'a')
			f.write(filename+"\n")
			f.close()
			f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/timestamp.txt",'a')
			f.write(filename+":"+str(now)+"\n")
			f.close()
		context={
		"heading":"Saved!",
		"form":form
		}
		return render(request,"write.html",context)
	else:
		return render(request,"write.html",context)

@login_required(login_url='signin')
def myblogs(request):
	file_list=[]
	f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/my_blogs_filenames.txt",'r')
	for line in f:
		file_list.append(line.rstrip('\n'))
	file_list.reverse()
	context={
	'file_list':file_list
	}
	return render(request,"myblogs.html",context)

global link_text
link_text=[]
@login_required(login_url='signin')
@csrf_exempt
def read(request):
	link_text.append(request.body)
	if (len(link_text)==2 or len(link_text)==1):
		title_name=link_text[0]
	else:
		title_name=link_text[-2]

	if (title_name!=''):
		u=User.objects.get(username=username_unique)
		author_name=u.first_name+" "+u.last_name
		
		f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/timestamp.txt",'r')
		times=f.readlines()
		f.close()
		time=''
		temp_time=[]
		for somefilestime in times:
			if title_name in somefilestime:
				temp_time.append(somefilestime)
		for data in temp_time:
			i=len(data)-26
			filename=data[0:i]
			if filename==title_name:
				time=data[i+1:len(data)-1]
			
		f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/myblogs/"+title_name+".txt",'r')
		temp=[]
		i=0
		for line in f:
			temp.append(line.rstrip('\n'))
		f.close()
		context={
		"title":title_name,
		"temp":temp,
		"author_name":author_name,
		"timestamp":time
		}

		return render(request,"read.html",context)
	else:
		file_list=[]
		f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/my_blogs_filenames.txt",'r')
		for line in f:
			file_list.append(line.rstrip('\n'))
		context={
		'file_list':file_list
		}
		return render(request,"myblogs.html",context)

@login_required(login_url='signin')
@csrf_exempt
def deleteblog(request):
	filename=str(request.body)
	if(filename!=''):
		os.remove(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/myblogs/"+filename+".txt")
		f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/my_blogs_filenames.txt",'r')
		filename_array=f.readlines()
		f.close()
		i=-1
		for var in filename_array:
			i+=1
			if(var==(filename+"\n")):
				filename_array.remove(var)
				break
		f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/my_blogs_filenames.txt",'w')
		for var in filename_array:
			f.write(var)
		f.close()
		f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/my_blogs_titles.txt",'r')
		filetitle_array=f.readlines()
		f.close()
		del filetitle_array[i]
		f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/my_blogs_titles.txt",'w')
		for var in filetitle_array:
			f.write(var)
		f.close()
		f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/timestamp.txt",'r')
		filetimestamp_array=f.readlines()
		f.close()
		del(filetimestamp_array[i])
		f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/timestamp.txt",'w')
		for var in filetimestamp_array:
			f.write(var)
		f.close()
		
	file_list=[]
	f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/my_blogs_filenames.txt",'r')
	for line in f:
		file_list.append(line.rstrip('\n'))
	f.close()
	context={
	'file_list':file_list
	}
	return render(request,"myblogs.html",context)

global read_title
read_title=[]
@login_required(login_url='signin')
@csrf_exempt
def editblog(request):
	read_title.append(request.body)
	if (len(read_title)%2 != 0):
		title_name=''
	else:
		if(read_title[-1]!=''):
			title_name=read_title[-1]
		else:
			title_name=read_title[-2]
	print (read_title)
	if (title_name!='' and os.path.exists(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/myblogs/"+title_name+".txt")):
		f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/myblogs/"+title_name+".txt",'r')
		string=f.read()
		f.close()
		#getting the title corresponding to the filename
		f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/my_blogs_filenames.txt",'r')
		filename_array=f.readlines()
		f.close()
		i=-1
		for var in filename_array:
			i+=1
			if(var==(title_name+"\n")):
				filename_array.remove(var)
				break
		f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/my_blogs_titles.txt",'r')
		filetitle_array=f.readlines()
		title=filetitle_array[i].rstrip('\n')
		form=newblog(request.POST or None,initial={'title':title,'content':string})
		context={
			"form":form,
			"heading":"Now Editing..."
			}
		#delete the existing file
		os.remove(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/myblogs/"+title_name+".txt")
		f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/my_blogs_filenames.txt",'r')
		filename_array=f.readlines()
		f.close()
		i=-1
		for var in filename_array:
			i+=1
			if(var==(title_name+"\n")):
				filename_array.remove(var)
				break
		f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/my_blogs_filenames.txt",'w')
		for var in filename_array:
			f.write(var)
		f.close()
		f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/my_blogs_titles.txt",'r')
		filetitle_array=f.readlines()
		f.close()
		del filetitle_array[i]
		f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/my_blogs_titles.txt",'w')
		for var in filetitle_array:
			f.write(var)
		f.close()
		f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/timestamp.txt",'r')
		filetimestamp_array=f.readlines()
		f.close()
		del(filetimestamp_array[i])
		f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/timestamp.txt",'w')
		for var in filetimestamp_array:
			f.write(var)
		f.close()
		#write a new file
		if form.is_valid():
			filename=form.cleaned_data.get("title")
			data=form.cleaned_data.get("content")
			count=0
			f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/my_blogs_titles.txt")
			
			for line in f:
				if filename==line.rstrip('\n'):
					count+=1
			f.close()
			f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/my_blogs_titles.txt",'a')
			f.write(filename+"\n")
			
			if count>0:	
				f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/myblogs/"+filename+"--"+str(count)+".txt",'w')
				f.write(data)
				f.close()
				now = time.strftime("%c")
				f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/my_blogs_filenames.txt",'a')
				f.write(filename+"--"+str(count)+"\n")
				f.close()
				f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/timestamp.txt",'a')
				f.write(filename+"--"+str(count)+":"+str(now)+"\n")
				f.close()
			else:
				f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/myblogs/"+filename+".txt",'w')
				f.write(data)
				f.close()
				now = time.strftime("%c")
				f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/my_blogs_filenames.txt",'a')
				f.write(filename+"\n")
				f.close()
				f=open(os.path.join(os.path.dirname(settings.BASE_DIR),"users/")+username_unique+"/timestamp.txt",'a')
				f.write(filename+":"+str(now)+"\n")
				f.close()
			context={
			"heading":"Saved!",
			"form":form
			}
			return render(request,"write.html",context)

		return render(request,"write.html",context)

