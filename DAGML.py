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
    for i in range(0,len(self.DAG)):
      currentDAGItem= self.DAG[i] 
      for j in range(0,len(currentDAGItem)):
        if currentDAGItem[j] != ' ':
          spaces = j
          break
        elif j == len(currentDAGItem)-1:
          spaces = j+1
      if spaces > 0 and spaces < self.spacesPerIndent:     
        self.spacesPerIndent = spaces  
      if spaces > maxSpaces:
        maxSpaces = spaces  
    if self.spacesPerIndent == 999 and maxSpaces > 0 : #Minimum number of spaces at the beginning of an indented line does not have a value below 999
      print("Error processing Indentation/spaces in input file")  
    for i in range(0,len(self.DAG)):
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
 
  def export(self,path):
    file=open(path,'w+')
    SpaceString = ''
    for i in range(0,len(self.IndentationOfDAG)):
      SpaceString = ''  
      for j in range(0,self.spacesPerIndent*self.IndentationOfDAG[i]):
        SpaceString = SpaceString+' '
      file.write(SpaceString+self.strippedDAG[i]+'\n')
    file.close()
    
  def addOperator(self,branchName,operator,position, NumberOfSpacesInIndent): #in progress
    # for i in range(0ipyth,len(self.DAG)):
    #  if self.DAG[i].strip()=='<'+str(branchNumber)+'>':
    #    branchStart=i
    #    break
    
    branchStart = self.strippedDAG.index('<'+branchName+'>')
        
    if self.operatorsInBranch(branchName,NumberOfSpacesInIndent)+1 < position:
      print("Position value too high for branch length") #change to try except later, add this check to linter
    else:
      self.strippedDAG.insert(branchStart+position+1,operator)
      self.IndentationOfDAG.insert(branchStart+position+1,self.IndentationOfDAG[branchStart]) 
      
        
  #def editCut
  
  def removeOperator(self,operator,clear=True,duplicateIndex=0): #clarify what clear does
    if type(operator)==int:
      operatorIndex = self.strippedDAG.index(str(operator)) #what if you have two identical operators in the DAG?
      self.strippedDAG.remove(str(operator)) #remove empty branch if applicable
      self.IndentationOfDAG.remove(self.IndentationOfDAG(operatorIndex))
      if clear and self.strippedDAG[operatorIndex-1][0]=='<' and self.strippedDAG[operatorIndex][0]=='<' :
        self.strippedDAG.remove(operatorIndex-1)
        self.IndentationOfDAG.remove(operatorIndex-1) 
    elif type(operator)==str:
      operatorIndex = self.strippedDAG.index(operator) #what if you have two identical operators in the DAG?
      self.strippedDAG.remove(operator) #remove empty branch if applicable
      self.IndentationOfDAG.remove(self.IndentationOfDAG(operatorIndex))
      if clear and self.strippedDAG[operatorIndex-1][0]=='<' and self.strippedDAG[operatorIndex][0]=='<' :
        self.strippedDAG.remove(operatorIndex-1)
        self.IndentationOfDAG.remove(operatorIndex-1)          
    else:
      print("operator must be integer or string")  
      
    #duplicateIndex behavior: for str input, generate ordered list of indices of operators with name (using for loop)
    #then use list[duplicateIndex] to select indice, then use that operator
        
  
  def addBranch(self, Branch, operator):
    self.strippedDAG.insert(self.strippedDAG.index(operator)+1,'<'+Branch+'>')
    self.IndentationOfDAG.insert(self.strippedDAG.index(operator)+1,self.IndentationOfDAG(self.strippedDAG.index(operator)))    
  
  def removeBranch(self,Branch,clear=False): #recomputing index is expensive, only do it once
    if self.strippedDAG[self.strippedDAG.index('<'+Branch+'>')+1][0] == '<':
      self.strippedDAG.remove(self.strippedDAG.index('<'+Branch+'>')) 
      self.IndentationOfDAG.remove(self.strippedDAG.index('<'+Branch+'>'))
    elif clear:
      branchIndex = self.strippedDAG.index('<'+Branch+'>')
      self.strippedDAG.remove(branchIndex) 
      self.IndentationOfDAG.remove(branchIndex)
      while self.strippedDAG[branchIndex][0] != '<':
        self.strippedDAG.remove(branchIndex)    
        self.IndentationOfDAG.remove(branchIndex)
    else:
      print ("Branch not removed because it has one or more opderators")
      
  
  def addMerge(self,MergeBranchList,DestinationBranch): # needs a lot of work!!!
    BranchPositions=[]
    for i in range(0,len(MergeBranchList)):
      BranchPositions.append(self.strippedDAG.index('<'+MergeBranchList[i]+'>')) #needs to be stripped to see if same
    LastBranchPosition = max(BranchPositions)  
    for i in range(LastBranchPosition+1,len(self.strippedDAG)): #Starts after last branch is defined
      if self.strippedDAG[i][0] == '<':
        MergePosition = i #This is the next branch, which is not one of the branches being merged. Merge will be inserted just before this branch is defined
        break 
    BranchesToMerge = ''
    for i in range(0,len(MergeBranchList)):
      BranchesToMerge = BranchesToMerge + MergeBranchList[i] +', ' #Builds up list of branches to merge in DAGML format
    indentationOfMerge = self.IndentationOfDAG(MergePosition)
    self.strippedDAG.insert(MergePosition,'merge('+BranchesToMerge+DestinationBranch+')') #inserts merge
    self.IndentationOfDAG.insert(MergePosition,indentationOfMerge)
  
  def removeMerge(self,MergeBranchList,DestinationBranch, MergePosition):
    BranchesToMerge = []
    for i in range(0,len(MergeBranchList)):
      BranchesToMerge = BranchesToMerge + MergeBranchList[i] +', ' #Builds up list of branches to merge in DAGML format
    self.strippedDAG.remove(self.strippedDAG.index(MergePosition,'merge('+BranchesToMerge+DestinationBranch+')')) #removes merge
    self.IndentationofDAG.remove(self.strippedDAG.index(MergePosition,'merge('+BranchesToMerge+DestinationBranch+')'))
    
  
  def branchesInDAG(self): #returns name list
    branches=[]

    for i in range(0,len(self.strippedDAG)):
      if self.strippedDAG[i][0]=='<':
        branches.append(self.strippedDAG[i][1:-2])
    return branches
  
  def operatorsInBranch(self,branch,NumberOfSpacesInIndent): #returns number, change to name list
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
