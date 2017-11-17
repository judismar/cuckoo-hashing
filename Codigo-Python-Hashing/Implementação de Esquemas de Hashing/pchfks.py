import math
import random
import sys
import time
from uhprime import HashFunction
from phfks import PerfectHashTable
random.seed()

#n = int(sys.argv[1])
#epsilon = float(sys.argv[2])
#constloops = int(sys.argv[3])

class CuckooHashingPerfectRehashfks:
	def __init__(self, n, epsilon):
		self.prime = 1000003
		self.r = int((1 + epsilon)*math.ceil(math.sqrt(n))) #size of each table
		self.d = int(math.ceil(math.sqrt(n))) #number of tables: function  of n -> ceil(sqrt(n))
		self.T = range(self.d)
		for i in range(self.d):
			self.T[i] = PerfectHashTable(self.r, [], self.prime)
			self.T[i].hf = HashFunction(self.r, self.prime)
		
	def busca(self, x):
		for i in range(self.d):
			if self.T[i].lookup(x):
				return True
		return False

	def insere(self, x):
		if self.busca(x):
			return
		k = 0
		for i in range(self.d): #maxloop is actually ceil(sqrt(n)) in this Cuckoo Hashing scheme
			k = random.randint(0, self.d-1) #all moves are made at random tables
			x = self.T[k].insert(x)
			if x == -1:
				return
		self.perfectRehash(k, x)

	def perfectRehash(self, tableIndex, key):
		aux = self.T[tableIndex].elements()
		aux.insert(-1, key)
		self.T[tableIndex] = PerfectHashTable(self.r, aux, self.prime)

	def printf(self):
		for i in range(self.d):
			print i
			self.T[i].printf()
