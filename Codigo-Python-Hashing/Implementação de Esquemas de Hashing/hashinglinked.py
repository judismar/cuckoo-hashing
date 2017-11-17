import sys
import time
from uhprime import HashFunction

class Lista:
	def __init__(self):
		self.prox = None
		self.valor = 0
	def insere(self, v):
		aux = self.prox
		self.prox = Lista()
		self.prox.valor = v
		self.prox.prox = aux
	def busca(self, v): #o valor existe na lista?
		aux = self.prox
		while aux != None:
			if aux.valor == v:
				return True
			aux = aux.prox
		return False
	def imprime(self):
		aux = self.prox
		while aux != None:
			print aux.valor
			aux = aux.prox
		print "--fim--"

class HashTable:
	def __init__(self, n, epsilon):
		self.n = int((1 + epsilon)*n)
		self.t = range(self.n)
		for i in range(self.n):
			self.t[i] = Lista()
		hf = HashFunction(self.n, 1000003)
		self.h = hf.h
	def insere(self, v):
		if self.busca(v):
			return
		self.t[self.h(v)].insere(v)
	def busca(self, x):
		return self.t[self.h(x)].busca(x)
	def imprime(self):
		for i in range(self.n):
			self.t[i].imprime()
