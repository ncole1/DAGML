#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 15:28:21 2018

@author: nightvid
"""
import csv
class DAG(object):
    def optimizer(dagIndents, indentSize, dagItem, dagFlows, zeroOneList, moreOpt):
        delLines = []
        zeroLines = []
        brEnd = 0
        operMode = ' '
        operator = ''
        minLiteral = float(0)
        maxLiteral = float(0)
        failureMode = ''
        dagLiteral = ''
        operMode = ''
        delIndex = 0
        zeroIndex = 0
        branchHeads = []
        brLine = 0
        brEnd = 0
        beginGroup = 0
        litSum = 0
        litProd = 1
        maxj = 0
        with open('Book1.csv',newline='\n') as file:
            lines = csv.reader(file,delimiter=',')
            for dagLine in range(0,len(dagItem)):
                zeroLines.append(False)
            for line in lines:
                print(line)
                operator = line[0]
                minLiteral = float(line[1])
                maxLiteral = float(line[2])
                failureMode = line[3]
                for dagLine in range(0,len(dagItem)):
                    if len(dagFlows[dagLine]) > 0:
                        dagLiteral = dagFlows[dagLine][0]
                        if operator == dagItem[dagLine] and dagLiteral > minLiteral and dagLiteral < maxLiteral:
                            print(failureMode + ' on DAG line ' + str(dagLine))
                            operMode = failureMode
                        else:
                            operMode = ' '
                    else:
                        operMode = ' '
                    if operMode == 'addZero' or operMode == 'multiplyOne':
                        delLines.append(dagLine)
                    if operMode == 'multiplyZero':
                        zeroLines[dagLine] = True
            for j in range(len(delLines)-1,-1,-1):
                delIndex = delLines[j]
                del dagIndents[delIndex]
                del dagItem[delIndex]
                del dagFlows[delIndex]
                del zeroLines[delIndex]
            for z in range(len(zeroLines)-1,-1,-1):
                zeroIndex = zeroLines[z]
                dagItem[zeroIndex] = 'zero'
            branchHeads = []
            for dagLine in range(0,len(dagItem)):
                if dagItem[dagLine][0] == '<':
                    branchHeads.append(dagLine)
            for branchNum in range(len(branchHeads)-1,-1,-1):
                brLine = branchHeads[branchNum]
                if brLine+1 < len(dagItem):
                    for operLine in range(brLine+1,len(dagItem)):
                        brEnd = operLine
                        if dagItem[operLine][0] == '<' or dagIndents[operLine] != dagIndents[operLine - 1]:
                            brEnd = operLine - 1
                            break
                        if len(dagItem[operLine]) > 4:
                            if dagItem[operLine][0:5] == 'merge':
                                brEnd = operLine - 1
                                break
                else:
                    brEnd = len(dagItem) - 1
                for dagLine in range(brEnd,brLine,-1):
                    if dagItem[dagLine] == 'zero':
                        dagItem[dagLine] = '<zero'
                        for n in range(brLine, dagLine):
                            dagItem[n] = 'null'
                        break
            maxj = len(dagItem) - 1
            for j in range(maxj,-1,-1):
                if dagItem[j] == 'null':
                    del dagIndents[j]
                    del dagItem[j]
                    del dagFlows[j]            
            for dagLine in range(1,len(dagItem)):
                if dagItem[dagLine] == 'add' and dagItem[dagLine - 1] == 'add':
                    for startGroup in range (dagLine-1, -1, -1):
                        if dagItem[startGroup] != 'add' or dagIndents[startGroup] != dagIndents[dagLine] or dagItem[startGroup+1][0] == '<':
                            beginGroup = startGroup+1
                            break
                    litSum = 0
                    if beginGroup < dagLine:
                        for sumLine in range(beginGroup,dagLine+1):
                            litSum = litSum + dagFlows[sumLine][0]
                        dagFlows[dagLine][0] = litSum
                        for n in range(beginGroup,dagLine):
                            dagItem[n] = 'null'                        
            maxj = len(dagItem) - 1
            for j in range(maxj,-1,-1):
                if dagItem[j] == 'null':
                    del dagIndents[j]
                    del dagItem[j]
                    del dagFlows[j]
            for dagLine in range(1,len(dagItem)):
                if dagItem[dagLine] == 'multiply' and dagItem[dagLine - 1] == 'multiply':
                    for startGroup in range (dagLine-1, -1, -1):
                        if dagItem[startGroup] != 'multiply' or dagIndents[startGroup] != dagIndents[dagLine] or dagItem[startGroup+1][0] == '<':
                            beginGroup = startGroup+1
                            break
                    litProd = 1
                    if beginGroup < dagLine:
                        for prodLine in range(beginGroup,dagLine+1):
                            litProd = litProd * dagFlows[prodLine][0]
                        dagFlows[dagLine][0] = litProd                    
                        for n in range(beginGroup,dagLine):
                            dagItem[n] = 'null' 
            maxj = len(dagItem) - 1
            for j in range(maxj,-1,-1):
                if dagItem[j] == 'null':
                    del dagIndents[j]
                    del dagItem[j]
                    del dagFlows[j]
            newIndents = dagIndents
            newItem = dagItem
            newFlows = dagFlows
        return(newIndents,newItem,newFlows)
        
        
        
