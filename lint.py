def lint(dagIndents, indentSize, dagItem, dagFlows):
    if type(indentSize) != int:
        raise Exception ('Error: indentSize is not of type \'int\'.')
    if type(dagIndents) != list:
        raise Exception ('Error: dagIndents is not of type \'list\'.')
    if type(dagItem) != list:
        raise Exception ('Error: dagItem is not of type \'list\'.')
    if type(dagFlows) != list:
        raise Exception ('Error: dagFlows is not of type \'list\'.')
    spaceString = ''
    itemPlusFlow = ''
    itemAndFlow = ''
    dagNameItem = ''
    fileForm = list()
    pokay = False
    if (len(dagIndents) != len(dagItem)) or (len(dagIndents) != len(dagFlows)):
        raise Exception('Dag components must have equal numbers of lines.')
    pchar = 'x'
    for i in range(0, len(dagItem)):
        if type(dagIndents[i]) != int:
            raise Exception('Error: dagIndents element number '+str(i)+' is not of type \'int\'.') 
        if len(dagItem[i]) == 0:
            raise Exception(('Dag items may not be empty, and blank lines are forbidden. Error on line ' + str(i)))
        if dagItem[i][0] == ' ':
            raise Exception(('Dag items may not begin with a space. Error on line ' + str(i)))
        if dagItem[i][-1] == ' ':
            raise Exception(('Dag items may not end with a space. Error on line ' + str(i)))
        if str(dagFlows[i])[0] == ' ':
            raise Exception(('Dag flows may not begin with a space. Error on line ' + str(i)))
        if str(dagFlows[i])[-1] == ' ':
            raise Exception(('Dag flows may not end with a space. Error on line ' + str(i)))
        for j in range(0,len(dagFlows[i])-1):
            if dagFlows[i][j:j+2] == '::':
                raise Exception(('Dag flows may not have double or multiple colons. Error on line ' + str(i)))
        for j in range(0,len(dagItem[i])):
            pokay = False
            if len(dagItem[i]) > 6:
                if dagItem[i][0:5] == 'merge' and (j == 5 or j == len(dagItem[i]) - 1):                    
                    pokay = True
                    if j == 5:
                        pchar = '('
                    else:
                        pchar = ')'                            
            if (dagItem[i][j] == '(' or dagItem[i][j] == ')' or dagItem[i][j] == '[' or dagItem[i][j] == ']') and (not pokay):
                raise Exception(('Dag items may not contain parentheses or brackets. Error on line ' + str(i)))    
            elif (pokay and (pchar != dagItem[i][j])):
                raise Exception(('Missing or improper merge parentheses on line ' + str(i)))
    for i in range(0, len(dagIndents)):
        spaceString = ''
        dagNameItem = dagItem[i] + ' '
        if str(dagFlows[i]) != '()' or dagNameItem[0] == '<':
            itemPlusFlow = dagItem[i] + str(dagFlows[i])
        else:
            itemPlusFlow = dagItem[i]
        itemAndFlow = ''
        for j in range(0, len(itemPlusFlow)):
            if ((itemPlusFlow[j] != '\'') and ((itemPlusFlow[j] != ' ')
            or j < len(dagItem[i]))):
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
        for j in range(0, indentSize*dagIndents[i]):
            spaceString = spaceString+' '
        fileForm.append(spaceString+itemAndFlow)
        print(spaceString+itemAndFlow)
        print('Indicator number 1')
    '''
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
    '''
    #print(fileForm)
    newIndents = []
    dagLine = ''
    indentLength = 999
    spaceCount = int()
    spaces = int()
    maxSpaces = int()
    for i in range(0,len(fileForm)):
        for j in range(0,len(fileForm[i])):
            if fileForm[i][j] != ' ':
                spaces = j
                break
            elif j == len(fileForm[i])-1:
                spaces = j+1
        if spaces > 0 and spaces < indentLength:
            indentLength = spaces
        if spaces > maxSpaces:
            maxSpaces = spaces  # Largest space
    if indentLength == 999 and maxSpaces > 0:  # Spaces > 999
        raise Exception('Error involving indentation/spaces')
    for i in range(0, len(fileForm)):  # assigns number of indents in DAG
        dagLine = fileForm[i]
        for j in range(0, len(dagLine)):
            if dagLine[j] != ' ':
                spaceCount = j
                break
            elif j == len(dagLine)-1:
                spaceCount = j+1
        #print('testyng')
        if spaceCount % indentLength == 0:
            newIndents.append(spaceCount//indentLength)
            #print(spaceCount//indentLength)
        else:
            raise Exception('ERROR: improper line indentations')
    newItem = []
    newFlows = []
    newFlowItems = []
    itemEndChar = 0
    mergeLine = False
    digitOrColon = []
    #print(fileForm)
    commaPos = []
    commas = 0
    operFound = False
    for i in range(0, len(fileForm)):
        newFlowItems = []
        itemAndFlow = fileForm[i].strip()
        lineLength = len(itemAndFlow)
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
            newItem.append(itemAndFlow[0:itemEndChar])
            for k in range(itemEndChar, len(itemAndFlow)-1):
                if (digitOrColon[k]) and (not (digitOrColon[k-1])):
                    for l in range(k, len(itemAndFlow)-1):
                        if (not (digitOrColon[l+1])):
                            newFlowItems.append(itemAndFlow[k:l+1])
                            break
            #newFlows.append(tuple(newFlowItems))           
            
            if (itemAndFlow[itemEndChar:len(itemAndFlow)]).count('|') == 0:
                newFlows.append(tuple(newFlowItems))
            else:
                print(newFlowItems)
                literal = newFlowItems[0]
                newFlows.append((literal,tuple(newFlowItems[1:len(newFlowItems)])))
        
        else:
            newItem.append(fileForm[i].strip())
            newFlows.append(tuple())
            if lineLength > 7 and i > 0:
                mergeOpers = ', '+(itemAndFlow[6:lineLength-1])+','
                print(mergeOpers)
                commaPos = []
                for j in range(0,len(mergeOpers)-1):
                    if mergeOpers[j] == ',':
                        commaPos.append(j)
                print(commaPos)    
                finalComma = len(mergeOpers)-1
                print(finalComma)
                commas = len(commaPos)
                for j in range(0,commas):
                    charIndex = commaPos[j]
                    if j < (commas - 1):
                        nextComma = commaPos[j+1]
                    else:
                        nextComma = finalComma
                    if nextComma > (charIndex + 2):
                        operString = mergeOpers[charIndex+2:nextComma]
                    else:
                        raise Exception(('Invalid spacing between commas in merge on line '+str(i)))
                    operFound = False
                    for k in range(0,i):
                        if newItem[k] == ('<' + operString):
                            operFound = True
                    if (not operFound):
                        #print('Mark')
                        #print(newItem)
                        #print('Rogers')
                        raise Exception(('Error: operator \''+operString+'\' not found prior to being involved in a merge on line '+str(i)))
                print('End')
            else:
                raise Exception(('Error: Invalid or empty merge on line '+str(i)))
    if type (indentLength) != int:
        raise Exception ('Error: New indent length not of type \'int\'.')
    if type(newIndents) != list:
        raise Exception ('Error: newIndents is not of type \'list\'.')
    if type(newItem) != list:
        raise Exception ('Error: newItem is not of type \'list\'.')
    if type(newFlows) != list:
        raise Exception ('Error: newFlows is not of type \'list\'.')
    if indentLength != indentSize:
        raise Exception('Error: Incorrect new indent length.')
    if len(newIndents) != len(dagIndents):
        raise Exception('Error: Incorrect number of lines in newIndents.')
    if len(newItem) != len(dagItem):
        raise Exception('Error: Incorrect number of lines in newItem.')
    if len(newFlows) != len(dagFlows):
        raise Exception('Error: Incorrect number of lines in newFlows.')
    for i in range(0, len(newFlows)):       
        if newIndents[i] != dagIndents[i]:
            raise Exception(('Error: Incorrect new number of indents on line ' + str(i)))
        if newItem[i] != dagItem[i]:
            raise Exception(('Error: Incorrect new dag item on line ' + str(i)))
        if str(newFlows[i]) != str(dagFlows[i]):
            print(str(newFlows[i]))
            print(str(dagFlows[i]))
            raise Exception(('Error: Incorrect new dag flows on line ' + str(i)))
