#!/usr/bin/env python
# encoding: utf8
# Artificial Intelligence, UBI 2019-20
# Modified by: Students names and numbers

import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry

x_ant = 0
y_ant = 0
obj_ant = ''
# Contador dos objetos
number_bed = 0
number_book = 0
number_chair = 0
number_computer = 0
number_person = 0
number_table = 0 
number_mistery = 0
number_door = 0

# Lista dos objetos já conhecidos
list_bed = []
list_book = []
list_chair = []
list_computer = []
list_person = []
list_table = []
list_mistery = []
list_door = []

# Lista dos espaços
space_1 = [1]
space_2 = [2]
space_3 = [3]
space_4 = [4]
space_5 = [5]
space_6 = [6]
space_7 = [7]
space_8 = [8]
space_9 = [9]
space_10 = [10]
space_11 = [11]
space_12 = [12]
space_13 = [13]
space_14 = [14]
space_15 = [15]

# Origem do robot
ogX = 0
ogY = 0
x = 0
y = 0

# ---------------------------------------------------------------
# ASNEIRAS
# Lista o objeto que encontrou (não repetido) no devido local 
def lists(objectD, lista):
	if objectD in lista:
		return -1
	else:
		lista.append(objectD)
		print lista
		return 1

# Ver a localização do robot
def localization(x, y):
	global ogX, ogY
	# Corredor 1
	if (x >= (ogX + 0)) and (x <= (ogX + 18.5)) and (y >= (ogY + (-1.5))) and (y <= (ogY + 0.1)):
		return 1
	if (x >= (ogX + 3.2)) and (x <= (ogX + 5.4)) and (y >= (ogY + 0.1)) and (y <= (ogY + 6.7)):
		return 2
	if (x >= (ogX + 2.8)) and (x <= (ogX + 18.5)) and (y >= (ogY + 6.7)) and (y <= (ogY + 8.8)):
		return 3
	if (x >= (ogX + 11.2)) and (x <= (ogX + 13.6)) and (y >= (ogY + 0.1)) and (y <= (ogY + 6.7)):
		return 4
	# Quarto 5
	if (x >= (ogX + (-0.5))) and (x <= (ogX + 2.6)) and (y >= (ogY + 0.7)) and (y <= (ogY + 3.8)):
		return 5
	if (x >= (ogX + (-0.5))) and (x <= (ogX + 2.6)) and (y >= (ogY + 4.5)) and (y <= (ogY + 8.8)):
		return 6
	if (x >= (ogX + (-0.5))) and (x <= (ogX + 4.4)) and (y >= (ogY + 8.8)) and (y <= (ogY + 12.6)):
		return 7
	if (x >= (ogX + (4.4))) and (x <= (ogX + 8.8)) and (y >= (ogY + 9.1)) and (y <= (ogY + 12.6)):
		return 8
	if (x >= (ogX + (9.3))) and (x <= (ogX + 13.7)) and (y >= (ogY + 9.1)) and (y <= (ogY + 12.6)):
		return 9
	if (x >= (ogX + (14.2))) and (x <= (ogX + 18.5)) and (y >= (ogY + 9.1)) and (y <= (ogY + 12.6)):
		return 10
	if (x >= (ogX + (13.9))) and (x <= (ogX + 18.5)) and (y >= (ogY + 3.8)) and (y <= (ogY + 6.8)):
		return 11
	if (x >= (ogX + (13.9))) and (x <= (ogX + 18.5)) and (y >= (ogY + 0.7)) and (y <= (ogY + 3.3)):
		return 12	
	if(x >= (ogX + 6.1)) and (x <= (ogX + 7.9)) and (y >= (ogY + 0.7)) and (y <= (ogY + 6.8)):
		return 13
	if(x >= (ogX + 8.4)) and (x <= (ogX + 10.6)) and (y >= (ogY + 0.7)) and (y <= (ogY + 6.8)):
		return 14

