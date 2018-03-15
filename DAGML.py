from lint import lint

class DAG(object):

    def __init__(self, path, spacing=True):
        if type (path) != int:
            file = open(path, 'r+')
            self.DAG = file.read().split('\n')
            del self.DAG[-1]  # import adds blank line at end
            file.close()
        else:
            self.DAG = []
        self.dagIndents = []
        dagItem = ''
        spaceCount = int()
        spaces = int()
        maxSpaces = int()
        self.indentSize = 999
        for i in range(0, len(self.DAG)):  # goes through DAG line by line
            dagItem = self.DAG[i]
            for j in range(0, len(dagItem)):
                if dagItem[j] != ' ':
                    spaces = j
                    break
                elif j == len(dagItem)-1:
                    spaces = j+1
            if spaces > 0 and spaces < self.indentSize:
                self.indentSize = spaces  # smallest space
            if spaces > maxSpaces:
                maxSpaces = spaces  # Largest space
        if self.indentSize == 999 and maxSpaces > 0:  # Spaces > 999
            raise Exception('Import error involving indentation/spaces')
        for i in range(0, len(self.DAG)):  # assigns number of indents in DAG
            dagItem = self.DAG[i]
            for j in range(0, len(dagItem)):
                if dagItem[j] != ' ':
                    spaceCount = j
                    break
                elif j == len(dagItem)-1:
                    spaceCount = j+1
            if spaceCount % self.indentSize == 0:
                self.dagIndents.append(spaceCount//self.indentSize)
            else:
                raise Exception('WARNING: improper line indentations')
        self.dagItem = []
        self.dagFlows = []
        dagFlowItems = []
        itemEndChar = 0
        mergeLine = False
        digitOrColon = []
        for i in range(0, len(self.DAG)):
            dagFlowItems = []
            itemAndFlow = self.DAG[i].strip()
            mergeLine = False
            digitOrColon = []
            for j in range(0, len(itemAndFlow)):
                digitOrColon.append(((itemAndFlow[j]).isdigit())
                or (itemAndFlow[j] == ':'))
            for j in range(0, len(itemAndFlow)):
                if (itemAndFlow[j] == '(' or itemAndFlow[j] == '['
                or j == len(itemAndFlow)-1):
                    itemEndChar = j
                    break
            if len(itemAndFlow) > 4:
                if itemAndFlow[0:5] == 'merge':
                    mergeLine = True
            if (not mergeLine):
                if itemEndChar < 1:
                    raise Exception('Empty string is invalid assignment.')
                self.dagItem.append(itemAndFlow[0:itemEndChar])
                for k in range(itemEndChar, len(itemAndFlow)-1):
                    if (digitOrColon[k]) and (not (digitOrColon[k-1])):
                        for l in range(k, len(itemAndFlow)-1):
                            if (not (digitOrColon[l+1])):
                                dagFlowItems.append(itemAndFlow[k:l+1])
                                break
                if (itemAndFlow[itemEndChar:len(itemAndFlow)]).count('|') == 0:
                    self.dagFlows.append(tuple(dagFlowItems))
                else:
                    print(dagFlowItems)
                    literal = dagFlowItems[0]
                    self.dagFlows.append((literal,tuple(dagFlowItems[1:len(dagFlowItems)])))
            else:
                self.dagItem.append(self.DAG[i].strip())
                self.dagFlows.append(tuple())

    def export(self, path, spacing = True):
        if type(spacing) == int:
            self.indentSize = spacing
        file = open(path, 'w+')
        spaceString = ''
        itemPlusFlow = ''
        itemAndFlow = ''
        dagNameItem = ''
        for i in range(0, len(self.dagIndents)):
            spaceString = ''
            dagNameItem = self.dagItem[i] + ' '
            if str(self.dagFlows[i]) != '()' or dagNameItem[0] == '<':
                itemPlusFlow = self.dagItem[i] + str(self.dagFlows[i])
            else:
                itemPlusFlow = self.dagItem[i]
            itemAndFlow = ''
            for j in range(0, len(itemPlusFlow)):
                if ((itemPlusFlow[j] != '\'') and ((itemPlusFlow[j] != ' ')
                or j < len(self.dagItem[i]))):
                    itemAndFlow = itemAndFlow + (itemPlusFlow[j])                
            if dagNameItem[0] == '<':
                replaceCount = itemAndFlow.count(',(')
                itemAndFlow = itemAndFlow.replace(",(","|")
                itemAndFlow = itemAndFlow[0:len(itemAndFlow)-replaceCount]
                itemAndFlow = itemAndFlow.replace(")", "]")
                itemAndFlow = itemAndFlow.replace("(", "[")
                itemAndFlow = itemAndFlow.replace(",]","]")
                itemAndFlow = itemAndFlow.replace(",)",")")               
                itemAndFlow = itemAndFlow.replace(",", "][")
            else:
                replaceCount = itemAndFlow.count(',(')
                itemAndFlow = itemAndFlow.replace(",(","|")
                itemAndFlow = itemAndFlow[0:len(itemAndFlow)-replaceCount]
            for j in range(0, self.indentSize*self.dagIndents[i]):
                spaceString = spaceString+' '
            file.write(spaceString+itemAndFlow+'\n')
        file.close()

    def branchesInDag(self):  # returns name list
        branches = []

        for i in range(0, len(self.dagItem)):
            (self.dagItem[i] + ' ')[0]
            if (self.dagItem[i] + ' ')[0] == '<':
                branches.append(self.dagItem[i][1:len(self.dagItem[i])])
        return branches

    def operatorsInBranch(self, branch):
        branchStart = int()
        branchEnd = int()
        for i in range(0, len(self.dagItem)):
            if self.dagItem[i] == '<' + str(branch):
                branchStart = i
                print(str(branchStart) + '_')
                break
        for i in range(branchStart+1, len(self.dagItem)):
            if ((self.dagItem[i]+' ')[0] == '<'
            or self.dagIndents[i] != self.dagIndents[i-1]):
                branchEnd = i
                print(branchEnd)
                break
        return branchEnd-branchStart-1

    def addOperator(self, branchName, operator, input, output, position, literal=True):
        branchStart = self.dagItem.index('<'+branchName)
        if self.operatorsInBranch(branchName)+1 < position:
            raise Exception('Position value too high for branch length')
        else:
            place = branchStart+position+1
            self.dagItem.insert(place, operator)
            h = (input, output)
            if type(literal) != bool:
                self.dagFlows.insert(place, (literal,h))
            else:
                self.dagFlows.insert(place, h)
            self.dagIndents.insert(place, self.dagIndents[branchStart])

    def removeOperator(self, operator, input, output, clear=True, duplIndex=0):
        # clear means remove empty branches
        # duplIndex behavior: for str input, generate ordered list
        # of indices of operators with name (using for loop)
        # then use list[duplIndex] to select indice, then use that operator
        if type(operator) == int:
            operIndex = self.dagItem.index(str(operator))
            del self.dagItem[operIndex]
            del self.dagFlows[operIndex]
            del self.dagIndents[operIndex]
            if (clear and (self.dagItem[operIndex-1] + ' ')[0] == '<'
            and (self.dagItem[operIndex] + ' ')[0] == '<'):
                del self.dagItem[operIndex-1]
                del self.dagFlows[operIndex-1]
                del self.dagIndents[operIndex-1]
        elif type(operator) == str:
            operIndex = self.dagItem.index(operator)
            del self.dagItem[operIndex]
            del self.dagFlows[operIndex]
            del self.dagIndents[operIndex]
            if (clear and (self.dagItem[operIndex-1] + ' ')[0] == '<'
            and (self.dagItem[operIndex] + ' ')[0] == '<'):
                del self.dagItem[operIndex-1]
                del self.dagFlows[operIndex-1]
                del self.dagIndents[operIndex-1]
        else:
            raise Exception('operator must be integer or string')

    def addBranch(self, branch, tupleStrings, operator,duplIndex = 0, literal=True):
        # format tupleStrings like ('6:7','8:9')
        self.dagItem.insert(self.dagItem.index(operator)+1, '<'+branch)
        t = tuple(tupleStrings)
        if type(literal) != bool:
            self.dagFlows.insert(self.dagItem.index(operator)+1, (literal,t))
        else:
            self.dagFlows.insert(self.dagItem.index(operator)+1, t)
        indents = self.dagIndents[self.dagItem.index(operator)]+1
        self.dagIndents.insert(self.dagItem.index(operator)+1, indents)

    def removeBranch(self, branch, clear=False, mergeCheck=True):
        branchMerged = False
        if mergeCheck:
            for i in range(self.dagItem.index('<'+branch), len(self.dagItem)):
                if len(self.dagItem[i]) > 4 + len(branch):
                    if self.dagItem[i][0:5] == 'merge':
                        jmax = len(self.dagItem[i]) - len(branch) + 1
                        for j in range(0, jmax):
                            if branch == self.dagItem[i][j:j+len(branch)]:
                                branchMerged = True
                                raise Exception('Branch in merge.')
        if(not branchMerged):
            index = self.dagItem.index('<'+branch)+1
            if (self.dagItem[index] + ' ')[0] == '<':
                del self.dagIndents[self.dagItem.index('<'+branch)]
                del self.dagFlows[self.dagItem.index('<'+branch)]
                del self.dagItem[self.dagItem.index('<'+branch)]
            elif clear:
                branchIndex = self.dagItem.index('<'+branch)
                del self.dagItem[branchIndex]
                del self.dagFlows[branchIndex]
                del self.dagIndents[branchIndex]
                while (self.dagItem[branchIndex] + ' ')[0] != '<':
                    del self.dagItem[branchIndex]
                    del self.dagFlows[branchIndex]
                    del self.dagIndents[branchIndex]
            else:
                raise Exception('Branch has one or more operators')

    def addMerge(self, branchList, destination):
        branchPos = []
        mergePos = len(self.dagItem)
        for i in range(0, len(branchList)):
            branchPos.append(self.dagItem.index('<'+branchList[i]))
        maxBranchPos = max(branchPos)
        for i in range(maxBranchPos+1, len(self.dagItem)):
            # Starts after last branch is defined
            if (self.dagItem[i] + ' ')[0] == '<':
                mergePos = i
                # This is the next branch, which is not one of the branches
                # being merged. Merge will be inserted just before
                # this branch is defined
                break
        print(mergePos)
        print(maxBranchPos)
        toMerge = ''
        for i in range(0, len(branchList)):
            toMerge = toMerge + branchList[i] + ', '
            # Builds up list of branches to merge in DAGML format
        if mergePos < len(self.dagItem):
            indentationOfMerge = max([self.dagIndents[mergePos]-1, 0])
        else:
            indentationOfMerge = max([self.dagIndents[mergePos-1]-1, 0])
        self.dagItem.insert(mergePos, 'merge('+toMerge+destination+')')
        # inserts merge
        self.dagFlows.insert(mergePos, tuple())
        self.dagIndents.insert(mergePos, indentationOfMerge)

    def removeMerge(self, branchList, destination):
        toMerge = ''
        for i in range(0, len(branchList)):
            toMerge = toMerge + branchList[i] + ', '
        index = self.dagItem.index('merge('+toMerge+destination+')')
        del self.dagIndents[index]
        del self.dagItem[self.dagItem.index('merge('+toMerge+destination+')')]
        # removes merge
#____________________________________________________________________________________________(03/09/2018)
    def editIO(self, operator, input, output, duplIndex=0, literal = True, keepLiteral = False):  # operators
        operIndex = self.dagItem.index(operator)  # operator string
        # must include arguments of pre-existing operator
        if keepLiteral:            
            if len(self.dagFlows[operIndex]) > 0:
                literal = self.dagFlows[operIndex][0]
                if type(self.dagFlows[operIndex][1]) != tuple:
                    #print(self.dagFlows[operIndex][1])
                    raise Exception('Error: Missing or improper literal.')
            else:
                raise Exception('Error: operator literal is missing')
        del self.dagFlows[operIndex]
        if type(literal) != bool:
            self.dagFlows.insert(operIndex, (literal,(input, output)))
        else:
            self.dagFlows.insert(operIndex, (input, output))
            

    def editSlice(self, branch, tupleStrings, duplIndex=0, literal = True, keepLiteral = False):
        # format tupleStrings like ('6:7','8:9')
        branchIndex = self.dagItem.index('<'+branch)
        if keepLiteral:            
            if len(self.dagFlows[branchIndex]) > 0:
                literal = self.dagFlows[branchIndex][0]
                if type(self.dagFlows[branchIndex][1]) != tuple:
                    raise Exception('Error: Missing or improper literal.')
            else:
                raise Exception('Error: branch literal is missing')
        del self.dagFlows[branchIndex]
        if type(literal) != bool:
            self.dagFlows.insert(branchIndex, (literal, tuple(tupleStrings)))
        else:
            self.dagFlows.insert(branchIndex, tuple(tupleStrings))
        # Duplicates not accounted for
    def editBranchLiteral(self, branch, literal = True):
        branchIndex = self.dagItem.index('<'+branch)
        complex = False
        if len(self.dagFlows[branchIndex]) > 1:
            if type(self.dagFlows[branchIndex][1]) == tuple:
                complex = True    
        if complex:
            innerTuple = self.dagFlows[branchIndex][1]
        else:
            innerTuple = self.dagFlows[branchIndex]
        del self.dagFlows[branchIndex]
        if type(literal) != bool:
            self.dagFlows.insert(branchIndex, (literal, innerTuple))
        else:
            self.dagFlows.insert(branchIndex, innerTuple)
    def editOperatorLiteral(self, operator, literal = True):        
        operIndex = self.dagItem.index(operator)
        complex = False
        if len(self.dagFlows[operIndex]) > 1:
            if type(self.dagFlows[operIndex][1]) == tuple:
                complex = True    
        if complex:
            innerTuple = self.dagFlows[operIndex][1]
        else:
            innerTuple = self.dagFlows[operIndex]
        del self.dagFlows[operIndex]
        if type(literal) != bool:
            self.dagFlows.insert(operIndex, (literal, innerTuple))
        else:
            self.dagFlows.insert(operIndex, innerTuple)  
