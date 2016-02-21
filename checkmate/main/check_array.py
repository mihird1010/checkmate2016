import csv
import sys				#define the 'array' to store the number of pipes user has
import 

@login_required
def validate(request):		#delete pipe from user pipe string
	up = request.user
	u = UserProfile.objects.get(user = up)
	allow = 0
	if (u.active_x == request.x) && (u.active_y == request.y):
		with open('activepos.csv', 'rb') as file:
		reader = csv.reader(file)
		for row in reader:
			if(row[0]== u.activeside and row[1]==request.pipe):
				allow = 1
				u.activeside = row[2]
				addx = int(row[3])
				addy = int(row[4])
				u.active_x=u.active_x+str( int(u.active_x[-1])+addx)
				u.active_x=u.active_x+str( int(u.active_y[-1])+addy)
		u.score += 150
	return allow


@login_required
def delete(request):		# update pipes 		#deduct score
	up = request.user
	u = UserProfile.objects.get(user = up)
	active_x = u.active_x
	active_y = u.active_y
	x = request.x
	y = request.y
	allow = 0
	for num1 in re.finditer(x, active_x):
		for num2 in re.finditer(y, active_y):
			if num2.start() == num1.start():
				pos = num1.start()
				if pos != (len(active_y)-1):
					u.active_x = active_x[:(pos+1)]
					u.active_y = active_y[:(pos+1)]
					allow = 1
	
	if allow == 1:
		# ?? #
	else:

