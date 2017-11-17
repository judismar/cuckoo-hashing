import math
import random
import sys
import time
from ph import DPHScheme
random.seed()

#n = int(sys.argv[1])
#epsilon = float(sys.argv[2])

class BadHashFunction:
	def __init__(self, m):
		self.m = m
	def h(self, x):
		return 0

class CuckooHashingPerfectRehash:
	def __init__(self, n, epsilon):
		self.r = int((1 + epsilon)*math.ceil(math.sqrt(n))) #size of each table
		self.d = int(math.ceil(math.sqrt(n))) #number of tables: function  of n -> ceil(sqrt(n))
		self.T = range(self.d)
		self.h = range(self.d)
		for i in range(self.d):
			hf = BadHashFunction(self.r)
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
		for i in range(self.d): #maxloop is actually ceil(sqrt(n)) in this Cuckoo Hashing scheme
			self.T[i][self.h[i](x)], x = x, self.T[i][self.h[i](x)]
			if not x:
				return
		i = 0 #worst-case simulation: determinism!
		while self.tableFull(i): #what if the ith table is full? From 0 to d-1. The first ones will be full (it will go to 1 when 0 is full! Worst-case!)
			i += 1
		self.perfectRehash(i, x)

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
		t = DPHScheme(aux, self.r)
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
