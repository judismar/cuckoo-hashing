import math
import random
import sys
import time
from uhprime import HashFunction
from phgraphs import HashFunctionGenerator
random.seed()

#n = int(sys.argv[1])
#epsilon = float(sys.argv[2])
#constloops = int(sys.argv[3])

class CuckooHashingPerfectRehashgraphs:
	def __init__(self, n, epsilon):
		self.r = int((1 + epsilon)*math.ceil(math.sqrt(n))) #size of each table
		self.d = int(math.ceil(math.sqrt(n))) #number of tables: function  of n -> ceil(sqrt(n))
		self.T = range(self.d)
		self.h = range(self.d)
		for i in range(self.d):
			hf = HashFunction(self.r, 144013)
			self.h[i] = hf.h
			self.T[i] = range(self.r)
			for k in range(self.r): #initialize all with None
				self.T[i][k] = None
		
	def busca(self, x):
		for i in range(self.d):
			if self.T[i][self.h[i](x)] == x:
				return True
		return False

	def insere(self, x):
		if self.busca(x):
			return
		k = 0
		for i in range(self.d): #maxloop is actually ceil(sqrt(n)) in this Cuckoo Hashing scheme
			k = random.randint(0, self.d-1) #all moves are made at random tables
			self.T[k][self.h[k](x)], x = x, self.T[k][self.h[k](x)]
			if not x:
				return
		while self.tableFull(k): #what if the k table is full? (can be easily solved with a list of available tables)
			k = random.randint(0, self.d-1)
		self.perfectRehash(k, x)

	def perfectRehash(self, tableIndex, key):
		aux = [] 
		numNones = -1
		for i in range(self.r):
			if self.T[tableIndex][i] != None:
				aux.append(self.T[tableIndex][i])
				self.T[tableIndex][i] = None
			else:
				numNones += 1
		aux.append(key)
		t = HashFunctionGenerator(2, 144013)
		t.mapping(aux, numNones)
		for key in aux:
			self.T[tableIndex][t.h(key)] = key
		self.h[tableIndex] = t.h

	def tableFull(self, tableIndex): #is table full? if yes, returns true
		for i in range(self.r):
			if not self.T[tableIndex][i]:
				return False
		return True

	def printf(self):
		for i in range(self.d):
			print i, self.T[i]
