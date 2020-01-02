#!/usr/bin/env python
# encoding: utf8
# Artificial Intelligence, UBI 2019-20
# Modified by: Students names and numbers

import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry
import networkx as nx
import matplotlib.pyplot as plt
import math

x_ant = 0
y_ant = 0
obj_ant = ''
init_time = 0
distancia_percorrida = 0
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
list_suits = []
visited = []
list_roomsComputer = []

# Dicionário contendo todos os espaços e conteúdos dentro deles
spaces = {"1": [],"2": [], "3": [], "4": [], "5": [], "6": [], "7": [], "8": [], "9": [], "10": [], "11": [], "12": [], "13": [], "14": []}
# Origem do robot
ogX = 0
ogY = 0
x = 0
y = 0

div_atual = 0
div_ant = 0
node_ant = 0
node_atual = 0
ver = False
grafo = nx.Graph()

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
	if (x >= (ogX + 11.1)) and (x <= (ogX + 13.7)) and (y >= (ogY + 0.1)) and (y <= (ogY + 6.7)):
		return 4
	# Quarto 5
	if (x >= (ogX + (-0.5))) and (x <= (ogX + 2.6)) and (y >= (ogY + 0.7)) and (y <= (ogY + 4.5)):
		return 5
	if (x >= (ogX + (-0.5))) and (x <= (ogX + 3.2)) and (y >= (ogY + 4.5)) and (y <= (ogY + 8.8)):
		return 6
	if (x >= (ogX + (-0.5))) and (x <= (ogX + 4.4)) and (y >= (ogY + 8.8)) and (y <= (ogY + 12.6)):
		return 7
	if (x >= (ogX + (4.4))) and (x <= (ogX + 8.8)) and (y >= (ogY + 8.8)) and (y <= (ogY + 12.6)):
		return 8
	if (x >= (ogX + (9.3))) and (x <= (ogX + 13.7)) and (y >= (ogY + 8.8)) and (y <= (ogY + 12.6)):
		return 9
	if (x >= (ogX + (14.2))) and (x <= (ogX + 18.5)) and (y >= (ogY + 8.8)) and (y <= (ogY + 12.6)):
		return 10
	if (x >= (ogX + (13.7))) and (x <= (ogX + 18.5)) and (y >= (ogY + 3.8)) and (y <= (ogY + 6.8)):
		return 11
	if (x >= (ogX + (13.7))) and (x <= (ogX + 18.5)) and (y >= (ogY + 0.7)) and (y <= (ogY + 3.3)):
		return 12	
	if(x >= (ogX + 5.4)) and (x <= (ogX + 7.9)) and (y >= (ogY + 0.7)) and (y <= (ogY + 6.8)):
		return 13
	if(x >= (ogX + 8.4)) and (x <= (ogX + 11.1)) and (y >= (ogY + 0.7)) and (y <= (ogY + 6.8)):
		return 14

# Preenche o dicionário 
def contents(objectD, space_number):
	global spaces,grafo
	for x in spaces.keys():
		if x == str(space_number):
			spaces[x].append(objectD)
			attrs = {space_number:{'objects':spaces.get(str(space_number), 'none'),'type':getTypeRoom(space_number)}}
			nx.set_node_attributes(grafo, attrs)
			if grafo.has_node(space_number):
				print 'conteudo'
				print grafo.nodes[space_number]['objects']
				print grafo.nodes[space_number]['type']
			

# Responde à 1
def q1():
	global spaces
	rooms_n_visited = 0
	count = 0
	occupied = 0
	# Vai iterar só nos quartos
	for x in range(5, 15):
		if len(spaces[str(x)]) != 0:
			count += 1
			for y in spaces[str(x)]:
				if "person_" in y:
					occupied += 1
					break
		else:
			rooms_n_visited += 1 	
	print "%d rooms not occupied of %d visited" %((count - occupied),(10 - rooms_n_visited))

