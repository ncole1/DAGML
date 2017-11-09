class Rake(object):
  def __init__(self, path):
    file=open(path,'r+')
    self.DAG=file.read().split('\n)
    file.close()
  def save(path):
    file=open(path,'w+')
    file.writelines(self.DAG)
