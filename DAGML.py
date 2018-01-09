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
  
  def removeOperator(operator):
    self.DAG.remove(self.DAG.index(operator)) #remove empty branch if applicable
  
  def addBranch(Branch, operator):
    self.DAG.insert(self.DAG.index(operator)+1,'<'+Branch+'>')    
  
  def removeBranch(Branch)
    self.DAG.remove(self.DAG.index('<'+Branch+'>')) #merge down operators in branch
  
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
