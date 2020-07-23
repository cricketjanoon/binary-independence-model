# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 05:40:58 2019
@author: cricketjanoon
"""
import numpy as np
import re
import math


##----------------------------
trainingSetCount = 32604
numberOfSearchesToShow = 5
##----------------------------

##-->> sample queries
# "gbagbo loyalists regain ground in ivory coast beach"
# "on debt ahead of high-level talks"
# "'nhl finals,' 'nixon in china'"
# "superintendent of the beaumont school district"
# "here's a look at some of the league's top young,"


#taking query from the user
inputQuery = input("Enter your query: ")
query = []
for term in inputQuery.split():
	t = re.sub(r"[^a-zA-Z0-9]","",term)
	query.append(t)

#reading the file and storing the documetns
file = open("LSI-data.txt")
documentMatrix = np.full((trainingSetCount,3), dtype=object, fill_value = "empty")
documentCount = 0
index = 0
for line in file:
	if documentCount>=trainingSetCount:
		break
	
	if line in ['\n','\r\n']:
		documentCount = documentCount + 1
		index = 0
	else:
		index = index + 1
		
	if index == 1:
		documentMatrix[documentCount,1] = line
	elif index == 2:
		documentMatrix[documentCount,2] = line
	elif index == 7:
		documentMatrix[documentCount,0] = line

#cleaning text code
for i in range(documentMatrix.shape[0]):
	for j in range(documentMatrix.shape[1]):
		documentMatrix[i,j] = re.sub(r'[^\w\s_]+', '', documentMatrix[i,j]).strip()
		documentMatrix[i,j] = documentMatrix[i,j].lower()				
documentMatrix = documentMatrix.astype(str)

documentMatrix2 = np.full((trainingSetCount), dtype=object, fill_value = "empty")
for i in range(len(documentMatrix)):
	documentMatrix2[i] = documentMatrix[i,1] + " " + documentMatrix[i, 2]	
documentMatrix2 = documentMatrix2.astype(str)

documents = list(documentMatrix2)
documentMatrix2 = None

#collect all words in the all documents
bagOfWords = []
for line in documents:
	for word in line.split():
		word = re.sub(r"[^a-zA-Z0-9]","",word)
		word = word.lower()
		if word not in bagOfWords:
			bagOfWords.append(word)
			
#instantiate term document matrix of appropriate size with zeros			
termDocumentMatrix = np.zeros((len(documents), len(bagOfWords)), dtype = 'int8')

#populate term document matrix
for i in range(len(documents)):
	docWordList = documents[i].split();
	
	for t in range(len(docWordList)):
		docWordList[t] = re.sub(r"[^a-zA-Z0-9]","",docWordList[t])
		docWordList[t] = docWordList[t].lower()
	
	for j in range(len(bagOfWords)):
		if bagOfWords[j] in docWordList:
			termDocumentMatrix[i,j] = 1

#calculate dft of each term and calculate its weight "w"
n = len(documents)
dft = np.zeros((len(bagOfWords)))
weight = np.zeros((len(bagOfWords)))

for i in range(len(bagOfWords)):
	for j in range(len(documents)):
		if termDocumentMatrix[j,i] == 1:
			dft[i] = dft[i] +1 
	weight[i] = math.log(n/dft[i], 2)


#now starting real BIM, calculating the retrieval status value of each doc
docProb = np.zeros((len(documents)))
for q in query:
	termIndex = bagOfWords.index(q)
	for d in range(len(termDocumentMatrix)):
		if termDocumentMatrix[d, termIndex] == 1:
			docProb[d] = docProb[d] + weight[termIndex]

#displaying the results			
indices = docProb.argsort()[-numberOfSearchesToShow:][::-1]
print("\n")
for i in range(len(indices)):
	print("Title:       " + documentMatrix[indices[i],1])
	print("Content:     " + documentMatrix[indices[i],2])
	print("Category:    " + documentMatrix[indices[i],0])
	print("RSV:         " + str(docProb[indices[i]]))
	print("Terms found: ", end='')
	for j in range(len(termDocumentMatrix[indices[i]])):
		if termDocumentMatrix[indices[i], j] == 1 and bagOfWords[j] in query:
			print(bagOfWords[j] + ", ", end = '')
	print("\n")