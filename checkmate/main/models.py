from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
	no=models.PositiveSmallIntegerField()
	difficulty=models.PositiveSmallIntegerField(default=1)
	content=models.CharField(max_length=5000)
	answer=models.CharField(max_length=50)
	def __unicode__(self):
		return str(self.content)
#class PipeList(models.Model): #stores pipes of each type the user has
#	type2=models.PositiveSmallIntegerField(default=0)
#	type3=models.PositiveSmallIntegerField(default=0)
#	type4=models.PositiveSmallIntegerField(default=0)
#	type5=models.PositiveSmallIntegerField(default=0)
#	type6=models.PositiveSmallIntegerField(default=0)
#	def __unicode__(self): 
#		return (str(self.type1)+"|"+str(self.type2)+"|"+str(self.type3)+"|"+str(self.type4)+"|"+str(self.type5)+"|"+str(self.type6))

class UserProfile(models.Model):
	user=models.OneToOneField(User) #extending user model
	score=models.IntegerField(default=0)
	pipe_inventory=models.CharField(default='0,0,0,0,0,0',max_length=100)
	pipestring=models.CharField(max_length=30,blank=True)
	active_side=models.CharField(default="R",max_length=30)
	active_x=models.CharField(default="1",max_length=30)
	active_y=models.CharField(default="0",max_length=30)
	teamname=models.CharField(max_length=200)
	name1=models.CharField(max_length=200)
	name2=models.CharField(max_length=200,blank=True,null=True)
	phone1=models.BigIntegerField(null=True)
	phone2=models.BigIntegerField(blank=True,null=True)
	email1=models.EmailField()
	email2=models.EmailField(blank=True,null=True)
	qa=models.CharField(max_length=100,blank=True,null=True,default="0") #storing list of questions attempted
	#idno1=models.CharField(max_length=20)
	#idno1=models.CharField(max_length=20,blank=True)
	
	def __unicode__(self):
		return self.user.username
		

