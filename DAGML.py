class DAGML(object):
  
  def __init__(self, path):
    file=open(path,'r+')
    self.DAG=file.read().split('\n')
    file.close()
    
  def export(path):
    file=open(path,'w+')
    file.writelines(self.DAG)
    file.close()
    
  def addOperator(branchNumber,operator,position): #in progress
    # for i in range(0,self.DAG.__len__):
    #  if self.DAG[i].strip()=='<'+str(branchNumber)+'>':
    #    branchStart=i
    #    break
    
    branchStart = self.DAG.index('<'+str(branchNumber)+'>')
        
    if operatorsInBranch(branchNumber)+1 < position:
      print("Position value too high for branch length") #change to try except later, add this check to linter
    else:
      self.DAG.insert(branchStart+position,operator)
      break
        
  def editCut
  
  def removeOperator(operator,clear=True):
    opindex = self.DAG.index(operator)
    self.DAG.remove(opindex) #remove empty branch if applicable
    if clear and self.DAG[opindex-1].strip()[0]=='<' and self.DAG[opindex].strip()[0]=='<' :
      self.DAG.remove(opindex-1)
      
  
  def addBranch(Branch, operator):
    self.DAG.insert(self.DAG.index(operator)+1,'<'+Branch+'>')    
  
  def removeBranch(Branch,clear=False) #recomputing index is expensive, only do it once
    if self.DAG[self.DAG.index('<'+Branch+'>')+1].strip()[0] == '<':
      self.DAG.remove(self.DAG.index('<'+Branch+'>')) 
    elif clear:
      branchIndex = self.DAG.index('<'+Branch+'>')
      self.DAG.remove(branchIndex) 
      while self.DAG[branchIndex].strip()[0] != '<':
        self.DAG.remove(branchIndex)    
    else:
      print "Branch not removed because it has one or more operators"
      
  
  def addMerge(MergeBranchList)
    BranchPositions=[]
    for i in range(0,MergeBranchList.__len__):
      BranchPositions.append(self.DAG.index('<'+MergeBranchList[i]+'>')) #needs to be stripped to see if same
    FirstBranchPosition = min(BranchPositions)
    LastBranchPosition = max(BranchPositions)
    
    for i in range(FirstBranchPosition-1,-1,-1):
      if self.DAG[i].strip()[0] == '<'
        DestinationBranch = i
        break
    for i in range(LastBranchPosition+1,self.DAG.__len__):
      if self.DAG[i].strip()[0] == '<'
        MergePosition = i
        break 
    BranchesToMerge = ''
    for i in range(0,MergeBranchList.__len__):
      BranchesToMerge = BranchesToMerge + MergeBranchList[i] +', '
    self.DAG.insert(MergePosition,'merge('+BranchesToMerge+DestinationBranch+')')
    
  
  def removeMerge
  
  def branchesInDAG: #returns name list
    branches=[]
    for i in range(0,self.DAG.__len__):
      if self.DAG[i].strip()[0]=='<':
        branches.append(self.DAG[i].strip()[1:-2])
    return branches
  
  def operatorsInBranch(branch): #returns number, change to name list
    for i in range(0,self.DAG.__len__):
      if self.DAG[i].strip()=='<'+str(branch)+'>':
        branchStart=i
        break
    for i in range(branchStart,self.DAG.__len__):
      if self.DAG[i][0].strip()=='<':
        branchEnd=i
        break
    return branchEnd-branchStart-1
