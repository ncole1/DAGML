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
    for i in range(0,len(self.DAG)): #Goes through DAG again line by line and assigns number of indents, since the previous loop found the number of spaces in one indent to 
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
      
    self.strippedDAG = [] #should be strippedDAG
    for i in range(0,len(self.DAG)):
      self.strippedDAG.append(self.DAG[i].strip())     
    self.lint()
  def lint(self)
    #code
  def editIO(self,operator, input,output, duplicateIndex=0): #operators
    operatorIndex = self.strippedDAG.index(operator) #operator string must include arguments of pre-existing operator
    newOperator = ''
    update = 0
    for j in range(len(operator)-2,-1,-1):
      if operator[j] == '(':
        newOperator = operator[0:j] + '(' + input + ',' + output + ')'
        update = 1
        break
    if update == 1:
      del self.strippedDAG[operatorIndex]
      self.strippedDAG.insert(operatorIndex,newOperator)    
    else:
      print("Open parenthesis not found in operator string")
    #Duplicates not accounted for  
  def export(self,path):
    file=open(path,'w+')
    SpaceString = ''
    for i in range(0,len(self.IndentationOfDAG)):
      SpaceString = ''  
      for j in range(0,self.spacesPerIndent*self.IndentationOfDAG[i]):
        SpaceString = SpaceString+' '
      file.write(SpaceString+self.strippedDAG[i]+'\n')
    file.close()
    
  def addOperator(self,branchName,operator,position): #in progress
    # for i in range(0ipyth,len(self.DAG)):
    #  if self.DAG[i].strip()=='<'+str(branchNumber)+'>':
    #    branchStart=i
    #    break
    
    branchStart = self.strippedDAG.index('<'+branchName+'>')
        
    if self.operatorsInBranch(branchName)+1 < position:
      print("Position value too high for branch length") #change to try except later, add this check to linter
    else:
      self.strippedDAG.insert(branchStart+position+1,operator)
      self.IndentationOfDAG.insert(branchStart+position+1,self.IndentationOfDAG[branchStart]) 
      
  def editSlice(self,brancStart,newSlice): #branches
    #change branch at branchStart to have slice newSlice

  def removeOperator(self,operator,clear=True,duplicateIndex=0): #clear means remove empty branches
    if type(operator)==int:
      operatorIndex = self.strippedDAG.index(str(operator)) #what if you have two identical operators in the DAG?
      self.strippedDAG.remove(str(operator)) #remove empty branch if applicable
      self.IndentationOfDAG.remove(self.IndentationOfDAG[operatorIndex])
      if clear and self.strippedDAG[operatorIndex-1][0]=='<' and self.strippedDAG[operatorIndex][0]=='<' :
        self.strippedDAG.remove(operatorIndex-1)
        self.IndentationOfDAG.remove(operatorIndex-1) 
    elif type(operator)==str:
      operatorIndex = self.strippedDAG.index(operator) #what if you have two identical operators in the DAG?
      self.strippedDAG.remove(operator) #remove empty branch if applicable
      self.IndentationOfDAG.remove(self.IndentationOfDAG[operatorIndex])
      if clear and self.strippedDAG[operatorIndex-1][0]=='<' and self.strippedDAG[operatorIndex][0]=='<' :
        self.strippedDAG.remove(operatorIndex-1)
        self.IndentationOfDAG.remove(operatorIndex-1)          
    else:
      print("operator must be integer or string")  
      
    #duplicateIndex behavior: for str input, generate ordered list of indices of operators with name (using for loop)
    #then use list[duplicateIndex] to select indice, then use that operator
        
  def addBranch(self, Branch, operator):
    self.strippedDAG.insert(self.strippedDAG.index(operator)+1,'<'+Branch+'>')
    self.IndentationOfDAG.insert(self.strippedDAG.index(operator)+1,self.IndentationOfDAG[self.strippedDAG.index(operator)]+1)    
  
  def removeBranch(self,Branch,clear=False): #recomputing index is expensive, only do it once
    if self.strippedDAG[self.strippedDAG.index('<'+Branch+'>')+1][0] == '<':
      del self.IndentationOfDAG [self.strippedDAG.index('<'+Branch+'>')]
      del self.strippedDAG [self.strippedDAG.index('<'+Branch+'>')]
    elif clear:
      branchIndex = self.strippedDAG.index('<'+Branch+'>')
      del self.strippedDAG[branchIndex] 
      del self.IndentationOfDAG[branchIndex]
      while self.strippedDAG[branchIndex][0] != '<':
        del self.strippedDAG[branchIndex] 
        del self.IndentationOfDAG[branchIndex]
    else:
      print ("Branch not removed because it has one or more operators")
      
  
  def addMerge(self,MergeBranchList,DestinationBranch): # needs a lot of work!!!
    BranchPositions=[]
    MergePosition = len(self.strippedDAG)
    for i in range(0,len(MergeBranchList)):
      BranchPositions.append(self.strippedDAG.index('<'+MergeBranchList[i]+'>')) #needs to be stripped to see if same
    LastBranchPosition = max(BranchPositions)  
    for i in range(LastBranchPosition+1,len(self.strippedDAG)): #Starts after last branch is defined
      if self.strippedDAG[i][0] == '<':
        MergePosition = i #This is the next branch, which is not one of the branches being merged. Merge will be inserted just before this branch is defined
        break 
    print(MergePosition)
    print(LastBranchPosition)
    BranchesToMerge = ''
    for i in range(0,len(MergeBranchList)):
      BranchesToMerge = BranchesToMerge + MergeBranchList[i] +', ' #Builds up list of branches to merge in DAGML format
    if MergePosition < len(self.strippedDAG):
      indentationOfMerge = max([self.IndentationOfDAG[MergePosition]-1,0])
    else:
      indentationOfMerge = max([self.IndentationOfDAG[MergePosition-1]-1,0])
    self.strippedDAG.insert(MergePosition,'merge('+BranchesToMerge+DestinationBranch+')') #inserts merge
    self.IndentationOfDAG.insert(MergePosition,indentationOfMerge)
  
  def removeMerge(self,MergeBranchList,DestinationBranch):
    BranchesToMerge = ''
    for i in range(0,len(MergeBranchList)):
      BranchesToMerge = BranchesToMerge + MergeBranchList[i] +', ' #Builds up list of branches to merge in DAGML format
    del self.IndentationOfDAG[self.strippedDAG.index('merge('+BranchesToMerge+DestinationBranch+')')]
    del self.strippedDAG[self.strippedDAG.index('merge('+BranchesToMerge+DestinationBranch+')')] #removes merge
    
    
  
  def branchesInDAG(self): #returns name list
    branches=[]

    for i in range(0,len(self.strippedDAG)):
      if self.strippedDAG[i][0]=='<':
        branches.append(self.strippedDAG[i][1:-1])
    return branches
  
  def operatorsInBranch(self,branch): #returns number, change to name list
    #print self.IndentationOfDAG
    branchStart=int()
    branchEnd=int()
    for i in range(0,len(self.strippedDAG)):
      if self.strippedDAG[i] =='<'+str(branch)+'>':
        branchStart=i
        print(str(branchStart)+'_')
        break
    for i in range(branchStart+1,len(self.strippedDAG)):
      if self.strippedDAG[i][0]=='<' or self.IndentationOfDAG[i] != self.IndentationOfDAG[i-1]:
        branchEnd=i
        print(branchEnd)
        break
    return branchEnd-branchStart-1