# Adiciona conteúdo NOVO no respetivo espaço
def contents(objectD, space_number):
	global space_1,space_2, space_3, space_4, space_5, space_6, space_7, space_8, space_9, space_10, space_11, space_12, space_13, space_14, space_15
	if space_number in space_1:
		space_1.add(objectD)
	if space_number in space_2:
		space_2.append(objectD)
	if space_number in space_3:
		space_3.append(objectD)
	if space_number in space_4:
		space_4.append(objectD)
	if space_number in space_5:
		space_5.append(objectD)
	if space_number in space_5:
		space_6.append(objectD)
	if space_number in space_7:
		space_7.append(objectD)
	if space_number in space_8:
		space_8.append(objectD)
	if space_number in space_9:
		space_.append(objectD)	
	if space_number in space_10:
		space_10.append(objectD)
	if space_number in space_11:
		space_11.append(objectD)
	if space_number in space_12:
		space_12.append(objectD)
	if space_number in space_13:
		space_13.append(objectD)
	if space_number in space_14:
		space_14.append(objectD)
	if space_number in space_15:
		space_15.append(objectD)
# ---------------------------------------------------------------
# odometry callback
def callback(data):
	global x_ant, y_ant, ogX, ogY, x, y
	x = data.pose.pose.position.x+ogX
	y = data.pose.pose.position.y+ogY	
	# show coordinates only when they change
	if x != x_ant or y != y_ant:
		print " x=%.1f y=%.1f" % (x,y)
		localization(x,y)
	x_ant = x
	y_ant = y

# ---------------------------------------------------------------
# object_recognition callback
def callback1(data):
	global x, y
	global obj_ant
	global number_person, number_chair, number_bed, number_book, number_computer, number_table, number_mistery
	global list_person, list_chair, list_bed, list_book, list_computer, list_table, list_mistery
	obj = data.data
	objects = []	# Quando deteta mais de 1 objeto
	if obj != obj_ant and data.data != "":
		if "," in obj:	# Detetou mais de 1 objeto
			obj = obj.replace(",", " ")
			objects = obj.split()
		else:
			objects.append(obj)	
		print objects
		# Motor de inferência, que incrementa o contador dos objetos
		for objectD in objects:
			if "person_" in objectD:
				if lists(objectD, list_person) == 1:			
					number_person += 1
					contents(objectD, localization(x, y))
			if "chair_" in objectD:
				if lists(objectD, list_chair) == 1:
					number_chair += 1
					contents(objectD, localization(x, y))		
			if "bed_" in objectD:
				if lists(objectD, list_bed) == 1:
					number_bed += 1
					contents(objectD, localization(x, y))	
			if "book_" in objectD:
				if lists(objectD, list_book) == 1:
					number_book += 1
					contents(objectD, localization(x, y))
			if "computer_" in objectD:
				if lists(objectD, list_computer) == 1:
					number_computer += 1
					contents(objectD, localization(x, y))
			if "table_" in objectD:
				if lists(objectD, list_table) == 1:
					number_table += 1
					contents(objectD, localization(x, y))
			if "mistery_" in objectD:
				if lists(objectD, list_mistery) == 1:
					number_mistery += 1
					contents(objectD, localization(x, y))
	obj_ant = data.data
		
# ---------------------------------------------------------------
# questions_keyboard callback
def callback2(data):
	global space_10, space_11, space_2
	if data.data is "1":
		print "Q%s.: %s" %(data.data, data.data)
	if data.data is "2":
		print "Q%s.: %s" %(data.data, data.data)
	if data.data is "3":
		print "Q%s.: %s" %(data.data, data.data)
	if data.data is "4":
		print "Q%s.: %s" %(data.data, data.data)		
	if data.data is "5":
		print "Q%s.: %s" %(data.data, data.data)
	if data.data is "6":
		print "Q%s.: %s" %(data.data, data.data)
	if data.data is "7":
		print "Q%s.: %s" %(data.data, data.data)
	if data.data is "8":
		print "Q%s.: %s" %(data.data, data.data)
	if data.data is "9":
		print "O conteúdo de todos os espaços"
		print space_1		
		print space_2
		print space_3
		print space_4
		print space_5
		print space_6
		print space_7
		print space_8
		print space_9
		print space_10
		print space_11
		print space_12
		print space_13
		print space_14


# ---------------------------------------------------------------
def agent():
	rospy.init_node('agent')

	rospy.Subscriber("questions_keyboard", String, callback2)
	rospy.Subscriber("object_recognition", String, callback1)
	rospy.Subscriber("odom", Odometry, callback)

	rospy.spin()

# ---------------------------------------------------------------
if __name__ == '__main__':
	agent()
