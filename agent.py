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

# Origem do robot
ogX = 0
ogY = 0

# ---------------------------------------------------------------
# ASNEIRAS
# Verifica se o objeto já foi reconhecido anteriormente

def lists(objectD, lista):
	if objectD in lista:
		print "Repetido"
		return -1
	else:
		lista.append(objectD)
		print lista
		return 1

# Ver se o agente está em qual corredor

def corridors(x, y):
	global ogX, ogY
	# Corredor 1
	if (x >= (ogX + 0)) and (x <= (ogX + 18.5)) and (y >= (ogY + (-1.5))) and (y <= (ogY + 0.1)):
		print "Corredor 1"
	if (x >= (ogX + 3.2)) and (x <= (ogX + 5.4)) and (y >= (ogY + 0.1)) and (y <= (ogY + 6.7)):
		print "Corredor 2"
	if (x >= (ogX + 2.8)) and (x <= (ogX + 18.5)) and (y >= (ogY + 6.7)) and (y <= (ogY + 8.8)):
		print "Corredor 3"
	if (x >= (ogX + 11.2)) and (x <= (ogX + 13.6)) and (y >= (ogY + 0.1)) and (y <= (ogY + 6.7)):
		print "Corredor 4"


# Ver se o agente está em algum quarto
def rooms(x, y):
	global ogX, ogY	
	# Quarto 5
	if (x >= (ogX + (-0.5))) and (x <= (ogX + 2.6)) and (y >= (ogY + 0.7)) and (y <= (ogY + 3.8)):
		print "Quarto 5"
	if (x >= (ogX + (-0.5))) and (x <= (ogX + 2.6)) and (y >= (ogY + 4.5)) and (y <= (ogY + 8.8)):
		print "Quarto 6"
	if (x >= (ogX + (-0.5))) and (x <= (ogX + 4.4)) and (y >= (ogY + 8.8)) and (y <= (ogY + 12.6)):
		print "Quarto 7"
	if (x >= (ogX + (4.4))) and (x <= (ogX + 8.8)) and (y >= (ogY + 9.1)) and (y <= (ogY + 12.6)):
		print "Quarto 8"
	if (x >= (ogX + (9.3))) and (x <= (ogX + 13.7)) and (y >= (ogY + 9.1)) and (y <= (ogY + 12.6)):
		print "Quarto 9"
	if (x >= (ogX + (14.2))) and (x <= (ogX + 18.5)) and (y >= (ogY + 9.1)) and (y <= (ogY + 12.6)):
		print "Quarto 10"
	if (x >= (ogX + (13.9))) and (x <= (ogX + 18.5)) and (y >= (ogY + 3.8)) and (y <= (ogY + 6.8)):
		print "Quarto 11"
	if (x >= (ogX + (13.9))) and (x <= (ogX + 18.5)) and (y >= (ogY + 0.7)) and (y <= (ogY + 3.3)):
		print "Quarto 12"	
	if(x >= (ogX + 6.1)) and (x <= (ogX + 7.9)) and (y >= (ogY + 0.7)) and (y <= (ogY + 6.8)):
		print "Quarto 13"
	if(x >= (ogX + 8.4)) and (x <= (ogX + 10.6)) and (y >= (ogY + 0.7)) and (y <= (ogY + 6.8)):
		print "Quarto 14"

		

# ---------------------------------------------------------------
# odometry callback
def callback(data):
	global x_ant, y_ant, ogX, ogY
	x = data.pose.pose.position.x+ogX
	y = data.pose.pose.position.y+ogY	
	# show coordinates only when they change
	if x != x_ant or y != y_ant:
		print " x=%.1f y=%.1f" % (x,y)
		rooms(x, y)
		corridors(x, y)
	x_ant = x
	y_ant = y

# ---------------------------------------------------------------
# object_recognition callback
def callback1(data):
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
			if "chair_" in objectD:
				if lists(objectD, list_chair) == 1:
					number_chair += 1		
			if "bed_" in objectD:
				if lists(objectD, list_bed) == 1:
					number_bed += 1	
			if "book_" in objectD:
				if lists(objectD, list_book) == 1:
					number_book += 1
			if "computer_" in objectD:
				if lists(objectD, list_computer) == 1:
					number_computer += 1
			if "table_" in objectD:
				if lists(objectD, list_table) == 1:
					number_table += 1
			if "mistery_" in objectD:
				if lists(objectD, list_mistery) == 1:
					number_mistery += 1
	obj_ant = data.data
		
# ---------------------------------------------------------------
# questions_keyboard callback
def callback2(data):
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
		print "Q%s.: %s" %(data.data, data.data)
	if data.data is "10":
		print "Q%s.: %s" %(data.data, data.data)
	if data.data is "11":
		print "Q%s.: %s" %(data.data, data.data)


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