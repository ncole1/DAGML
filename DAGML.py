class DAG(object):
  
  def __init__(self, path):
    file=open(path,'r+')
    self.DAG=file.read().split('\n')
    del self.DAG[-1] #import adds blank line at end
    file.close()
    
  def findIndex(self,name):
    StrippedDAG = []
    for i in range(0,len(self.DAG)):
      StrippedDAG.append(self.DAG[i].strip()) 
    index = StrippedDAG.index(name)
    return index

  def export(self,path):
    file=open(path,'w+')
    for i in range(0,len(self.DAG)):
      file.write(self.DAG[i]+'\n')
    file.close()
    
  def addOperator(self,branchNumber,operator,position): #in progress
    # for i in range(0ipyth,len(self.DAG)):
    #  if self.DAG[i].strip()=='<'+str(branchNumber)+'>':
    #    branchStart=i
    #    break
    
    branchStart = self.findIndex('<'+str(branchNumber)+'>')
        
    if self.operatorsInBranch(branchNumber)+1 < position:
      print("Position value too high for branch length") #change to try except later, add this check to linter
    else:
      self.DAG.insert(branchStart+position+1,operator)
      
        
  #def editCut
  
  def removeOperator(self,operator,clear=True):
    opindex = self.DAG.index(operator)
    self.DAG.remove(opindex) #remove empty branch if applicable
    if clear and self.DAG[opindex-1].strip()[0]=='<' and self.DAG[opindex].strip()[0]=='<' :
      self.DAG.remove(opindex-1)
      
  
  def addBranch(self, Branch, operator):
    self.DAG.insert(self.findIndex(operator)+1,'<'+Branch+'>')    
  
  def removeBranch(self,Branch,clear=False): #recomputing index is expensive, only do it once
    if self.DAG[self.DAG.index('<'+Branch+'>')+1].strip()[0] == '<':
      self.DAG.remove(self.DAG.index('<'+Branch+'>')) 
    elif clear:
      branchIndex = self.DAG.index('<'+Branch+'>')
      self.DAG.remove(branchIndex) 
      while self.DAG[branchIndex].strip()[0] != '<':
        self.DAG.remove(branchIndex)    
    else:
      print ("Branch not removed because it has one or more opderators")
      
  
  def addMerge(self,MergeBranchList,DestinationBranch): # needs a lot of work!!!
    BranchPositions=[]
    StrippedDAG = []
    for i in range(0,len(self.DAG)):
      StrippedDAG.append(self.DAG[i].strip()) # Builds up stripped DAG
    for i in range(0,len(MergeBranchList)):
      BranchPositions.append(StrippedDAG.index('<'+MergeBranchList[i]+'>')) #needs to be stripped to see if same
    LastBranchPosition = max(BranchPositions)  
    for i in range(LastBranchPosition+1,len(self.DAG)): #Starts after last branch is defined
      if self.DAG[i].strip()[0] == '<':
        MergePosition = i #This is the next branch, which is not one of the branches being merged. Merge will be inserted just before this branch is defined
        break 
    BranchesToMerge = ''
    for i in range(0,len(MergeBranchList)):
      BranchesToMerge = BranchesToMerge + MergeBranchList[i] +', ' #Builds up list of branches to merge in DAGML format
    self.DAG.insert(MergePosition,'merge('+BranchesToMerge+DestinationBranch+')') #inserts merge
    
  
  def removeMerge(self,MergeBranchList,DestinationBranch):
    for i in range(0,len(MergeBranchList)):
      BranchesToMerge = BranchesToMerge + MergeBranchList[i] +', ' #Builds up list of branches to merge in DAGML format
    self.DAG.remove(self.DAG.index(MergePosition,'merge('+BranchesToMerge+DestinationBranch+')')) #removes merge
    
    
  
  def branchesInDAG(self): #returns name list
    branches=[]
    for i in range(0,len(self.DAG)):
      if self.DAG[i].strip()[0]=='<':
        branches.append(self.DAG[i].strip()[1:-2])
    return branches
  
  def operatorsInBranch(self,branch): #returns number, change to name list
    for i in range(0,len(self.DAG)):
      if self.DAG[i].strip()=='<'+str(branch)+'>':
        branchStart=i
        break
    for i in range(branchStart,len(self.DAG)):
      if self.DAG[i][0].strip()=='<':
        branchEnd=i
        break
    return branchEnd-branchStart-1
