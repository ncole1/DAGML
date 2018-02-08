class DAG(object):
	#variable name changes:
	#no names longer than 12 characters
	#DAG can be lower case
	#remove references to stripped DAG since it's no longer an object
	#real error messages
	#raise Exception('My error!') instead of printing error messages

	def __init__(self, path,spacing=True):
		file=open(path,'r+')
		self.DAG=file.read().split('\n') 
		del self.DAG[-1] #import adds blank line at end
		file.close()
		self.dagIndentation = []
		currentDAGItem= ''
		numberOfSpaces = int() 
		spaces = int()
		maxSpaces = int() 
		self.spacesPerIndent = 999
		for i in range(0,len(self.DAG)):#goes through DAG line by line
			currentDAGItem= self.DAG[i] 
			for j in range(0,len(currentDAGItem)):
				if currentDAGItem[j] != ' ':
					spaces = j #j increments until the j-th character in the i-th DAG line is not blank
					break
				elif j == len(currentDAGItem)-1:
					spaces = j+1 #handles the case where it goes all the way to the end of the line
			if spaces > 0 and spaces < self.spacesPerIndent:     
				self.spacesPerIndent = spaces #This keeps track of the smallest nonzero number of spaces at the beginning of a line 
			if spaces > maxSpaces:
				maxSpaces = spaces #Largest number of spaces at beginning of line 
		if self.spacesPerIndent == 999 and maxSpaces > 0 : #Minimum number of spaces at the beginning of an indented line does not have a value below 999
			print("Error processing Indentation/spaces in input file")  
		for i in range(0,len(self.DAG)): #Goes through DAG again line by line and assigns number of indents, since the previous loop found the number of spaces in one indent  
			currentDAGItem = self.DAG[i]
			for j in range(0,len(currentDAGItem)):
				if currentDAGItem[j] != ' ':
					numberOfSpaces = j
					break
				elif j == len(currentDAGItem)-1:
					numberOfSpaces = j+1
			if numberOfSpaces%self.spacesPerIndent == 0:
				self.dagIndentation.append(numberOfSpaces//self.spacesPerIndent) 
			else:
				print("WARNING: Input DAG file has improper or irregular spacing in line indentations")  
		self.dagItem = [] 
		self.dagFlows = []
		tupleNumbers = []
		lineBreakPoint = 0 
		mergeLine = False
		isDigitOrColon = []
		for i in range(0,len(self.DAG)):
			tupleNumbers = []  
			strippedDAGItem = self.DAG[i].strip()  
			mergeLine = False
			isDigitOrColon = []
			for j in range(0,len(strippedDAGItem)):
				isDigitOrColon.append(((strippedDAGItem[j]).isdigit()) or (strippedDAGItem[j] == ':'))
			for j in range(0,len(strippedDAGItem)):  
				if strippedDAGItem[j] == '(' or strippedDAGItem[j] == '[' or j == len(strippedDAGItem)-1:  
					lineBreakPoint = j
					break
			if len(strippedDAGItem) > 4:
				if strippedDAGItem[0:5] == 'merge':
					mergeLine = True
			if (not mergeLine):
				if lineBreakPoint < 1:
					print("WARNING: Operator and/or branch name(s) given as empty strings.")  
				self.dagItem.append(strippedDAGItem[0:lineBreakPoint])
				for k in range(lineBreakPoint,len(strippedDAGItem)-1):
					if (isDigitOrColon[k]) and (not (isDigitOrColon[k-1])):
						for l in range(k,len(strippedDAGItem)-1):
							if (not (isDigitOrColon[l+1])):
								tupleNumbers.append(strippedDAGItem[k:l+1])
								break
				self.dagFlows.append(tuple(tupleNumbers))
			else:
				self.dagItem.append(self.DAG[i].strip())  
				self.dagFlows.append(tuple())     


	def export(self,path): 
		file=open(path,'w+')
		spaceString = ''
		reconstitutedStrippedDAGItem = ''
		properStrippedDAGItem = ''
		DAGNameItem = ''
		for i in range(0,len(self.dagIndentation)):
			spaceString = ''  
			DAGNameItem = self.dagItem[i] + ' '
			if str(self.dagFlows[i]) != '()' or DAGNameItem[0] == '<':
				reconstitutedStrippedDAGItem = self.dagItem[i] + str(self.dagFlows[i])
			else:
				reconstitutedStrippedDAGItem = self.dagItem[i]  
			properStrippedDAGItem = ''
			for j in range(0,len(reconstitutedStrippedDAGItem)):
				if (reconstitutedStrippedDAGItem[j] != '\'') and ((reconstitutedStrippedDAGItem[j] != ' ') or j < len(self.dagItem[i])):
					properStrippedDAGItem = properStrippedDAGItem + (reconstitutedStrippedDAGItem[j])
			if DAGNameItem[0] == '<':
				properStrippedDAGItem = properStrippedDAGItem.replace(")","]") 
				properStrippedDAGItem = properStrippedDAGItem.replace("(","[") 
				properStrippedDAGItem = properStrippedDAGItem.replace(",","][") 
			for j in range(0,self.spacesPerIndent*self.dagIndentation[i]):
				spaceString = spaceString+' '
			file.write(spaceString+properStrippedDAGItem+'\n')
		file.close()


	def branchesInDAG(self): #returns name list
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
			if (self.dagItem[i]+' ')[0]=='<' or self.dagIndentation[i] != self.dagIndentation[i-1]:
				branchEnd=i
				print(branchEnd)
				break
		return branchEnd-branchStart-1


	def addOperator(self,branchName,operator,input,output,position): 
		branchStart = self.dagItem.index('<'+branchName)
				
		if self.operatorsInBranch(branchName)+1 < position:
			print("Position value too high for branch length")
		else:
			self.dagItem.insert(branchStart+position+1,operator)
			self.dagFlows.insert(branchStart+position+1,(input, output))
			self.dagIndentation.insert(branchStart+position+1,self.dagIndentation[branchStart]) 


	def removeOperator(self,operator,input,output,clear=True,duplicateIndex=0): #clear means remove empty branches
		#duplicateIndex behavior: for str input, generate ordered list of indices of operators with name (using for loop)
		#then use list[duplicateIndex] to select indice, then use that operator
		if type(operator)==int:
			operatorIndex = self.dagItem.index(str(operator)) 
			del self.dagItem [operatorIndex] 
			del self.dagFlows [operatorIndex]
			del self.dagIndentation [operatorIndex]      
				if clear and (self.dagItem[operatorIndex-1] + ' ')[0]=='<' and (self.dagItem[operatorIndex] + ' ')[0]=='<' :
					del self.dagItem [operatorIndex-1] 
					del self.dagFlows [operatorIndex-1]
					del self.dagIndentation [operatorIndex-1] 
		elif type(operator)==str:
			operatorIndex = self.dagItem.index(operator)
			del self.dagItem [operatorIndex] 
			del self.dagFlows [operatorIndex] 
			del self.dagIndentation [operatorIndex]
				if clear and (self.dagItem[operatorIndex-1] + ' ')[0]=='<' and (self.dagItem[operatorIndex] + ' ')[0]=='<' :
					del self.dagItem [operatorIndex-1] 
					del self.dagFlows [operatorIndex-1] 
					del self.dagIndentation [operatorIndex-1]          
		else:
			print("operator must be integer or string")  
			
	def addBranch(self, branch, tupleStrings, operator): #format tupleStrings like ('6:7','8:9')
		self.dagItem.insert(self.dagItem.index(operator)+1,'<'+branch)
		self.dagFlows.insert(self.dagItem.index(operator)+1,tuple(tupleStrings))
		self.dagIndentation.insert(self.dagItem.index(operator)+1,self.dagIndentation[self.dagItem.index(operator)]+1)    


	def removeBranch(self,branch,clear=False,mergeCheck = True): 
		mergeConflict = False
		if mergeCheck :
			for i in range(self.dagItem.index('<'+branch),len(self.dagItem)):
				if len(self.dagItem[i]) > 4 + len(branch):
					if self.dagItem[i][0:5] == 'merge':
						for j in range(0,(len(self.dagItem[i]) - len(branch) + 1)):  
							if branch == self.dagItem[i][j:j+len(branch)]:
								mergeConflict = True
								print("You are attempting to remove a branch which is later found in a merge. Operation canceled.")
		if( not mergeConflict):
			if (self.dagItem[self.dagItem.index('<'+branch)+1] + ' ')[0] == '<':
				del self.dagIndentation [self.dagItem.index('<'+branch)]
				del self.dagFlows [self.dagItem.index('<'+branch)]
				del self.dagItem [self.dagItem.index('<'+branch)]
			elif clear:
				branchIndex = self.dagItem.index('<'+branch)
				del self.dagItem[branchIndex]
				del self.dagFlows[branchIndex]
				del self.dagIndentation[branchIndex]
				while (self.dagItem[branchIndex] + ' ')[0] != '<':
					del self.dagItem[branchIndex]
					del self.dagFlows[branchIndex]
					del self.dagIndentation[branchIndex]
			else:
				print ("Branch not removed because it has one or more operators")


	def addMerge(self,mergeBranchList,destinationBranch): 
		branchPositions=[]
		mergePosition = len(self.dagItem)
		for i in range(0,len(mergeBranchList)):
			branchPositions.append(self.dagItem.index('<'+mergeBranchList[i])) #needs to be stripped to see if same
		lastBranchPosition = max(branchPositions)  
		for i in range(lastBranchPosition+1,len(self.dagItem)): #Starts after last branch is defined
			if (self.dagItem[i]+ ' ')[0] == '<':
				mergePosition = i #This is the next branch, which is not one of the branches being merged. Merge will be inserted just before this branch is defined
				break 
		print(mergePosition)
		print(lastBranchPosition)
		branchesToMerge = ''
		for i in range(0,len(mergeBranchList)):
			branchesToMerge = branchesToMerge + mergeBranchList[i] +', ' #Builds up list of branches to merge in DAGML format
		if mergePosition < len(self.dagItem):
			indentationOfMerge = max([self.dagIndentation[mergePosition]-1,0])
		else:
			indentationOfMerge = max([self.dagIndentation[mergePosition-1]-1,0])
		self.dagItem.insert(mergePosition,'merge('+branchesToMerge+destinationBranch+')') #inserts merge
		self.dagFlows.insert(mergePosition,tuple())
		self.dagIndentation.insert(mergePosition,indentationOfMerge)

	def removeMerge(self,mergeBranchList,destinationBranch):
		branchesToMerge = ''
		for i in range(0,len(mergeBranchList)):
			branchesToMerge = branchesToMerge + mergeBranchList[i] +', ' 
		del self.dagIndentation[self.dagItem.index('merge('+branchesToMerge+destinationBranch+')')]
		del self.dagItem[self.dagItem.index('merge('+branchesToMerge+destinationBranch+')')] #removes merge


	def editIO(self,operator, input,output, duplicateIndex=0): #operators
	    operatorIndex = self.dagItem.index(operator) #operator string must include arguments of pre-existing operator
	    del self.dagFlows[operatorIndex]
	    self.dagFlows.insert(operatorIndex,(input, output))    


	def editSlice(self,branch, tupleStrings, duplicateIndex=0):  #format tupleStrings like ('6:7','8:9')
	    branchIndex = self.dagItem.index('<'+branch) 
	    del self.dagFlows[branchIndex]
	    self.dagFlows.insert(branchIndex,tuple(tupleStrings))    