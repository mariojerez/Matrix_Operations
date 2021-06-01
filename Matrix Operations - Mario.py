## Mario Jerez 05/26/2020
## Multivariable Calculus
## Nick Rauh
##                           Matrix Operations Conference Project (first + second semester)

import math
from graphics import *

def scalar_vectorMult(scalar, vector):
    dimension = len(vector)
    result = []
    for i in range(dimension):
        result.append(scalar * vector[i])
    return result
        

def dotProduct(vector1, vector2):
    if len(vector1) != len(vector2):
        print("vectors must be equal dimension")
        return
    product = 0
    for i in range(len(vector1)):
        product = product + vector1[i] * vector2[i]
    return product

def vectorLength(vector):
    dotProd = dotProduct(vector, vector)
    length = math.sqrt(dotProd)
    return length

def vector_vectorProjection(projectedVector, canvasVector):
    numer = dotProduct(projectedVector, canvasVector)
    denom = (vectorLength(canvasVector))**2
    scalar = numer / denom
    result = scalar_vectorMult(scalar, canvasVector)
    return result
    

def buildVectorSet():
    numVectors = eval(input("How many vectors are in the set? "))
    vectorSet = []
    
    for i in range(numVectors):
        currentVector = eval(input("enter vector {:d} in the form [a1, a2, a3]: ".format(i+1)))
        vectorSet.append(currentVector)
        
    dimension = len(vectorSet[0])
    print("vector set is ", vectorSet)
    return vectorSet

def vectorAddition(vector1, vector2):
    if len(vector1) != len(vector2):
        print("both vectors must have the same dimension")
        return
    vectorSum = []
    for i in range(len(vector1)):
        sum = vector1[i] + vector2[i]
        vectorSum.append(sum)
    return vectorSum

def vectorSubtraction(vector2, vector1): ## vector2 - vector1
    if len(vector1) != len(vector2):
        print("both vectors must have the same dimension")
        return
    vectorSum = []
    for i in range(len(vector1)):
        sum = vector2[i] - vector1[i]
        vectorSum.append(sum)
    return vectorSum

def GramSchmidt(): ## numbers may look a little weird like 8.1837493e-16 instead of 0
    vectorSet = buildVectorSet()
    numVectors = len(vectorSet)
    orthogonalSet = []
    for i in range(numVectors):
        orthogonalVector = vectorSet[i]
        if len(orthogonalSet) != 0:
            sumOfProjections = vector_vectorProjection(orthogonalVector, orthogonalSet[0])
            for j in range(1, len(orthogonalSet)):
                sumOfProjections = vectorAddition(sumOfProjections, vector_vectorProjection(orthogonalSet[j], orthogonalVector))
            orthogonalVector = vectorSubtraction(orthogonalVector, sumOfProjections)
        orthogonalSet.append(orthogonalVector)
    return orthogonalSet

##-------------------------------------------------------------------------------------
## Some helper functions to build the matrix

def emptyMatrix(numRows,numCols):
    A = []
    for _ in range(numRows):
        row = [0] * numCols
        A.append(row)
    return A

def matrix(letter,numRows,numCols):
    A = emptyMatrix(numRows,numCols)

    for r in range(numRows):
        for c in range(numCols):
            A[r][c] = eval(input("Enter value for {:s}{:d}{:d}: ".format(letter,r+1,c+1)))
    return A

##-------------------------------------------------------------------------------------
## Some matrix operation programs

def matrixAddition():
    numRows, numCols = eval(input('Enter number of rows and columns ("m,n"): '))
    A = matrix("a",numRows,numCols)
    B = matrix("b",numRows,numCols)
    S = emptyMatrix(numRows,numCols)
    for r in range(numRows):
        for c in range(numCols):
            S[r][c] = A[r][c] + B[r][c]
    return S
#-------------------
def matrixMult():
    numRowsA, numColsA = eval(input('Enter number of rows and columns of the first matrix ("m,n"): '))
    numRowsB, numColsB = eval(input('Enter number of rows and columns of the second matrix ("m,n"): '))
    if numColsA != numRowsB:
        print("Do you even matrix bro?")
    else:
        A = matrix("a", numRowsA, numColsA)
        B = matrix("b", numRowsB, numColsB)
        M = emptyMatrix(numRowsA, numColsB)
        for cb in range(numColsB):
            for ra in range(numRowsA):
                for rb in range(numRowsB):
                    M[ra][cb] = M[ra][cb] + A[ra][rb] * B[rb][cb]
        return M
