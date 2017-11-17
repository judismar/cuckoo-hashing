import random
import math
from uhprime import HashFunction

class Graph:
	def __init__(self, gen, numList):
		n = len(numList)
		self.v = gen.v
		self.mi = 0 #mi = n after inserting all edges
		self.r = gen.r
		self.mult = int(2**math.ceil(math.log(self.r, 2))) #extra bit alocation to avoid repeated identifiers for edges
		#the graph will be represented in the computer's memory with arrays FIRST, NEXT, PREV and NODE, explained with details in Majewski et al.
		self.FIRST = range(self.v)
		self.NEXT = range(n*self.mult)
		self.PREV = range(n*self.mult)
		self.NODE = range(n)
		for i in range(self.v):
			self.FIRST[i] = -1
		for i in range(n):
			self.NODE[i] = range(self.r)
		#now: mapping keys into edges
		for key in numList: #generating each edge
			edge = range(self.r) #set of r vertices
			for k in range(self.r):
				edge[k] = gen.f(k, key)
			#device to generate different vertices not working!
			self.insertEdge(edge)
		#	print edge
		#print ""

	def insertEdge(self, vertexSet):
		for i in range(self.r):
			self.NODE[self.mi][i] = vertexSet[i]
			if self.FIRST[vertexSet[i]] != -1:
				self.PREV[self.FIRST[vertexSet[i]]] = self.mi*self.mult + i
			self.NEXT[self.mi*self.mult + i] = self.FIRST[vertexSet[i]]
			self.PREV[self.mi*self.mult + i] = -1
			self.FIRST[vertexSet[i]] = self.mi*self.mult + i
		self.mi += 1

	def deleteEdge(self, edge):
		self.stack.append(edge)
		for i in range(self.r):
			if self.PREV[edge*self.mult + i] == -1: #initial edge
				self.FIRST[self.NODE[edge][i]] = self.NEXT[edge*self.mult + i]
			else: #not initial
				self.NEXT[self.PREV[edge*self.mult + i]] = self.NEXT[edge*self.mult + i]
			if self.NEXT[edge*self.mult + i] != -1: #not at the end
				self.PREV[self.NEXT[edge*self.mult + i]] = self.PREV[edge*self.mult + i]

	def deleteRecursively(self, edge):
		self.deleteEdge(edge)
		for i in range(self.r):
			if self.degree1(self.NODE[edge][i]):
				self.deleteRecursively(self.FIRST[self.NODE[edge][i]]/self.mult)

	def degree1(self, vertex):
		return self.FIRST[vertex] != -1 and self.NEXT[self.FIRST[vertex]] == -1 

	def acyclic(self): #is the hipergraph acyclic?
		self.stack = [] #stack of removed edges
		for v in range(self.v): #scanning vertices
			if self.degree1(v):
				e = self.FIRST[v]/self.mult
				self.deleteRecursively(e)
		for e in self.FIRST: #is there any edge left?
				if e != -1:
					return False #yes
		return True

	def assignment(self, numNones):
		self.mi += numNones
		h = range(self.mi)
		g = range(self.v)
		for i in range(self.v):
			g[i] = -1
		while len(self.stack) > 0:
			edge = self.stack.pop()
			unassignedVertices = []
			for i in range(self.r):
				if g[self.NODE[edge][i]] == -1:
					unassignedVertices.append(self.NODE[edge][i])
			for i in range(1, len(unassignedVertices)):
				g[unassignedVertices[i]] = 0
			aux = 0
			for i in range(self.r):
				if g[self.NODE[edge][i]] != -1:
					aux += g[self.NODE[edge][i]]
			g[unassignedVertices[0]] = (h[edge] - aux) % self.mi
		return g

	def printg(self):
		for i in range(self.v):
			print "Vertice ", i
			aux = self.FIRST[i]
			while aux != -1:
				print aux/self.mult
				aux = self.NEXT[aux]

class HashFunctionGenerator:
	def __init__(self, r, p):
		random.seed()
		self.r = r
		self.p = p
		self.hf = range(r)

	def reset(self):
		for i in range(self.r):
			self.hf[i] = HashFunction(self.v, self.p)

	def f(self, i, x):
		return self.hf[i].h(x)

	def mapping(self, numList, numNones): #searches for an acyclic graph in a random fanshion, then solves the assigmnent problem
		self.v = int(math.ceil(2.09*len(numList))) #ceiling of c*n
		self.reset() #init the functions
		while True: #repeats until acyclic graph is found and returned
			graph = Graph(self, numList)
			if graph.acyclic():
				self.graph = graph
				self.g = graph.assignment(numNones)
				return
			self.reset()

	def h(self, key):
		aux = 0
		for i in range(self.r):
			aux += self.g[self.f(i, key)]
		return aux % self.graph.mi
