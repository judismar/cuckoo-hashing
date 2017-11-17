import math
import random
import sys
import time
from hashinglinked import HashTable
from pch import CuckooHashingPerfectRehash
from ch import CuckooHashing

N = 100
NMEAN = 10
EPSILON = 1

P = []
with open("primos", "r") as f:
	for x in f:
		P.append(int(x))

def exp(strout, hashingf, chaves = None):
	chavesBuffer = chaves
	n = 0
	output = ""
	for _ in range(N):
		amostraInsert = []
		amostraBusca = []
		n += 40
		if not chavesBuffer:
			chaves = range(1, n+1)
		output += str(n) + " "
		for _ in range(NMEAN):
			h = hashingf(n)
			begin = time.time()
			for i in range(n):
				h.insere(chaves[i])
			end = time.time()
			amostraInsert.append(float(end)-float(begin))
			begin = time.time()
			for i in range(n):
				h.busca(-1)
			end = time.time()
			amostraBusca.append(float(end)-float(begin))
		output = output + str(1000000.0*float(mean(amostraInsert))/float(n)) + " "
		output = output + str(1000000.0*float(mean(amostraBusca))/float(n)) + "\n"
	f = open(strout, "w")
	f.write(output)
	f.close()
	print "Experimento finalizado!"

def expPiorCasoBuscaCuckoo(strout):
	n = 0
	output = ""
	for _ in range(N):
		amostraBusca = []
		n += 40
		output += str(n) + " "
		for _ in range(NMEAN):
			h = CuckooHashing(n, EPSILON, int(math.log(n)))
			begin = time.time()
			for i in range(n):
				h.busca(-1)
			end = time.time()
			amostraBusca.append(float(end)-float(begin))
		output = output + str(1000000.0*float(mean(amostraBusca))/float(n)) + "\n"
	f = open(strout, "w")
	f.write(output)
	f.close()
	print "Experimento finalizado!"

def mean(numlist):
	sumvar = 0
	for num in numlist:
		sumvar += num
	return float(sumvar)/float(len(numlist))

def hashingLinked(n):
	return HashTable(n, EPSILON)

def cuckoo(n):
	return CuckooHashingPerfectRehash(n, EPSILON)

exp("/home/judismar/Desktop/hash-linked-pior-caso.txt", hashingLinked)
exp("/home/judismar/Desktop/cuckoo-hashing-perfeito-pior-caso.txt", cuckoo, P)
expPiorCasoBuscaCuckoo("/home/judismar/Desktop/cuckoo-hashing-pior-caso-busca.txt")
