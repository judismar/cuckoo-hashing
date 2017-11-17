import math

class DPHScheme: #deterministic Perfect Hashing scheme
	def __init__(self, S, m): #outputs constant C (algorithm A)
		S.sort()
		n = len(S)
		self.m = m #for perfect rehash
		m = S #all prime, no need to  use function p
		#all M[j]
		M = range(n)
		for j in range(n):
			M[j] = 1
			for i in range(n):
				if i != j:
					M[j] *= m[i]
		#all b[i]
		Ml = range(n)
		b = range(n)
		for i in range(n):
			Ml[i] = M[i] % m[i]
			if Ml[i] > 1:
				dend = m[i]
				dsr = Ml[i]
				Q = [None]
				j = 1
				Q.append(math.floor(dend/dsr))
				rmd = dend - Q[j]*dsr
				while rmd > 1:
					dend = dsr
					dsr = rmd
					j += 1
					Q.append(math.floor(dend/dsr))
					rmd = dend - Q[j]*dsr
				k = j
				B = [1, -Q[k]]
				for j in range(1, k):
					B.append(-B[j]*Q[k-j] + B[j-1])
				b[i] = B[k]
			else:
				b[i] = 1
		#C
		sumvar = 0
		prodvar = 1
		for i in range(n):
			sumvar += long(b[i])*M[i]*long(i+1) #why not M'[i]? (also: i must go from 1 to n)
			prodvar *= m[i]
		self.C = sumvar % prodvar
			
	def h(self, x):
		return (self.C % x - 1) % self.m

	def p(self, x):
		return x**2 - x + 17