#-------------------
def matrixTranspose(ARows, ACols):
    A = matrix("a",ARows,ACols)
    TRows, TCols = ACols, ARows
    T = emptyMatrix(TRows,TCols)
    for rt in range(TRows):
        for ct in range(TCols):
            T[rt][ct] = A[ct][rt]
    print(T)

#-------------------
## REDUCED ROW ECHELON FORM –– My most challenging program!
    
def rref(numRows,numCols):
    A = matrix("a",numRows,numCols)
    rowsWithPivots = []
    ## Place pivots and zero out
    
    for c in range(1,numCols + 1):
        rowsWithPivots = placePivot(A, c, rowsWithPivots)
        A = zeroOutCol(A, c, rowsWithPivots)
        
    ## make pivots == 1
        
    A = makeOne(A, rowsWithPivots)
    
    ##rearrange rows
    pivotList, _ = realPivots(rowsWithPivots)
    numPivots = len(pivotList)
    
    rowOccupied = 0
    pivotLocation = 0
    pivotFound = False
    for c in range(1, numCols+1):
        for r in range(1,numRows+1):

            if A[r-1][c-1] == 1:
                pivotFound = True
                pivotLocation = r
                break
        
        if pivotFound == True:
            switchRows(A, rowOccupied+1, pivotLocation)
            rowOccupied = rowOccupied + 1
        pivotFound = False
        if rowOccupied == numPivots:
            break
    print(A)

##-------------------------------------------------------------------------------------
## Some helper functions for my rref program
                    
def placePivot(A,ColNum,rowsWithPivots):
    for r in range(len(A)):
        if not(r + 1 in rowsWithPivots) and A[r][ColNum - 1] != 0:
            rowsWithPivots.append(r + 1)
            return rowsWithPivots
    rowsWithPivots.append(False) # False means that that column has no pivots
    return rowsWithPivots
     
def zeroOutCol(A,ColNum,rowsWithPivots):
    # rowsWithPivots list position is the column number that that pivot is located in
    # rowsWithPivots list element is the row number that has a pivot
    pivotRow = rowsWithPivots[ColNum - 1]
    if pivotRow == False:
        return A
    for r in range(len(A)):
        if not(r + 1 == pivotRow) and A[r][ColNum - 1] != 0:
            pivotRowValue = A[pivotRow - 1][ColNum - 1]
            rValue = A[r][ColNum - 1]
            for c in range(len(A[0])):
                A[r][c], A[pivotRow - 1][c] = A[r][c] * pivotRowValue, A[pivotRow - 1][c] * rValue
                A[r][c] = A[r][c] - A[pivotRow - 1][c]
    return A


def makeOne(A, rowsWithPivots):
    for rowNum in rowsWithPivots:
        if rowNum != False:
            r = rowNum - 1
            c = rowsWithPivots.index(rowNum) # A[r][c] is the pivot
            pivot = A[r][c]
            for column in range(len(A[0])):
                A[r][column] = A[r][column] / pivot
    return A

def rearrange(A, rowsWithPivots, numRows):
    for r in range(1, numRows + 1):
        
        nextHighestRow = min(rowsWithPivots)
        if r != nextHighestRow:
            A = switchRows(A,r - 1,nextHighestRow - 1)
        rowsWithPivots.remove(nextHighestRow)
        
    return A

def realPivots(rowsWithPivots):
    columnsWithoutPivots = []
    while True:
        nextHighestRow = min(rowsWithPivots)
        if nextHighestRow == False:
            columnsWithoutPivots.append(rowsWithPivots.index(nextHighestRow) + 1)
            rowsWithPivots.remove(nextHighestRow)
        else:
            return rowsWithPivots, columnsWithoutPivots

        
def switchRows(A,row1,row2):
    A[row1 - 1], A[row2 - 1] = A[row2 - 1], A[row1 - 1]
    return A
                    
## Thank you for looking at my code :)
## Yours truly,
## Mario
