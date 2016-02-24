from django.shortcuts import render_to_response,render
from django.template import RequestContext
from django.http import HttpResponseRedirect,Http404,HttpResponse,JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from checkmate.main.models import *
from django.contrib.auth.decorators import login_required
from checkmate.main.forms import *
from django.db import IntegrityError
import json
from django.core import serializers

def login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	if request.POST:
		form=LoginForm(request.POST)
		if form.is_valid():	
			data=form.cleaned_data
			username = data['username']
			password = data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					auth.login(request, user)
					return HttpResponseRedirect('/')
					
				else:
					state = "Your account is not active, please contact the site admin."
					return render_to_response('login.html', {'form':form,'state':state},context_instance=RequestContext(request))
					
			else:
				state = "Your username and/or password were incorrect."
				return render_to_response('login.html', {'form':form,'state':state},context_instance=RequestContext(request))
		else:
			return render_to_response('login.html', {'form':form},context_instance=RequestContext(request))
			
	else:
		form=LoginForm()
		return render_to_response('login.html', {'form':form},context_instance=RequestContext(request))

@login_required
def question(request):
	#return HttpResponse("asdf")
	if request.method=="POST" :
		#if is_instance(request.POST.get('no'),int)
		if str(request.POST.get('no')).isdigit():
			no = int(request.POST.get('no'))
		else:
			print "1"
			raise Http404
	else:
		print "2"
		raise Http404
	
		
	#if request.method== "GET":
	#	no=int(request.GET.get['no'])
	u=request.user
	try:
		up=UserProfile.objects.get(user=u)
	except DoesNotExist:
		print "3"
		raise Http404
	try:
		ques=Question.objects.get(no=no)
	except:
		print "4"
		raise Http404
	resp={}
	resp['status']=1
	if request.method=="POST" and 'answer' in request.POST:
		data=request.POST
		
		#if len(up.qa)>1:
		if up.qa is not None:
			qas=up.qa.split(',')
		
		if up.fa is not None:
			fas=up.fa.split(',')	
		#print qas	#.filter
		for i in qas:
			if str(no)==str(i):
				resp['status']=-1
				break
		#print resp['status']
		
		if 	resp['status']==1 or resp['status']==0:
			flag=False
			for i in fas:
				if str(no)==str(i):
					up.qa+=str(no)
					up.qa+=","
					flag=True
			if flag==False:
				up.fa+=str(no)
				up.fa+=","				
			up.save()
			
			if data['answer'].lower()==ques.answer and resp['status']==1:
				if ques.difficulty==1:
					up.score+=50
				elif ques.difficulty==2:
					up.score+=100
				elif ques.difficulty==3:
					up.score+=150
			elif data['answer'].lower()!=ques.answer:
				resp['status']=0			#deduct points for wrong answer
		up.save()
	else:
		resp['content']=ques.content
		resp['qno']=ques.no
		resp['diff']=ques.difficulty
	resp['score']=up.score	
	resp['quesatt']=up.qa
	resp['quesfirst']=up.fa
	
	data = json.dumps(resp,indent=4)
	#print data			#do simplejson if reqd
	return HttpResponse(data,content_type='json')
			
@login_required
def main(request):
	u=request.user
	try:
		up=UserProfile.objects.get(user=u)
	except:
		raise Http404
	return render_to_response('index.html', {'up':up},context_instance=RequestContext(request))

def rulebook(request):
	 return render_to_response('rulebook.html',context_instance=RequestContext(request))

def leaderboard(request):
	try: 
		usrs=UserProfile.objects.order_by('score')[:max(25,UserProfile.objects.all().count())]
	except:
		raise Http404
	resp={}
	for i in range(len(usrs)):
		resp[i]['teamname']=usrs[i].teamname
		resp[i]['score']=usrs[i].score

	data = json.dumps(resp,indent=4)								#do simplejson if reqd
	return HttpResponse(data,content_type='json')

@login_required
def arena(request):
	resp={}
	try:
		u=request.user
		up=UserProfile.objects.get(user=u)
		resp['inventory']=up.pipe_inventory
		resp['score']=up.score
	except:
		raise Http404
	data = json.dumps(resp,indent=4)
	#print data			#do simplejson if reqd
	return HttpResponse(data,content_type='json')
	
