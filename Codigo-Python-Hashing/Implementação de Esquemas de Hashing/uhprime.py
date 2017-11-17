import random

#instances of this class are members of a universal family
class HashFunction: #universal, i.e. probability of colision is at most 1/m
	def __init__(self, m, p):
		self.m = m
		self.p = p
		self.a = random.randint(1, p-1)
		self.b = random.randint(0, p-1)

	def h(self, x):
		return ((self.a*x + self.b) % self.p) % self.m
