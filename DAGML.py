class DAG(object):
	

	def __init__(self, path,spacing=True):
		file=open(path,'r+')
		self.DAG=file.read().split('\n') 
		del self.DAG[-1] #import adds blank line at end
		file.close()
		self.dagIndents = []
		dagItem= ''
		spaceCount = int() 
		spaces = int()
		maxSpaces = int() 
		self.indentSize = 999
		for i in range(0,len(self.DAG)):#goes through DAG line by line
			dagItem= self.DAG[i] 
			for j in range(0,len(dagItem)):
				if dagItem[j] != ' ':
					spaces = j #j increments until the j-th character in the i-th DAG line is not blank
					break
				elif j == len(dagItem)-1:
					spaces = j+1 #handles the case where it goes all the way to the end of the line
			if spaces > 0 and spaces < self.indentSize:     
				self.indentSize = spaces #This keeps track of the smallest nonzero number of spaces at the beginning of a line 
			if spaces > maxSpaces:
				maxSpaces = spaces #Largest number of spaces at beginning of line 
		if self.indentSize == 999 and maxSpaces > 0 : #Minimum number of spaces at the beginning of an indented line does not have a value below 999
			raise Exception('Error processing Indentation/spaces in input file')  
		for i in range(0,len(self.DAG)): #Goes through DAG again line by line and assigns number of indents, since the previous loop found the number of spaces in one indent  
			dagItem = self.DAG[i]
			for j in range(0,len(dagItem)):
				if dagItem[j] != ' ':
					spaceCount = j
					break
				elif j == len(dagItem)-1:
					spaceCount = j+1
			if spaceCount%self.indentSize == 0:
				self.dagIndents.append(spaceCount//self.indentSize) 
			else:
				raise Exception('WARNING: Input DAG file has improper or irregular spacing in line indentations')  
		self.dagItem = [] 
		self.dagFlows = []
		dagFlowItems = []
		itemEndChar = 0 
		mergeLine = False
		digitOrColon = []
		for i in range(0,len(self.DAG)):
			dagFlowItems = []  
			itemAndFlow = self.DAG[i].strip()  
			mergeLine = False
			digitOrColon = []
			for j in range(0,len(itemAndFlow)):
				digitOrColon.append(((itemAndFlow[j]).isdigit()) or (itemAndFlow[j] == ':'))
			for j in range(0,len(itemAndFlow)):  
				if itemAndFlow[j] == '(' or itemAndFlow[j] == '[' or j == len(itemAndFlow)-1:  
					itemEndChar = j
					break
			if len(itemAndFlow) > 4:
				if itemAndFlow[0:5] == 'merge':
					mergeLine = True
			if (not mergeLine):
				if itemEndChar < 1:
					raise Exception('WARNING: Operator and/or branch name(s) given as empty strings.')  
				self.dagItem.append(itemAndFlow[0:itemEndChar])
				for k in range(itemEndChar,len(itemAndFlow)-1):
					if (digitOrColon[k]) and (not (digitOrColon[k-1])):
						for l in range(k,len(itemAndFlow)-1):
							if (not (digitOrColon[l+1])):
								dagFlowItems.append(itemAndFlow[k:l+1])
								break
				self.dagFlows.append(tuple(dagFlowItems))
			else:
				self.dagItem.append(self.DAG[i].strip())  
				self.dagFlows.append(tuple())     


	def export(self,path): 
		file=open(path,'w+')
		spaceString = ''
		itemPlusFlow = ''
		itemAndFlow= ''
		dagNameItem = ''
		for i in range(0,len(self.dagIndents)):
			spaceString = ''  
			dagNameItem = self.dagItem[i] + ' '
			if str(self.dagFlows[i]) != '()' or dagNameItem[0] == '<':
				itemPlusFlow = self.dagItem[i] + str(self.dagFlows[i])
			else:
				itemPlusFlow = self.dagItem[i]  
			itemAndFlow= ''
			for j in range(0,len(itemPlusFlow)):
				if (itemPlusFlow[j] != '\'') and ((itemPlusFlow[j] != ' ') or j < len(self.dagItem[i])):
					itemAndFlow= itemAndFlow+ (itemPlusFlow[j])
			if dagNameItem[0] == '<':
				itemAndFlow= itemAndFlow.replace(")","]") 
				itemAndFlow= itemAndFlow.replace("(","[") 
				itemAndFlow= itemAndFlow.replace(",","][") 
			for j in range(0,self.indentSize*self.dagIndents[i]):
				spaceString = spaceString+' '
			file.write(spaceString+itemAndFlow+'\n')
		file.close()


	def branchesInDag(self): #returns name list
		branches=[]

		for i in range(0,len(self.dagItem)):
			(self.dagItem[i]+' ')[0]
			if (self.dagItem[i]+' ')[0]=='<':
				branches.append(self.dagItem[i][1:len(self.dagItem[i])])
		return branches


	def operatorsInBranch(self,branch): 
		branchStart=int()
		branchEnd=int()
		for i in range(0,len(self.dagItem)):
			if self.dagItem[i] =='<'+str(branch):
				branchStart=i
				print(str(branchStart)+'_')
				break
		for i in range(branchStart+1,len(self.dagItem)):
			if (self.dagItem[i]+' ')[0]=='<' or self.dagIndents[i] != self.dagIndents[i-1]:
				branchEnd=i
				print(branchEnd)
				break
		return branchEnd-branchStart-1


	def addOperator(self,branchName,operator,input,output,position): 
		branchStart = self.dagItem.index('<'+branchName)
				
		if self.operatorsInBranch(branchName)+1 < position:
			raise Exception('Position value too high for branch length')
		else:
			self.dagItem.insert(branchStart+position+1,operator)
			self.dagFlows.insert(branchStart+position+1,(input, output))
			self.dagIndents.insert(branchStart+position+1,self.dagIndents[branchStart]) 


	def removeOperator(self,operator,input,output,clear=True,duplicateIndex=0): #clear means remove empty branches
		#duplicateIndex behavior: for str input, generate ordered list of indices of operators with name (using for loop)
		#then use list[duplicateIndex] to select indice, then use that operator
		if type(operator)==int:
			operIndex = self.dagItem.index(str(operator)) 
			del self.dagItem [operIndex] 
			del self.dagFlows [operIndex]
			del self.dagIndents [operIndex]      
				if clear and (self.dagItem[operIndex-1] + ' ')[0]=='<' and (self.dagItem[operIndex] + ' ')[0]=='<' :
					del self.dagItem [operIndex-1] 
					del self.dagFlows [operIndex-1]
					del self.dagIndents [operIndex-1] 
		elif type(operator)==str:
			operIndex = self.dagItem.index(operator)
			del self.dagItem [operIndex] 
			del self.dagFlows [operIndex] 
			del self.dagIndents [operIndex]
				if clear and (self.dagItem[operIndex-1] + ' ')[0]=='<' and (self.dagItem[operIndex] + ' ')[0]=='<' :
					del self.dagItem [operIndex-1] 
					del self.dagFlows [operIndex-1] 
					del self.dagIndents [operIndex-1]          
		else:
			raise Exception('operator must be integer or string')  
			
	def addBranch(self, branch, tupleStrings, operator): #format tupleStrings like ('6:7','8:9')
		self.dagItem.insert(self.dagItem.index(operator)+1,'<'+branch)
		self.dagFlows.insert(self.dagItem.index(operator)+1,tuple(tupleStrings))
		self.dagIndents.insert(self.dagItem.index(operator)+1,self.dagIndents[self.dagItem.index(operator)]+1)    


	def removeBranch(self,branch,clear=False,mergeCheck = True): 
		branchMerged = False
		if mergeCheck :
			for i in range(self.dagItem.index('<'+branch),len(self.dagItem)):
				if len(self.dagItem[i]) > 4 + len(branch):
					if self.dagItem[i][0:5] == 'merge':
						for j in range(0,(len(self.dagItem[i]) - len(branch) + 1)):  
							if branch == self.dagItem[i][j:j+len(branch)]:
								branchMerged = True
								print("You are attempting to remove a branch which is later found in a merge. Operation canceled.")
		if( not branchMerged):
			if (self.dagItem[self.dagItem.index('<'+branch)+1] + ' ')[0] == '<':
				del self.dagIndents [self.dagItem.index('<'+branch)]
				del self.dagFlows [self.dagItem.index('<'+branch)]
				del self.dagItem [self.dagItem.index('<'+branch)]
			elif clear:
				branchIndex = self.dagItem.index('<'+branch)
				del self.dagItem[branchIndex]
				del self.dagFlows[branchIndex]
				del self.dagIndents[branchIndex]
				while (self.dagItem[branchIndex] + ' ')[0] != '<':
					del self.dagItem[branchIndex]
					del self.dagFlows[branchIndex]
					del self.dagIndents[branchIndex]
			else:
				raise Exception('Branch not removed because it has one or more operators')


	def addMerge(self,branchList,destination): 
		branchPos=[]
		mergePos = len(self.dagItem)
		for i in range(0,len(branchList)):
			branchPos.append(self.dagItem.index('<'+branchList[i])) #needs to be stripped to see if same
		maxBranchPos = max(branchPos)  
		for i in range(maxBranchPos+1,len(self.dagItem)): #Starts after last branch is defined
			if (self.dagItem[i]+ ' ')[0] == '<':
				mergePos = i #This is the next branch, which is not one of the branches being merged. Merge will be inserted just before this branch is defined
				break 
		print(mergePos)
		print(maxBranchPos)
		toMerge = ''
		for i in range(0,len(branchList)):
			toMerge = toMerge + branchList[i] +', ' #Builds up list of branches to merge in DAGML format
		if mergePos < len(self.dagItem):
			indentationOfMerge = max([self.dagIndents[mergePos]-1,0])
		else:
			indentationOfMerge = max([self.dagIndents[mergePos-1]-1,0])
		self.dagItem.insert(mergePos,'merge('+toMerge+destination+')') #inserts merge
		self.dagFlows.insert(mergePos,tuple())
		self.dagIndents.insert(mergePos,indentationOfMerge)

	def removeMerge(self,branchList,destination):
		toMerge = ''
		for i in range(0,len(branchList)):
			toMerge = toMerge + branchList[i] +', ' 
		del self.dagIndents[self.dagItem.index('merge('+toMerge+destination+')')]
		del self.dagItem[self.dagItem.index('merge('+toMerge+destination+')')] #removes merge


	def editIO(self,operator, input,output, duplicateIndex=0): #operators
	    operIndex = self.dagItem.index(operator) #operator string must include arguments of pre-existing operator
	    del self.dagFlows[operIndex]
	    self.dagFlows.insert(operIndex,(input, output))    


	def editSlice(self,branch, input, output, duplicateIndex=0):  #format tupleStrings like ('6:7','8:9')
	    branchIndex = self.dagItem.index('<'+branch) 
	    del self.dagFlows[branchIndex]
	    self.dagFlows.insert(branchIndex,(input, output))    
