class Rake(object):
  def __init__(self, path):
    file=open(path,'r+')
    self.DAG=file.read().split('\n)
    file.close()
  def save(path):
    file=open(path,'w+')
    file.writelines(self.DAG)
  def addOperator(branchNumber,operator):
    self.DAG.find('<'+branchNumber+
                               
  def removeOperator
  def addBranch
  def removeBranch
  def addMerge
  def removeMerge
  def branchesInDAG: #return name list
    return [i for i, x in enumerate(my_list) if x == "<"]
  def operatorsInBranch
  def editCut
  