# Responde à 3
def q3():
	global spaces
	total_persons = 0
	rooms_persons = 0
	corridors_persons = 0
	for x in range(1, 15):
		for y in spaces[str(x)]:
			if "person_" in y:
				total_persons += 1
				if x < 5:
					corridors_persons += 1
				else:
					rooms_persons += 1 		
	if corridors_persons > rooms_persons:
		print "In Corridors with: %.2f percentage" %(float(corridors_persons)/total_persons*100)
	elif rooms_persons > corridors_persons:
		print "In Rooms with: %.2f percentage" %(float(rooms_persons)/total_persons*100)
	elif rooms_persons == corridors_persons and rooms_persons != 0:
		print "It's equal, 50/50 probability."
	else:
		print "I don't have enough information"


def suits(local):
	global div_atual,div_ant, ver
	ver = False
	if local != div_atual:
		div_ant = div_atual
		div_atual = local
		print div_ant
		print div_atual
	if div_atual in range(5,15) and div_ant in range(5,15):
		suit = (div_ant,div_atual)
		if len(list_suits) == 0:
			list_suits.append(suit)
		else:
			for suits in list_suits:
				if suit not in list_suits and (suit[0] != suits[0] or suit[0] != suits[1]) and suit[0] == suits[1]:
					ver = False	
				else:
					if suit not in list_suits and (suit[0] == suits[0] or suit[0] == suits[1]) and suit[0] == suits[1]:
						ver = False
					else:
						if suit not in list_suits:
							ver = True

			if ver:
				list_suits.append(suit)
						


#Função conta suits
def contsuits():
	return len(list_suits)

#Função construir grafo
def construirGrafo(local):
	global node_ant,node_atual, grafo, visited
	if local != node_atual:
		node_ant = node_atual
		node_atual = local
		if (node_atual,node_ant) not in grafo.edges() or (node_ant, node_atual) not in grafo.edges() and node_atual not in grado.nodes():
			grafo.add_node(node_atual)
			grafo.add_node(node_ant)
			attrs = {node_atual:{'objects':spaces.get(str(node_atual), 'none'),'type':getTypeRoom(node_atual)}}
			nx.set_node_attributes(grafo, attrs)
			grafo.add_edge(node_atual,node_ant,weight = 1)
		visited.append(node_atual)
		visited.append(node_ant)

def mostrargrafo():
	print nx.shortest_path(grafo,div_atual,0,1,method='dijkstra')
	


def getTypeRoom(key):
	global spaces
	beds = 0
	table = 0
	chair = 0
	if not spaces:
		return 'I dont have enough information to answer that question'
	elif key == 0:
		return 'Elevator'
	elif key in range(1,4):
		return 'Hall' + str(key)
	else:
		
		for item in spaces.get(str(key), 'none'):
			if 'bed_' in item:
				print 'Entrou'
				beds += 1
			elif 'table_' in item:
				table += 1
			elif 'chair_' in item:
				chair += 1
		
		if beds > 1:
			return 'double_room'
		elif beds == 1:
			return 'single_room'
		elif table > 1 and chair >= 1:
			return 'meeting_room'
			
		else:
			for tuples in list_suits:
				if key in tuples:
					return 'suit_room'
					break;				
			return 'generic_room'
def q4():
	global spaces
	list_rooms = []
	for i in range(1,15):
		list_rooms.append(0)
	maior = 0
	room = 0
	if not spaces:
		print 'I dont have enough information to answer that question'
	else:	
		for x in range(1,15):
			for y in spaces[str(x)]:
				if "computer_" in y:
					list_rooms[x] += 1
		if not list_rooms:
			print 'Dont exist any computer in the rooms that was visited'
		else:
			for index, val in enumerate(list_rooms):
				if val > maior:
					room = index
					if getTypeRoom(room) not in list_roomsComputer:
						list_roomsComputer.append(getTypeRoom(room))
		if room == 0:
			print 'I dont have enough information to answer that question'
		else:
	 		print 'If you want to find a computer go to room of type '
			for rooms in list_roomsComputer:
				print rooms  
