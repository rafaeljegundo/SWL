#!/usr/bin/env python
# encoding: utf-8
"""
Created by Rafael  Jegundo on 2009-06-20.
Copyright (c) 2009. All rights reserved.
"""

import os
import operator
import GAs
import sys
import numpy
from math import log, exp, sqrt
from random import shuffle, random, uniform

def inputData(data):

	""" Esta função procura """
		
	folder = raw_input("Path to folder")
	
	files = os.listdir(folder)
	
	files = filter(lambda x: x[-3:] == 'txt', files)
	
	for txt in files:
	
		f = open(folder + txt , 'r')
				
		for line in f :
			
			data.append(line[:-1].split('\t'))
								
		f.close()
		
		data = filter( lambda x: type(eval(x[0])) == int ,data)
		
	f = open('data.dat', 'w')
		
	for line in data :
			
		f.write(line[0] + '\t' + line[1] + '\t' + line[2] + '\n')
			
	f.close()	
	
	sys.exit()
	
	return data


def orderingData(data,r):
	
	data = sorted(data, key=operator.itemgetter(0))
	
	
	for line in data :
		
		if line[0] not in r :
			
			r.append(line[0])
	
	r = map(float,r)	
	
	r.sort()
		
	return data, r

	
def treatingData(data, r):
	
	pars = []
	erros = []
	
	global A
	
	A = 0
	N = 0
	
	vArray = []
		
	vFile = open('test.dat','r')
	
	for line in vFile:
		
		vArray.append(float(line))

	vFile.close()
	
	for line in data:
			
			vR = vArray[int(line[0])]
			A += float(line[2])/(exp(-int(line[1])*vR))
			N += 1

	A = A/N
	
	for n in r :
		
		data2 = []
			
		for line in data :
						
			index = float(line[0])
		
			t = float(line[1])
			
			W = float(line[2])
			
			if index == n :
				
				data2.append((float(line[1]),float(line[2])))
						
		## Ordering data2 trough t 
			
		data2 = sorted(data2, key=operator.itemgetter(0))
		
		data3 = []
		
		index = 0
		
		VZero = 0
		
		for a in range(24) :
			
			s = 0
			
			while a == data2[index][0] :
				
				s += data2[index][1]
				
				index += 1
			
			data3.append(s/index)
		
			VZero += data3[a]
			
	#	print -VZero/24		
			
		## Runing Genetic Algorithm

		genetics = GAs.genetic(data3,A)
						
		pars.append([genetics[0], genetics[1]])
			
	return data, pars

def bootstrap(conf):
	
	l = len(conf)
	
	bootstraped = []	
	
	for i in range(0,l): 
		
		alpha = int(uniform(0,l))    # choose random config 
		
		bootstraped.append(conf[alpha])    # keep G[alpha]
	
	bootstraped.sort()
	
	v = bootstraped[len(bootstraped)/2]
			
	return v

def sdev(array, mew):
	
	array.sort()
	
	sigma = 0
		
	for a in array :
		
		sigma += (a-mew)*(a-mew)		
		
	sigma = sqrt(sigma/len(array))
	
	return sigma
	
def bootstrapping(data):
	
	erros = [0]	
	
	for r in range(1,13):

		conf = []
		
		mean = []
		
		for line in data:
		
			if r == int(line[0]):
				
				conf.append(float(line[2]))
		
		mew = conf[len(conf)/2]
				
		for i in range(10*24):		
			
			mean.append(bootstrap(conf))
			
		erros.append(sdev(mean,mew))
	
	return erros

def outputData(pars,erros):
	
	f = open('pars.dat','w')	
	
	i = 0
	
	for line in pars :
		
		f.write(str(i) + '\t' + str(line[1]) + '\t' + str(erros[i]) + '\n')
	
		i += 1
		
	f.close()
	
	return
	


def main():
	
	data = [] # r,t,W
	
	r = []
	
 	data = inputData(data)
	
	f = open('data.dat','r')
	
	for line in f :

		data.append(line[:-1].split('\t'))
	
	f.close()

	erros = bootstrapping(data)
	
	data, r = orderingData(data, r)
	
	data, pars = treatingData(data, r)

	outputData(pars,erros)
	
	pass



if __name__ == '__main__':
	main()

