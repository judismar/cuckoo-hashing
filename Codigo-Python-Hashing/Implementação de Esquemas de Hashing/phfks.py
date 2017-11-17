from uhprime import HashFunction

class PerfectHashTable:
	def __init__(self, n, numList, p):
		self.t = range(n)
		for i in range(n):
			self.t[i] = HashTable() 
		self.hf = HashFunction(n, p)
		for x in numList:
			self.t[self.hf.h(x)].insert(x)
		for bin in self.t:
			bin.go(p)

	def lookup(self, x):
		return self.t[self.hf.h(x)].lookup(x)

	def insert(self, x):
		return self.t[self.hf.h(x)].insertNew(x)

	def elements(self): #return list of all elements
		l = []
		for bin in self.t:
			bin.insertElementsOnList(l)
		return l

	def printf(self):
		for bin in self.t:
			bin.printf()

class HashTable:
	def __init__(self):
		self.l = []
		self.t = []
		self.n = 0
		self.hf = None

	def go(self, p): #insert list elements in table without colision
		self.n = len(self.l)**2
		if self.n == 0:
			self.n = 1
		self.t = range(self.n)
		for i in range(self.n):
			self.t[i] = -1
		colision = True
		while colision:
			colision = False
			self.hf = HashFunction(self.n, p)
			for x in self.l:
				h = self.hf.h(x)
				if self.t[h] > -1:
					colision = True
					for i in range(self.n):
						self.t[i] = -1
					break
				self.t[h] = x

	def insert(self, x): #in list!
		self.l.insert(-1, x)

	def insertNew(self, x): #after called method go()
		h = self.hf.h(x)
		ret = self.t[h]
		self.t[h] = x
		return ret

	def lookup(self, x):
		return self.t[self.hf.h(x)] == x

	def insertElementsOnList(self, l):
		for x in self.t:
			if x > -1:
				l.insert(-1, x)

	def printf(self):
		print self.t
