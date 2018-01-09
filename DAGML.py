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
  
  def removeBranch(Branch,clear=False)
    if self.DAG[self.DAG.index('<'+Branch+'>')+1].strip()[0] == '<':
      self.DAG.remove(self.DAG.index('<'+Branch+'>')) 
    elif clear:
      brindex = self.DAG.index('<'+Branch+'>')
      self.DAG.remove(brindex) 
      while self.DAG[brindex].strip()[0] <> '<':
        self.DAG.remove(brindex)    
    else:
      print "Branch not removed because it has one or more operators"
      
  
  def addMerge
    
  
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
