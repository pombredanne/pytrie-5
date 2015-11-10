from __future__ import division
#from re import compile as _RE
import sqlite3
import timeit

class TrieNode:	
	def __init__(self, value, size):
		self.value = value
		self.size = size
		self.prob = 1
		# reference to another node
		self.children = []

class Trie:
	def __init__(self):		
		self.node = TrieNode("", 0)
		
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
	def nodesProbability(self, root):
		self.nodesProbCal(root.node)

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
	def printDFSTrie(self, root):
		self.printDFSNode(root.node)


	def printDFSNode(self, node):
		print node.value + "/ " + str(node.size) + "/ " + str(node.prob)
		print "******"
		for x in node.children:
			self.printDFSNode(x)
		if not node.children:
			return
	
	# ------------ DFS print to file ---------------
	def printDFSTraverseToFile(self, root):
		target = open('dfs-traverse-info.trie','w+')
		self.DFSTraverse(root.node, target, '')
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

class Dehkhoda:
	def __init__(self):
		self.words = []
	
	def getWords(self):
		con = sqlite3.connect("Dehkhoda.db")
		cursor = con.execute("SELECT name from dehkhoda")
		for row in cursor:
			self.words.append(row[0])
		con.close()




start = timeit.default_timer()
myTrie = Trie()

db = Dehkhoda()
db.getWords()


for x in xrange(0,len(db.words)):
	myTrie.add(db.words[x])

myTrie.nodesProbability(myTrie)
#myTrie.printDFSTrie(myTrie)
myTrie.printDFSTraverseToFile(myTrie)

stop = timeit.default_timer()

print stop - start



