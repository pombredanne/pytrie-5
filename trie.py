# -*- coding: utf-8 -*-
from __future__ import division
import sqlite3
import timeit

class TrieNode:	
	def __init__(self, value, size):
		self.value = value
		self.size = size
		self.prob = 1
		# reference to another nodes
		self.children = []

class Trie:
	def __init__(self):		
		self.node = TrieNode("", 0)
		self.words = []
		self.maxLevel = 0
		self.averageLevel = 0
		self.totalLeaf = 0
			
	#------------- connect and fetch from DB (table and database must have same name) ----------------
	def getWordsFromDB(self, dbName, tableName):
		con = sqlite3.connect(dbName)
		cursor = con.execute("SELECT name from "+tableName)
		for row in cursor:
			self.words.append(row[0])
		con.close()

	def add(self, value):
		self.node.size+=1
		list(value)
		valueCounter = 0
		parent = self.node
		while valueCounter < len(value) and self.findChar(value[valueCounter], parent):					
			x = self.findChar(value[valueCounter], parent)
			x.size +=1
			valueCounter += 1
			parent = x
		if valueCounter != len(value):
			for additionalChars in xrange(valueCounter,len(value)):
				parent = self.addChar(value[additionalChars], parent)
			return True
		else:
			return False

	def findChar(self, inputChar, parent):		
		find = False
		for x in xrange(0,len(parent.children)):
			if (parent.children[x].value == inputChar):
				find = parent.children[x]
		return find		

	def addChar(self, childChar, parent):
		if not self.findChar(childChar, parent):
			child = TrieNode(childChar, 1)
			parent.children.append(child)
			return parent.children[len(parent.children)-1]
		return False

	# -------  probability of each node ----------
	def nodesProbability(self):
		self.nodesProbCal(self.node)

	def nodesProbCal(self, node):
		self.nodesCondProbCal(node)
		for x in node.children:
			x.prob = x.prob * node.prob
			self.nodesProbCal(x)
		if not node.children:
			return
			
	def nodesCondProbCal(self, node):
		#print "******"
		for x in node.children:
			x.prob = x.size / node.size
			self.nodesCondProbCal(x)
		if not node.children:
			return	

	# -----------  DFS print of Trie --------------
	def printDFSTrie(self):
		self.printDFSNode(self.node)


	def printDFSNode(self, node):
		print node.value + "/ " + str(node.size) + "/ " + str(node.prob)
		print "******"
		for x in node.children:
			self.printDFSNode(x)
		if not node.children:
			return
	
	# ------------ DFS print of Trie to file ---------------
	def printDFSTraverseToFile(self):
		target = open('dfs-traverse-info.trie','w+')
		self.DFSTraverse(self.node, target, '')
		target.close()


	def DFSTraverse(self, node, fileName, fileVal):
		fileVal += node.value
		word = 'value: '+fileVal+'*, prob:'+str(node.prob)
		fileName.write(word.encode('utf-8'))
		fileName.write('\n')
		for child in node.children:
			self.DFSTraverse(child, fileName, fileVal)
		if not node.children:
			return	

	# -------------  most probable words in level L of tree  ------------
	def leafsOfLevel(self, level):
		leafdict = {}
		self.leafsOfLevelDFS(self.node, level, 0, leafdict, "")
		return leafdict
		
	def leafsOfLevelDFS(self, node, level, levelCounter, leafdict, traverseVal):
		traverseVal += node.value;
		if levelCounter == level:
			leafdict[traverseVal] = node.prob
			return
		if not node.children:
			return
		for child in node.children:
			self.leafsOfLevelDFS(child, level, levelCounter+1, leafdict, traverseVal)

	def printMaxLevelProbsFromOneToFile(self, levelOnetoLevel):
		target = open('max_probs.trie','w+')
		for x in xrange(1,30):
			levelDict = self.leafsOfLevel(x)
			maxValue = 0
			maxKey = ""
			for key, value in levelDict.iteritems():	
				if value>maxValue:
					maxValue = value
					maxKey = key
			target.write((maxKey + "* p=" + str(maxValue)).encode('utf-8') + "\n") 
		target.close()

	# ---------   get max level of trie leafs ------------
	def maxLevelCatch(self):
		self.trieMaxLevel(self.node, -1)
		self.maxLevel 
		return self.maxLevel

	def trieMaxLevel(self, node, startLevel):
		startLevel += 1
		if not node.children:
			if startLevel > self.maxLevel:
				self.maxLevel = startLevel
			return
		for child in node.children:
			self.trieMaxLevel(child, startLevel)

	# --------------  average level of trie leafs  ----------
	def averageLevelCatch(self):
		self.trieAverageLevel(self.node, 0)
		self.averageLevel = self.averageLevel / self.totalLeaf
		return self.averageLevel	

	def trieAverageLevel(self, node , level):	
			if not node.children:
				self.totalLeaf += 1
				self.averageLevel += level
				return
			level += 1
			for child in node.children:
					self.trieAverageLevel(child, level)	

	#  ------------- find a word in trie and return true or false ---------
	def findWord(self, word):
		list(word)
		wordCounter = 0
		parent = self.node
		while wordCounter < len(word) and self.findChar(word[wordCounter], parent):					
			x = self.findChar(word[wordCounter], parent)
			wordCounter += 1
			parent = x
		if wordCounter == len(word):
			childrenSizeNum = 0
			if not parent.children:
				return True
			else:
				for child in parent.children:
					childrenSizeNum += child.size
				if childrenSizeNum < parent.size:
					return True
		else:
			return False

	# ----------------   get trie inserted words average length -----------
	def wordsAverageLength(self):
		sizeSum = 0
		for word in self.words:
			sizeSum += len(word)

		return sizeSum / len(self.words)

start = timeit.default_timer()
myTrie = Trie()
myTrie.getWordsFromDB("Dehkhoda.db","Dehkhoda")
for x in xrange(0,len(myTrie.words)):
	myTrie.add(myTrie.words[x])
myTrie.nodesProbability()
#print myTrie.findWord(u'آآآ')
#print myTrie.wordsAverageLength()
'''
myTrie.add("efa")
myTrie.add("efalarma")
myTrie.add("efalary")
myTrie.add("efalamy")
myTrie.add("efalao")
myTrie.printDFSTrie()
'''
#myTrie.printDFSTrie()
#print myTrie.maxLevelCatch()
#print myTrie.findWord('efa')
#print myTrie.averageLevelCatch()
#myTrie.printDFSTraverseToFile()
'''   -------------  check if sum of probabilities is 1 or not  ------------
check = 0
for x in levelThreeProb:
	check += x

print check
'''
#print myTrie.averageLevelCatch(myTrie)
''' ------------------ catch the maximum level of the trie --------------------
print myTrie.maxLevelCatch()
'''

''' ---------------- print maximum probability in each level -------------------
myTrie.printMaxLevelProbsFromOneToFile(30)
'''
#print max(levelThreeProb)
#print levelThreeProb.index(max(levelThreeProb))
stop = timeit.default_timer()
print "execution time = " + str(stop - start)



