
#Naive Bayesian Code

from __future__ import division
import collections
import math


class NaiveBayesian:
	def __init__(self,inputFile):
	
		self.trainingFile = inputFile
		self.featurenames = {}      #all feature names and their possible values (including the class label)
		self.ListofFeatures = []       #track order of features
		self.featureCounts = collections.defaultdict(lambda: 1)
		self.Attributes = []        #all atributes from learning file
		self.classCounter = collections.defaultdict(lambda: 0)   #count number of classes

	def ClassifierTraining(self):
		for attribute in self.Attributes:
			self.classCounter[attribute[len(attribute)-1]]+=1
			#go through all attributes and count them
			for counter in range(0,len(attribute)-1):
				#Count features for conditional probability calculations
				self.featureCounts[(attribute[len(attribute)-1], self.ListofFeatures[counter], attribute[counter])] += 1

	
		for label in self.classCounter:
			#
			for feature in self.ListofFeatures[:len(self.ListofFeatures)-1]:
				self.classCounter[label] += len(self.featurenames[feature])

	def Classify(self,features):
		probPerClass = {}
		for label in self.classCounter:
			logProb = 0
			for featureValue in features:
				
				prob +=  (self.featureCounts[(label, self.ListofFeatures[features.index(featureValue)], featureValue)]/self.classCounter[label])
			probPerClass[label] = (self.classCounter[label]/sum(self.classCounter.values())) * (logProb)
		#debuggingl ine
		print probPerClass
	#	return max(probPerClass, key = lambda classLabel: probPerClass[classLabel])

	def GetValues(self):
		file = open(self.trainingFile,'r')
		for line in file:
			if line[0]!='@':#start of data
				self.Attributes.append(line.strip().lower().split(','))
			else:
				if line.strip().lower().find('@data')==-1 and  (not line.lower().startswith('@relation')):
					self.ListofFeatures.append(line.strip().split()[1])
					self.featurenames[self.ListofFeatures[len(self.ListofFeatures) - 1]] = line[line.find('{')+1: line.find('}')].strip().split(',')

		file.close()


	def TestClassifier(self,inputFile):
		file = open(inputFile , 'r')
		for line in file:
			if line[0]!='@':
				vector=line.strip().lower().split(',')
				print "classifier: " + self.Classify(vector) + " given " + vector[len(vector) - 1]       

if __name__  == "__main__":
	model=NaiveBayesian("/Users/jamillan/pubs.dat")
	model.GetValues()
	model.ClassifierTraining()
	model.TestClassifier("/Users/jamillan/pubs.dat")

	
