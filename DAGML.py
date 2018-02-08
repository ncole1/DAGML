class DAG(object):
	

	def __init__(self, path,spacing=True):
		file=open(path,'r+')
		self.DAG=file.read().split('\n') 
		del self.DAG[-1] #import adds blank line at end
		file.close()
		self.indentationOfDAG = [] #rename to indents
		currentDAGItem= ''
		numberOfSpaces = int() #rename to something better
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
				self.indentationOfDAG.append(numberOfSpaces//self.spacesPerIndent) 
			else:
				print("WARNING: Input DAG file has improper or irregular spacing in line indentations")  
		self.DAGNames = [] #should be strippedDAG
		self.DAGTuples = []
		#self.strippedDAG = []
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
				self.DAGNames.append(strippedDAGItem[0:lineBreakPoint])
				for k in range(lineBreakPoint,len(strippedDAGItem)-1):
					if (isDigitOrColon[k]) and (not (isDigitOrColon[k-1])):
						for l in range(k,len(strippedDAGItem)-1):
							if (not (isDigitOrColon[l+1])):
								tupleNumbers.append(strippedDAGItem[k:l+1])
								break
				self.DAGTuples.append(tuple(tupleNumbers))
			else:
				self.DAGNames.append(self.DAG[i].strip())  
				self.DAGTuples.append(tuple())     


	def export(self,path):
		file=open(path,'w+')
		spaceString = ''
		reconstitutedStrippedDAGItem = ''
		properStrippedDAGItem = ''
		DAGNameItem = ''
		for i in range(0,len(self.indentationOfDAG)):
			spaceString = ''  
			DAGNameItem = self.DAGNames[i] + ' '
			if str(self.DAGTuples[i]) != '()' or DAGNameItem[0] == '<':
				reconstitutedStrippedDAGItem = self.DAGNames[i] + str(self.DAGTuples[i])
			else:
				reconstitutedStrippedDAGItem = self.DAGNames[i]  
			properStrippedDAGItem = ''
			for j in range(0,len(reconstitutedStrippedDAGItem)):
				if (reconstitutedStrippedDAGItem[j] != '\'') and ((reconstitutedStrippedDAGItem[j] != ' ') or j < len(self.DAGNames[i])):
					properStrippedDAGItem = properStrippedDAGItem + (reconstitutedStrippedDAGItem[j])
			if DAGNameItem[0] == '<':
				properStrippedDAGItem = properStrippedDAGItem.replace(")","]") 
				properStrippedDAGItem = properStrippedDAGItem.replace("(","[") 
				properStrippedDAGItem = properStrippedDAGItem.replace(",","][") 
			for j in range(0,self.spacesPerIndent*self.indentationOfDAG[i]):
				spaceString = spaceString+' '
			file.write(spaceString+properStrippedDAGItem+'\n')
		file.close()


	def branchesInDAG(self): #returns name list
		branches=[]

		for i in range(0,len(self.DAGNames)):
			(self.DAGNames[i]+' ')[0]
			if (self.DAGNames[i]+' ')[0]=='<':
				branches.append(self.DAGNames[i][1:len(self.DAGNames[i])])
		return branches


	def operatorsInBranch(self,branch): #returns number, change to name list
		#print self.IndentationOfDAG
		branchStart=int()
		branchEnd=int()
		for i in range(0,len(self.DAGNames)):
			if self.DAGNames[i] =='<'+str(branch):
				branchStart=i
				print(str(branchStart)+'_')
				break
		for i in range(branchStart+1,len(self.DAGNames)):
			if (self.DAGNames[i]+' ')[0]=='<' or self.indentationOfDAG[i] != self.indentationOfDAG[i-1]:
				branchEnd=i
				print(branchEnd)
				break
		return branchEnd-branchStart-1


	def addOperator(self,branchName,operator,input,output,position): #in progress
		branchStart = self.DAGNames.index('<'+branchName)
				
		if self.operatorsInBranch(branchName)+1 < position:
			print("Position value too high for branch length") #change to try except later, add this check to linter
		else:
			self.DAGNames.insert(branchStart+position+1,operator)
			self.DAGTuples.insert(branchStart+position+1,(input, output))
			self.indentationOfDAG.insert(branchStart+position+1,self.indentationOfDAG[branchStart]) 


	def removeOperator(self,operator,input,output,clear=True,duplicateIndex=0): #clear means remove empty branches
		#duplicateIndex behavior: for str input, generate ordered list of indices of operators with name (using for loop)
		#then use list[duplicateIndex] to select indice, then use that operator
		if type(operator)==int:
			operatorIndex = self.DAGNames.index(str(operator)) #what if you have two identical operators in the DAG?
			del self.DAGNames [operatorIndex] #remove empty branch if applicable
			del self.DAGTuples [operatorIndex]
			del self.indentationOfDAG [operatorIndex]      
				if clear and (self.DAGNames[operatorIndex-1] + ' ')[0]=='<' and (self.DAGNames[operatorIndex] + ' ')[0]=='<' :
					del self.DAGNames [operatorIndex-1] #remove empty branch if applicable
					del self.DAGTuples [operatorIndex-1]
					del self.indentationOfDAG [operatorIndex-1] 
		elif type(operator)==str:
			operatorIndex = self.DAGNames.index(operator)#what if you have two identical operators in the DAG?
			del self.DAGNames [operatorIndex] #remove empty branch if applicable
			del self.DAGTuples [operatorIndex] #remove empty branch if applicable
			del self.indentationOfDAG [operatorIndex]
				if clear and (self.DAGNames[operatorIndex-1] + ' ')[0]=='<' and (self.DAGNames[operatorIndex] + ' ')[0]=='<' :
					del self.DAGNames [operatorIndex-1] #remove empty branch if applicable
					del self.DAGTuples [operatorIndex-1] #remove empty branch if applicable
					del self.indentationOfDAG [operatorIndex-1]          
		else:
			print("operator must be integer or string")  
			
	def addBranch(self, branch, tupleStrings, operator): #format tupleStrings like ('6:7','8:9')
		self.DAGNames.insert(self.DAGNames.index(operator)+1,'<'+branch)
		self.DAGTuples.insert(self.DAGNames.index(operator)+1,tuple(tupleStrings))
		self.indentationOfDAG.insert(self.DAGNames.index(operator)+1,self.indentationOfDAG[self.DAGNames.index(operator)]+1)    


	def removeBranch(self,branch,clear=False,mergeCheck = True): #recomputing index is expensive, only do it once
		mergeConflict = False
		if mergeCheck :
			for i in range(self.DAGNames.index('<'+branch),len(self.DAGNames)):
				if len(self.DAGNames[i]) > 4 + len(branch):
					if self.DAGNames[i][0:5] == 'merge':
						for j in range(0,(len(self.DAGNames[i]) - len(branch) + 1)):  
							if branch == self.DAGNames[i][j:j+len(branch)]:
								mergeConflict = True
								print("You are attempting to remove a branch which is later found in a merge. Operation canceled.")
		if( not mergeConflict):
			if (self.DAGNames[self.DAGNames.index('<'+branch)+1] + ' ')[0] == '<':
				del self.indentationOfDAG [self.DAGNames.index('<'+branch)]
				del self.DAGTuples [self.DAGNames.index('<'+branch)]
				del self.DAGNames [self.DAGNames.index('<'+branch)]
			elif clear:
				branchIndex = self.DAGNames.index('<'+branch)
				del self.DAGNames[branchIndex]
				del self.DAGTuples[branchIndex]
				del self.indentationOfDAG[branchIndex]
				while (self.DAGNames[branchIndex] + ' ')[0] != '<':
					del self.DAGNames[branchIndex]
					del self.DAGTuples[branchIndex]
					del self.indentationOfDAG[branchIndex]
			else:
				print ("Branch not removed because it has one or more operators")




	def addMerge(self,mergeBranchList,destinationBranch): # needs a lot of work!!!
		branchPositions=[]
		mergePosition = len(self.DAGNames)
		for i in range(0,len(mergeBranchList)):
			branchPositions.append(self.DAGNames.index('<'+mergeBranchList[i])) #needs to be stripped to see if same
		lastBranchPosition = max(branchPositions)  
		for i in range(lastBranchPosition+1,len(self.DAGNames)): #Starts after last branch is defined
			if (self.DAGNames[i]+ ' ')[0] == '<':
				mergePosition = i #This is the next branch, which is not one of the branches being merged. Merge will be inserted just before this branch is defined
				break 
		print(mergePosition)
		print(lastBranchPosition)
		branchesToMerge = ''
		for i in range(0,len(mergeBranchList)):
			branchesToMerge = branchesToMerge + mergeBranchList[i] +', ' #Builds up list of branches to merge in DAGML format
		if mergePosition < len(self.DAGNames):
			indentationOfMerge = max([self.indentationOfDAG[mergePosition]-1,0])
		else:
			indentationOfMerge = max([self.indentationOfDAG[mergePosition-1]-1,0])
		self.DAGNames.insert(mergePosition,'merge('+branchesToMerge+destinationBranch+')') #inserts merge
		self.DAGTuples.insert(mergePosition,tuple())
		self.indentationOfDAG.insert(mergePosition,indentationOfMerge)

	def removeMerge(self,mergeBranchList,destinationBranch):
		branchesToMerge = ''
		for i in range(0,len(mergeBranchList)):
			branchesToMerge = branchesToMerge + mergeBranchList[i] +', ' #Builds up list of branches to merge in DAGML format
		del self.indentationOfDAG[self.DAGNames.index('merge('+branchesToMerge+destinationBranch+')')]
		del self.DAGNames[self.DAGNames.index('merge('+branchesToMerge+destinationBranch+')')] #removes merge


	def editIO(self,operator, input,output, duplicateIndex=0): #operators
	    operatorIndex = self.DAGNames.index(operator) #operator string must include arguments of pre-existing operator
	    del self.DAGTuples[operatorIndex]
	    self.DAGTuples.insert(operatorIndex,(input, output))    
	    #Duplicates not accounted for  


	def editSlice(self,branch, tupleStrings, duplicateIndex=0):  #format tupleStrings like ('6:7','8:9')
	    branchIndex = self.DAGNames.index('<'+branch) 
	    del self.DAGTuples[branchIndex]
	    self.DAGTuples.insert(branchIndex,tuple(tupleStrings))    
	    #Duplicates not accounted for  