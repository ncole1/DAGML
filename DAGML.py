class DAG(object):
  
  def __init__(self, path,spacing=True):
    file=open(path,'r+')
    self.DAG=file.read().split('\n') 
    del self.DAG[-1] #import adds blank line at end
    file.close()
    self.IndentationOfDAG = [] #rename to indents
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
        self.IndentationOfDAG.append(numberOfSpaces//self.spacesPerIndent) 
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
      #self.strippedDAG.append(self.DAG[i].strip())    
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
  def export(self,path):
    file=open(path,'w+')
    SpaceString = ''
    reconstitutedStrippedDAGItem = ''
    properStrippedDAGItem = ''
    DAGNameItem = ''
    for i in range(0,len(self.IndentationOfDAG)):
      SpaceString = ''  
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
      for j in range(0,self.spacesPerIndent*self.IndentationOfDAG[i]):
        SpaceString = SpaceString+' '
      file.write(SpaceString+properStrippedDAGItem+'\n')
    file.close()
    
  def addOperator(self,branchName,operator,input,output,position): #in progress
    branchStart = self.DAGNames.index('<'+branchName)
        
    if self.operatorsInBranch(branchName)+1 < position:
      print("Position value too high for branch length") #change to try except later, add this check to linter
    else:
      self.DAGNames.insert(branchStart+position+1,operator)
      self.DAGTuples.insert(branchStart+position+1,(input, output))
      self.IndentationOfDAG.insert(branchStart+position+1,self.IndentationOfDAG[branchStart]) 
      
  #def editSlice(self): #branches

  def removeOperator(self,operator,input,output,clear=True,duplicateIndex=0): #clear means remove empty branches
    if type(operator)==int:
      operatorIndex = self.DAGNames.index(str(operator)) #what if you have two identical operators in the DAG?
      del self.DAGNames [operatorIndex] #remove empty branch if applicable
      del self.DAGTuples [operatorIndex]
      del self.IndentationOfDAG [operatorIndex]      
      if clear and (self.DAGNames[operatorIndex-1] + ' ')[0]=='<' and (self.DAGNames[operatorIndex] + ' ')[0]=='<' :
        del self.DAGNames [operatorIndex-1] #remove empty branch if applicable
        del self.DAGTuples [operatorIndex-1]
        del self.IndentationOfDAG [operatorIndex-1] 
    elif type(operator)==str:
      operatorIndex = self.DAGNames.index(operator)#what if you have two identical operators in the DAG?
      del self.DAGNames [operatorIndex] #remove empty branch if applicable
      del self.DAGTuples [operatorIndex] #remove empty branch if applicable
      del self.IndentationOfDAG [operatorIndex]
      if clear and (self.DAGNames[operatorIndex-1] + ' ')[0]=='<' and (self.DAGNames[operatorIndex] + ' ')[0]=='<' :
        del self.DAGNames [operatorIndex-1] #remove empty branch if applicable
        del self.DAGTuples [operatorIndex-1] #remove empty branch if applicable
        del self.IndentationOfDAG [operatorIndex-1]          
    else:
      print("operator must be integer or string")  
      
    #duplicateIndex behavior: for str input, generate ordered list of indices of operators with name (using for loop)
    #then use list[duplicateIndex] to select indice, then use that operator
        
  def addBranch(self, Branch, tupleStrings, operator): #format tupleStrings like ('6:7','8:9')
    self.DAGNames.insert(self.DAGNames.index(operator)+1,'<'+Branch)
    self.DAGTuples.insert(self.DAGNames.index(operator)+1,tuple(tupleStrings))
    self.IndentationOfDAG.insert(self.DAGNames.index(operator)+1,self.IndentationOfDAG[self.DAGNames.index(operator)]+1)    
  def removeBranch(self,Branch,clear=False,mergeCheck = True): #recomputing index is expensive, only do it once
    mergeConflict = False
    if mergeCheck :
      for i in range(self.DAGNames.index('<'+Branch),len(self.DAGNames)):
        if len(self.DAGNames[i]) > 4 + len(Branch):
          if self.DAGNames[i][0:5] == 'merge':
            for j in range(0,(len(self.DAGNames[i]) - len(Branch) + 1)):  
              if Branch == self.DAGNames[i][j:j+len(Branch)]:
                mergeConflict = True
                print("You are attempting to remove a branch which is later found in a merge. Operation canceled.")
    if( not mergeConflict):
      if (self.DAGNames[self.DAGNames.index('<'+Branch)+1] + ' ')[0] == '<':
        del self.IndentationOfDAG [self.DAGNames.index('<'+Branch)]
        del self.DAGTuples [self.DAGNames.index('<'+Branch)]
        del self.DAGNames [self.DAGNames.index('<'+Branch)]
      elif clear:
        branchIndex = self.DAGNames.index('<'+Branch)
        del self.DAGNames[branchIndex]
        del self.DAGTuples[branchIndex]
        del self.IndentationOfDAG[branchIndex]
        while (self.DAGNames[branchIndex] + ' ')[0] != '<':
          del self.DAGNames[branchIndex]
          del self.DAGTuples[branchIndex]
          del self.IndentationOfDAG[branchIndex]
      else:
        print ("Branch not removed because it has one or more operators")
      
  
  def addMerge(self,MergeBranchList,DestinationBranch): # needs a lot of work!!!
    BranchPositions=[]
    MergePosition = len(self.DAGNames)
    for i in range(0,len(MergeBranchList)):
      BranchPositions.append(self.DAGNames.index('<'+MergeBranchList[i])) #needs to be stripped to see if same
    LastBranchPosition = max(BranchPositions)  
    for i in range(LastBranchPosition+1,len(self.DAGNames)): #Starts after last branch is defined
      if (self.DAGNames[i]+ ' ')[0] == '<':
        MergePosition = i #This is the next branch, which is not one of the branches being merged. Merge will be inserted just before this branch is defined
        break 
    print(MergePosition)
    print(LastBranchPosition)
    BranchesToMerge = ''
    for i in range(0,len(MergeBranchList)):
      BranchesToMerge = BranchesToMerge + MergeBranchList[i] +', ' #Builds up list of branches to merge in DAGML format
    if MergePosition < len(self.DAGNames):
      indentationOfMerge = max([self.IndentationOfDAG[MergePosition]-1,0])
    else:
      indentationOfMerge = max([self.IndentationOfDAG[MergePosition-1]-1,0])
    self.DAGNames.insert(MergePosition,'merge('+BranchesToMerge+DestinationBranch+')') #inserts merge
    self.DAGTuples.insert(MergePosition,tuple())
    self.IndentationOfDAG.insert(MergePosition,indentationOfMerge)
  
  def removeMerge(self,MergeBranchList,DestinationBranch):
    BranchesToMerge = ''
    for i in range(0,len(MergeBranchList)):
      BranchesToMerge = BranchesToMerge + MergeBranchList[i] +', ' #Builds up list of branches to merge in DAGML format
    del self.IndentationOfDAG[self.DAGNames.index('merge('+BranchesToMerge+DestinationBranch+')')]
    del self.DAGNames[self.DAGNames.index('merge('+BranchesToMerge+DestinationBranch+')')] #removes merge
    
    
  
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
      if (self.DAGNames[i]+' ')[0]=='<' or self.IndentationOfDAG[i] != self.IndentationOfDAG[i-1]:
        branchEnd=i
        print(branchEnd)
        break
    return branchEnd-branchStart-1
