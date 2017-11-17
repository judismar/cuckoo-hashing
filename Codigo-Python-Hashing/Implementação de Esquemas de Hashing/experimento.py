import math
import random
import sys
import time
from ch import CuckooHashing
from hashinglinked import HashTable
from pchfks import CuckooHashingPerfectRehashfks
from pchgraphs import CuckooHashingPerfectRehashgraphs

N = 100
NMEAN = 1
EPSILON = 1

def exp(strout, hashingf):
	n = 0
	output = ""
	for _ in range(N):
		amostraInsert = []
		amostraBusca = []
		n += 50
		output += str(n) + " "
		for _ in range(NMEAN):
			h = hashingf(n)
			begin = time.time()
			for i in range(n):
				h.insere(i+1)
			end = time.time()
			amostraInsert.append(float(end)-float(begin))
			begin = time.time()
			for i in range(n):
				h.busca(i+1)
			end = time.time()
			amostraBusca.append(float(end)-float(begin))
		output = output + str(1000000.0*float(mean(amostraInsert))/float(n)) + " "
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
	return CuckooHashing(n, EPSILON, int(math.log(n)))

def cuckooFKS(n):
	return CuckooHashingPerfectRehashfks(n, EPSILON)

def cuckooGraphs(n):
	return CuckooHashingPerfectRehashgraphs(n, EPSILON)

exp("/home/judismar/Desktop/hash-linked.txt", hashingLinked)
exp("/home/judismar/Desktop/cuckoo-hashing.txt", cuckoo)
exp("/home/judismar/Desktop/cuckoo-perfect-fks.txt", cuckooFKS)
exp("/home/judismar/Desktop/cuckoo-perfect-graphs.txt", cuckooGraphs)
