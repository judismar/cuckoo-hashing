import math
import time
import random
import sys
from uhprime import HashFunction

#n = int(sys.argv[1])
#epsilon = float(sys.argv[2])
#maxloop = int(sys.argv[3])

random.seed()

class CuckooHashing:
	def __init__(self, n, epsilon, maxloop):
		self.maxloop = maxloop
		self.prime = 1000003
		self.r = int((1 + epsilon)*n) #size of each table
		self.d = 4 #number of tables
		self.T = range(self.d)
		self.h = range(self.d)
		for i in range(self.d):
			self.T[i] = range(self.r)
			for k in range(self.r): #initialize all with None
				self.T[i][k] = None
			#get d hash functions from universal family
			hf = HashFunction(self.r, self.prime)
			self.h[i] = hf.h

	def busca(self, x):
		for i in range(self.d):
			if self.T[i][self.h[i](x)] == x:
				return True
		return False

	def insere(self, x):
		if self.busca(x):
			return
		for i in range(self.maxloop):
			for k in range(self.d):
				self.T[k][self.h[k](x)], x = x, self.T[k][self.h[k](x)]
				if not x:
					return
		self.rehash(x)

	def insertaux(self, x):
		if self.busca(x):
			return True
		for i in range(self.maxloop):
			for k in range(self.d):	
				self.T[k][self.h[k](x)], x = x, self.T[k][self.h[k](x)]
				if not x:
					return True
		return False

	def rehash(self, key):
		t = range(self.d)
		for i in range(self.d):
			t[i] = range(0, self.r) #buffer
		for i in range(0, self.r):
			for k in range(self.d):
				t[k][i] = self.T[k][i]
				self.T[k][i] = None
		for i in range(self.d):
			hf = HashFunction(self.r, self.prime)
			self.h[i] = hf.h
		self.insertaux(key)
		for i in range (0, self.r):
			for k in range(self.d):
				if t[k][i] != None:
					sucesso = self.insertaux(t[k][i])
					if not sucesso:
						for l in range(self.d):
							self.T[l] = t[l]
						return self.rehash(key)

	def printf(self):
		for i in range(self.d):
			print i, self.T[i]