def q5():
	global x,y
	list_rooms = []
	menor = 10000000000
	nearest_room = 0
	peso = 0
	div_atual = localization(x,y)
	
	if nx.is_empty(grafo):
		print 'I dont visited enough rooms or i dont visited a single room yet'
	else:
		for x in range(1,15):
			if grafo.has_node(x):
				if 'single_room' == grafo.nodes[x]['type']:
					list_rooms.append(x)

		if not list_rooms:
			print 'I dont visited single rooms yet'
		else:	
			print list_rooms
			print div_atual
			for room in list_rooms:
				peso = len(nx.shortest_path(grafo,div_atual,room,1,method='dijkstra'))
				if peso < menor:
				 nearest_room = room
			if nearest_room == 0:
				print 'Dont exist single rooms'
			else:
				print 'The nearest single room is room number ' + str(nearest_room)
		
def q7():
	global init_time
	global list_book
	global spaces
	time = rospy.get_rostime().secs - init_time
	count = 0
	# Vai iterar só nos quartos
	for x in range(5, 15):
		if len(spaces[str(x)]) != 0:
			count += 1
			 		
	if len(list_book) == 0:
		print 'I dont have enought information...'
	else:
		print "I estimate to find %.2f books in the next 2 minutes" %((1-count/10)*(120*len(list_book))/time)

def q8():
	totalTables = number_table
	rooms = 0
	propB = 0.0
	propA = 0.0
	propAsabendoB = 0.0

	for x in range(1,15):
		for y in spaces[str(x)]:
			if 'book_' not in y and 'chair_' in y:
				print rooms
				rooms += 1
	propB = float(rooms) / 15
	if totalTables == 0:
		propA = 0
	else:
		propA = 1 / float(totalTables)
	if propB == 0:
		propAsabedoB = 0
	else:
		propAsabendoB = (propA*((propB*propA)/propA))/propB

	print 'The probability of finding a table in a room without books but that has at least one chair is: '  + str(propAsabendoB*100) + '%'
					
def q9():
	global distancia_percorrida
	print 'Distance: %.2f' %(distancia_percorrida)
# ---------------------------------------------------------------
# odometry callback
def callback(data):
	global x_ant, y_ant, ogX, ogY, x, y, distancia_percorrida
	x = data.pose.pose.position.x+ogX
	y = data.pose.pose.position.y+ogY	
	# show coordinates only when they change
	if x != x_ant or y != y_ant:
		print " x=%.1f y=%.1f" % (x,y)
		localization(x,y)
		suits(localization(x,y))
		construirGrafo(localization(x,y))
		
	#Calcular diferenca da distancia entre os pontos
	#e adicionar para obter a distância percorrida
	distancia_percorrida += math.sqrt((x-x_ant)*(x-x_ant)+(y-y_ant)*(y-y_ant))
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
	global spaces 
	if data.data is "1":
		q1()
	if data.data is "2":
		print "Q%s.: %s" %(data.data, data.data)
		print "I find until now %d" %contsuits()
	if data.data is "3":
		q3()
	if data.data is "4":
		print "Q%s.: %s" %(data.data, data.data)
		q4()
				
	if data.data is "5":
		print "Q%s.: %s" %(data.data, data.data)
		q5()
	if data.data is "6":
		print "Q%s.: %s" %(data.data, data.data)
		mostrargrafo()
	if data.data is "7":
		q7()
	if data.data is "8":
		print "Q%s.: %s" %(data.data, data.data)
		q8()
	if data.data is "9":
		q9()
# ---------------------------------------------------------------
def agent():
	global init_time
	rospy.init_node('agent')
	init_time = rospy.get_rostime().secs
	rospy.Subscriber("questions_keyboard", String, callback2)
	rospy.Subscriber("object_recognition", String, callback1)
	rospy.Subscriber("odom", Odometry, callback)

	rospy.spin()

# ---------------------------------------------------------------
if __name__ == '__main__':
	agent()
