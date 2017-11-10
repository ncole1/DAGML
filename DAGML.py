class Rake(object):
  
  def __init__(self, path):
    file=open(path,'r+')
    self.DAG=file.read().split('\n')
    file.close()
    
  def save(path):
    file=open(path,'w+')
    file.writelines(self.DAG)
    file.close()
    
  def addOperator(branchNumber,operator): #in progress
    for i in range(0,self.DAG.__len__):
      if self.DAG[i][0].strip()=='<'+str(branch):
        branchStart=i
        break
        
  def editCut
  
  def removeOperator
  
  def addBranch
  
  def removeBranch
  
  def addMerge
  
  def removeMerge
  
  def branchesInDAG: #return name list
    branches=[]
    for i in range(0,self.DAG.__len__):
      if self.DAG[i][0].strip()=='<':
        branches.append(self.DAG[i][1])
    return branches
  
  def operatorsInBranch(branch):
    for i in range(0,self.DAG.__len__):
      if self.DAG[i][0].strip()=='<'+str(branch):
        branchStart=i
        break
    for i in range(branchStart,self.DAG.__len__):
      if self.DAG[i][0].strip()=='<':
        branchEnd=i
        break
    return branchEnd-branchStart-1
