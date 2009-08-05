#!/usr/bin/env python
# encoding: utf-8
"""
GA.py

Created by Rafael  Jegundo on 2009-06-21.
Copyright (c) 2009 . All rights reserved.
"""

from random import random
from math import exp, sqrt
import operator
import sys

def initialPop(iPopSize, hi, lo,Chromosomes,A):	
	
	for a in range(iPopSize):
		
			Chromosomes.append([A, (hi-lo)*random()+lo])
			
	return Chromosomes
	

def costFunction(par,data,n):

	F = []

	s = 0
	
	for t in range(n):

		F.append(par[0]*exp(-t*par[1]))

	for t in range(n):	

		s += (float(data[t])-F[t])**2

	return s
	
	
def cost(genes, data, n):

	aveCost = 0

	for a in genes:

		a[0] = costFunction(a[1],data,n)

		aveCost += a[0]	

	aveCost = aveCost/len(genes)

	return genes
	

def mate(genes,A):

	beta = random()

	goodGenes = len(genes)/2

	for i in range(goodGenes-1):

		gene1 = genes[i][1]

		gene2 = genes[i+1][1]

		newGene1 = [A,beta*gene1[1]+(1-beta)*gene2[1]]

		newGene2 = [A,beta*gene2[1]+(1-beta)*gene1[1]]

		genes[goodGenes+i][1] = newGene1

		i+=1 

		genes[goodGenes+i][1] = newGene2

	return genes
	
def mutate(genes,popSize,pars,mutateRate):

	for m in range(int(popSize*pars*mutateRate)) :

		row = int(popSize*random())

	#	col = int(pars*random())
		
		col = 1
		
		genes[row][1][col] = (hi-lo)*random()+lo

	return genes
		
def dRdBeta2(t,A, beta2):

	return -t*A*exp(-beta2*t) 
	
def rFunction(y,x,beta1, beta2):

	return y[x]-beta1*exp(-beta2*x)
		
def newton(data,beta,n,A):
		
	increment = [0,0]
	
	convergence = False
	
	while not(convergence):
		
		beta[0] = A
		
		betaOld = beta
		
		for i in range(1,n) :
			
			increment[1] = rFunction(data, i, beta[0], beta[1])/dRdBeta2(i,beta[0],beta[1])
		
			beta[1]+= increment[1]
			
		if abs(betaOld[1]-beta[1]) <= 0.001 :
		
			convergence = True
		
	convergence = False
	
	return beta

	
def genetic(data,A):
	
	genesFile = open('genes.dat', 'w')

	costFile = open('cost.dat','w') # cost(t_n)

	popSize = 0.5

	iPopSize = 20

	maxIterations = 20

	keep = 0.5

	pars = 2

	mutateRate = 0.4

	hi = 0.4

	lo = 0.000001

	Chromosomes = []

	iChromosomes = []
	
	
	n = len(data)
	
	initialPop(iPopSize,hi,lo,Chromosomes,A)
	
	genN = 0
	
	# First Generation
	
	for gene in Chromosomes:
		
		iChromosomes.append([costFunction(gene,data,n), gene])
		
		
	iChromosomesSorted = sorted(iChromosomes, key=operator.itemgetter(0))

	# Deleting the worst half
		
	genesSorted = [iChromosomesSorted[a] for a in range(len(iChromosomesSorted)/2)]
		
	while genN < maxIterations:
		
		genes = genesSorted	
		
		genesOld = genes
		
		for line in genes : 
			
			genesFile.write(str(line) + '\n')
			
			
		genesFile.write('\n\n')
		
	
		# Mate
	
		genes = mate(genes,A)
		
		
		# Mutate
		
		genes = mutate(genes,popSize,pars,mutateRate)
		
		
		# Calculate cost
		
		genes = cost(genes,data,n)
		
		# Sort
		
		genesSorted = sorted(genes, key=operator.itemgetter(0))
					
		genN += 1
		
	genesFile.close()
	
	costFile.close()
	
	results = [genes[1][1][0], genes[1][1][1]]
	
	results = newton(data, results,n,A)
		
	return results
