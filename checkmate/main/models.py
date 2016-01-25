from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
	no=models.PositiveSmallIntegerField()
	difficulty=models.PositiveSmallIntegerField()
	content=models.CharField(max_length=5000)
	answer=models.CharField(max_length=50)
	def __unicode__(self):
		return str(self.content)

class UserProfile(models.Model):
	user=models.ForeignKey(User,unique=True) #extending user model
	score=models.IntegerField(default=0)
	pipes=models.IntegerField(default=1) #Let's start with something like a horizontal pipe
	name1=models.CharField(max_length=200)
	name2=models.CharField(max_length=200,blank=True,null=True)
	phone1=models.BigIntegerField(null=True)
	phone2=models.BigIntegerField(blank=True,null=True)
	email1=models.EmailField()
	email2=models.EmailField(blank=True,null=True)
	qs=models.ManyToManyField('Question',related_name='qs')#storing list of questions attempted
	def __unicode__(self):
		return self.user.username
		