@login_required
def buy(request):
	
	#if 'pipe' in request.POST
	pipe=int(str(request.POST.get('pipe')))
		
	resp={}
	#print pipe
	try:
		u=request.user
		up=UserProfile.objects.get(user=u)
	except :
		raise Http404
	inv=up.pipe_inventory.split(',')
	
	if up.score>=100:
		resp['status']=1
		up.score-=100
		inv[pipe]=str(int(inv[pipe])+1)
		
	up.pipe_inventory=','.join(inv)
	up.save()
	resp['inventory']=up.pipe_inventory
	resp['score']=up.score
	data = json.dumps(resp,indent=4)
	print data			#do simplejson if reqd
	return HttpResponse(data,content_type='json')			
	
	
@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")

def register(request):
	m=''
	if request.user.is_authenticated():
		return HttpResponseRedirect('/main/')
	if request.POST:
		form=RegistrationForm(request.POST)
		#a=form.cleaned_data
		print form
		if form.is_valid():
			data=form.cleaned_data
			print data
			u=User()
			up=UserProfile()
			u.username=data['username']
			u.set_password(data['password'])
			try:
				u.save()
			except IntegrityError:
				m='Username already exists'
				return render_to_response('register.html',{'message':m},context_instance=RequestContext(request))
			up.teamname=data['username']
			up.name1=data['name1']
			up.name2=data['name2']
			up.phone1=data['phone1']
			up.phone2=data['phone2']
			up.email1=data['email1']
			up.email2=data['email2']
			up.user=u
			up.save()
			return HttpResponseRedirect('/login/')
		else:
			return render_to_response('register.html',{'message':m},context_instance=RequestContext(request))
	else:
		form=RegistrationForm()
		return render_to_response('register.html',{'form':form},context_instance=RequestContext(request))

@login_required
def validate(request):
	
	r={}
	try:
		u=request.user
		up=UserProfile.objects.get(user=u)
		snap=request.POST.get('snapshot')
	except:
		raise Http404
	#s= [1,0,0,0,0,4,5,1,0,0,0,0,6,0,0,0,0,4,1,0,0,0,0,4,1]
	ct=0
	for i in range(5):
		for j in range(5):
			s[i][j]=snap[ct]
			ct+=1
	x=check_success(s)
	inv=up.pipe_inventory.split(',')
	
	if x:
		for i in s:
			if i>0:
				inv[i-1]-=1
			if inv[i-1]<0:
				r['status']=-1
				inv = up.pipe_inventory.split(',')
	else:		
		r['status']=0
	if r['status']==1:
		up.score+=x*200			#document this
		if x>18:
			up.score +=1000
		elif x>12:
			up.score +=500
	r['score']=up.score
	r['inventory']=up.pipe_inventory
	
	data = json.dumps(r,indent=4)
	#print data			#do simplejson if reqd
	return HttpResponse(data,content_type='json')			


def check_success(s):
	#s= [[1,0,0,0,0],[4,5,1,0,0],[0,0,6,0,0],[0,0,4,1,0],[0,0,0,4,1]]
	i,j,ent,desti,destj,destent=0,0,2,5,4,3
	pipe_map ={"p0": 0,"p1": 14,"p2": 35,"p3": 6,"p4": 15,"p5": 10,"p6": 21}

	#	ent is the entry point for the pipe
	#	the numbers associated with box is
	#	2 - left; 3 - top; 5 - right; 7 - bottom
	#	prime numbers are used so that we can define pipes with product of this numbers
	
	success = False
	count,ext,num=0,0,0
	while (i>=0 and i<len(s) and j>=0 and j<len(s[0])):
		num = int(pipe_map["p"+str(s[i][j])]);
		s[i][j] = 0
		if (num==0 or num%ent != 0):
			break
		else:
			count+=1
			ext = num/ent
			if (ext==7):
				i+=1
				ent=3
			elif (ext==5):
				j+=1
				ent=2
			elif (ext==3):
				i-=1
				ent=7
			elif (ext==2):
				j-=1
				ent=5
			elif (ext*ent==210):
				if (ext%21==0):
					if ent==2:
						i+=1 
					else:
						i-=1
				else:
					if ent==2:
						j+=1 
					else:
						j-=1
			else:
				return 0
		if (i==desti and j==destj and ent==destent):
			success = True
			break
	if success:
		return count
	else:
		return 0
