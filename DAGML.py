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
    for i in range(0,self.DAG.__len__):
      if self.DAG[i].strip()=='<'+str(branchNumber)+'>':
        branchStart=i
        break
    if operatorsInBranch(branchNumber)+1 < position:
      print("Position value too high for branch length") #change to try except later, add this check to linter
    else:
      branches.insert(branchStart+position,operator)
      break
        
  def editCut
  
  def removeOperator
  
  def addBranch
  
  def removeBranch
  
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
