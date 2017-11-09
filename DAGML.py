class Rake(object):
  def __init__(self, path):
    file=open(path,'r+')
    self.DAG=file.read().split('\n')
    file.close()
  def save(path):
    file=open(path,'w+')
    file.writelines(self.DAG)
    file.close()
  def addOperator(branchNumber,operator):
    self.DAG.find('<'+branchNumber+
                               
  def removeOperator
  def addBranch
  def removeBranch
  def addMerge
  def removeMerge
  def branchesInDAG: #return name list
    output=[]
    for i in range(0,self.DAG.__len__):
      if self.DAG[i][0]=='<':
      output.append(self.DAG[i][1])
    return output
  def operatorsInBranch
  def editCut
  
