#######################################################################################
'''
    @uthor: Nautash
    Encoding: utf-8
	Project: Recommendation System
'''
#######################################################################################

import numpy as np
import math
import copy

#######################################################################################
# Populating data
data = []
user = [5, 2, 5, 0, 5, 3, 5]
data.append(user)

user = [1, 0, 4, 3, 2, 3, 2]
data.append(user)

user = [1, 3, 2, 4, 3, 3, 3]
data.append(user)

user = [1, 4, 2, 2, 0, 2, 3]
data.append(user)

user = [1, 5, 2, 4, 2, 3, 2]
data.append(user)

user = [5, 1, 5, 3, 5, 2, 5]
data.append(user)

#######################################################################################


#######################################################################################
# Function to calculate similarity
def calcFormula(a, b):
    a_square = [i * j for i, j in zip(a, a)]
    b_square = [i * j for i, j in zip(b, b)]
    ab = [i * j for i, j in zip(a, b)]
    
    sum_aSq = sum(a_square)
    sum_bSq = sum(b_square)
    sum_ab = sum(ab)
    
    try:
        similarity = sum_ab / ((math.sqrt(sum_aSq)) * (math.sqrt(sum_bSq)))
    except ZeroDivisionError:
        similarity = 0.0
    return round(similarity, 2)

#######################################################################################


#######################################################################################
# Function for cosine similarity
def cosineSimilarity(a, b):
    return calcFormula(a, b)

#######################################################################################


#######################################################################################
# Function for adjusting average
def adjustAvg(l):
    suml = sum(l)
    filledIndexes = len(l) - l.count(0)
    
    try:
        avgOf_l = suml / filledIndexes
    except ZeroDivisionError:
        avgOf_l = 0.0
    
    for i in range(len(l)):
        if l[i] != 0:
            l[i] -= avgOf_l
    
    return l
            
#######################################################################################


#######################################################################################
# Function for updating lists
def updateLists(a, b):
    a = adjustAvg(a)
    b = adjustAvg(b)
    
    return a, b
    
#######################################################################################


#######################################################################################
# Function for centered cosine similarity
def centeredCosineSimilarity(a, b):
    a, b = updateLists(a, b)
    return calcFormula(a, b)
    
#######################################################################################


#######################################################################################
# Function replace with zeroes
def replaceZeroesWith(a, b, val):
    l = [i for i in range(len(a)) if a[i] == 0]
    
    for i in l:
        b[i] = val
        
    return b
#######################################################################################


#######################################################################################
# Function for pearson similarity
def pearsonSimilarity(a, b):
    if a.count(0) > 0:
        b = replaceZeroesWith(a, b, 0)
        
    if b.count(0) > 0:
        a = replaceZeroesWith(b, a, 0)
        
    return calcFormula(a, b)
        
#######################################################################################


#######################################################################################
# Function for finding max in a list
def findMax(arr):
    maxNum = max(arr)
    return arr.index(maxNum)

#######################################################################################


#######################################################################################
# Function for generating similarity matrix
def simMatrix(data, typeOf):
    similarityMatrix = []

    for i in range(len(data)):
        simArray = []
        for j in range(len(data)):
            if typeOf == 0:
                simArray.append(cosineSimilarity(data[i], data[j]))
            elif typeOf == 1:
                simArray.append(centeredCosineSimilarity(data[i], data[j]))
            elif typeOf == 2:
                simArray.append(pearsonSimilarity(data[i], data[j]))
        similarityMatrix.append(simArray)
        
    return similarityMatrix

#######################################################################################


#######################################################################################
# Function for generating sorted similarity index matrix
def sortedSimIndexMatrix(similarityMatrix):
    sortedSimilarityIndexedMatrix = []

    for i in range(len(similarityMatrix)):
        copyList = similarityMatrix[i]
        indexList = []
        
        for j in range(len(similarityMatrix[i])):
            index = findMax(copyList)
            indexList.append(index)
            copyList[index] = -99
        sortedSimilarityIndexedMatrix.append(indexList)
        
    return sortedSimilarityIndexedMatrix
    
#######################################################################################


#######################################################################################
# Funtion to find similar users
def findSimilarObjects(l, users):
    simUsers = []
    
    for i in range((users)):
        simUsers.append(l[i])
        
    return simUsers
#######################################################################################


#######################################################################################
# Function for printing matrix
def printMatrix(matrix):
    for i in range(len(matrix)): print(matrix[i])
    print('\n')
    
#######################################################################################


#######################################################################################
# Function for popping first indexes from index-matrices
def popIndexes(matrix):
    for i in matrix:
        i.pop(0)
        
    return matrix

#######################################################################################


#######################################################################################
# Function for getting similar users
def getSimilarObjects(matrix):
    myDic = {}
    
    for i in range(len(data)):
        twoObjs, threeObjs, fourObjs = [], [], []
        l = []
        
        if data[i].count(0) > 0:
            twoObjs = findSimilarObjects(matrix[i], 2)
            threeObjs = findSimilarObjects(matrix[i], 3)
            fourObjs = findSimilarObjects(matrix[i], 4)
        
        # Adding similar users for indivial user
        l.append(twoObjs)
        l.append(threeObjs)
        l.append(fourObjs)
        myDic.update({i : l})
        
    return myDic

#######################################################################################


#######################################################################################
# Function to calculate weighted average
def calcWeightedAvg(simUsers, originalList, simMatrix):
    avgs = []
    
    for i in simUsers:
        total = 0
        den = 0.0
        
        # If list is empty, then there are no similar users
        if len(i) == 0:
            return 0
        for user in i:
            if user >= len(originalList):
                total = total + (originalList[len(originalList) - 1] * simMatrix[user])
            else:
                total = total + (originalList[user] * simMatrix[user])
            den += simMatrix[user]
        avgs.append(total / den)
    
    return max(avgs)

#######################################################################################


#######################################################################################
# Function to calculate average
def calcAvg(simUsers, originalList, simMatrix):
    avgs = []
    
    for i in simUsers:
        total = 0
        
        # If list is empty, then there are no similar users
        if len(i) == 0:
            return 0
        for user in i:
            if user >= len(originalList): total += originalList[len(originalList) - 1]
            else: total += originalList[user]
            
        avgs.append(total / len(i))
    
    return max(avgs)

#######################################################################################


#######################################################################################
### USER TO USER ###

# Generating cosine similarity matrix
cp = copy.deepcopy(data)
similarityMatrix = simMatrix(cp, 0)
print('Cosine similarity matrix (user-to-user):')
printMatrix(similarityMatrix)


# Generating centered cosine similarity matrix
cp = copy.deepcopy(data)
centeredSimilarityMatrix = simMatrix(cp, 1)
print('Centered cosine similarity matrix (user-to-user):')
printMatrix(centeredSimilarityMatrix)


# Generating pearson similarity matrix
cp = copy.deepcopy(data)
pearsonSimilarityMatrix = simMatrix(cp, 2)
print('Pearson similarity matrix (user-to-user):')
printMatrix(pearsonSimilarityMatrix)

#######################################################################################


#######################################################################################
### USER TO USER ###

# For Cosine Similarity
# Sorting similarityMatrix and creating index-based matrix
cp = copy.deepcopy(similarityMatrix)
sortedSimilarityIndexedMatrix = sortedSimIndexMatrix(cp)
sortedSimilarityIndexedMatrix = popIndexes(sortedSimilarityIndexedMatrix)
print('Sorted cosine similarity index matrix (user-to-user):')
printMatrix(sortedSimilarityIndexedMatrix)


# For Centered Cosine Similarity
# Sorting similarityMatrix and creating index-based matrix
cp = copy.deepcopy(centeredSimilarityMatrix)
sorted_centeredSimIndexedMatrix = sortedSimIndexMatrix(cp)
sorted_centeredSimIndexedMatrix = popIndexes(sorted_centeredSimIndexedMatrix)
print('Sorted centered cosine similarity index matrix (user-to-user):')
printMatrix(sorted_centeredSimIndexedMatrix)


# For Pearson Similarity
# Sorting similarityMatrix and creating index-based matrix
cp = copy.deepcopy(pearsonSimilarityMatrix)
sorted_pearsonSimIndexedMatrix = sortedSimIndexMatrix(cp)
sorted_pearsonSimIndexedMatrix = popIndexes(sorted_pearsonSimIndexedMatrix)
print('Sorted pearson similarity index matrix (user-to-user):')
printMatrix(sorted_pearsonSimIndexedMatrix)

#######################################################################################


#######################################################################################
# Making deep copy of data list
itemsData = copy.deepcopy(data)

# Taking transpose of a matrix
itemsData = np.array(itemsData)
itemsData = itemsData.transpose()

# Coverting numpy array back to list
itemsData = itemsData.tolist()

#######################################################################################


#######################################################################################
### ITEM TO ITEM ###
# Generating cosine similarity matrix
cp = copy.deepcopy(itemsData)
item_similarityMatrix = simMatrix(cp, 0)
print('Cosine similarity matrix (item-to-item):')
printMatrix(item_similarityMatrix)


# Generating centered cosine similarity matrix
cp = copy.deepcopy(itemsData)
item_centeredSimilarityMatrix = simMatrix(cp, 1)
print('Centered cosine similarity matrix (item-to-item):')
printMatrix(item_centeredSimilarityMatrix)


# Generating pearson similarity matrix
cp = copy.deepcopy(itemsData)
item_pearsonSimilarityMatrix = simMatrix(cp, 2)
print('Pearson similarity matrix (item-to-item):')
printMatrix(item_pearsonSimilarityMatrix)

#######################################################################################


#######################################################################################
### ITEM TO ITEM ###

# For Cosine Similarity
# Sorting similarityMatrix and creating index-based matrix
cp = copy.deepcopy(item_similarityMatrix)
item_sortedSimilarityIndexedMatrix = sortedSimIndexMatrix(cp)
item_sortedSimilarityIndexedMatrix = popIndexes(item_sortedSimilarityIndexedMatrix)
print('Sorted cosine similarity index matrix (item-to-item):')
printMatrix(item_sortedSimilarityIndexedMatrix)


# For Centered Cosine Similarity
# Sorting similarityMatrix and creating index-based matrix
cp = copy.deepcopy(item_centeredSimilarityMatrix)
item_sorted_centeredSimIndexedMatrix = sortedSimIndexMatrix(cp)
item_sorted_centeredSimIndexedMatrix = popIndexes(item_sorted_centeredSimIndexedMatrix)
print('Sorted centered cosine similarity index matrix (item-to-item):')
printMatrix(item_sorted_centeredSimIndexedMatrix)


# For Pearson Similarity
# Sorting similarityMatrix and creating index-based matrix
cp = copy.deepcopy(item_pearsonSimilarityMatrix)
item_sorted_pearsonSimIndexedMatrix = sortedSimIndexMatrix(cp)
item_sorted_pearsonSimIndexedMatrix = popIndexes(item_sorted_pearsonSimIndexedMatrix)
print('Sorted pearson similarity index matrix (item-to-item):')
printMatrix(item_sorted_pearsonSimIndexedMatrix)

#######################################################################################


#######################################################################################
# Function to calculate averages of similar users
def getAvgs(dictionary, avgFun):
    user_cosineAvgs, user_centeredAvgs, user_pearsonAvgs = [], [], []
    item_cosineAvgs, item_centeredAvgs, item_pearsonAvgs = [], [], []
    itemsAvgs, usersAvgs = {}, {}
    
    # Dictionary -> List -> Dictionary -> List of lists
    for key, value in dictionary.items():
        
        ### USERS ###
        if key == 'Users':
            # Accessing dictionaries from list
            for i in range(len(value)):
                # Accessing dictionary items
                for k, v in value[i].items():
                     # Cosine similarity
                    if i == 0:
                        user_cosineAvgs.append(avgFun(v, data[k], similarityMatrix[k]))
                    # Centered cosine similarity
                    elif i == 1:
                        user_centeredAvgs.append(avgFun(v, data[k], centeredSimilarityMatrix[k]))
                    # Pearson similarity
                    #elif i == 2:
                        #user_pearsonAvgs.append(avgFun(v, data[k], pearsonSimilarityMatrix[k]))
                        
            usersAvgs.update({'cosine' : user_cosineAvgs})
            usersAvgs.update({'centered' : user_centeredAvgs})
            #usersAvgs.update({'pearson' : user_pearsonAvgs})
            
        ### ITEMS ###
        elif key == 'Items':
            # Accessing dictionaries from list
            for i in range(len(value)):
                # Accessing dictionary items
                for k, v in value[i].items():
                    # Cosine similarity
                    if i == 0:
                        item_cosineAvgs.append(avgFun(v, itemsData[k], item_similarityMatrix[k]))
                    # Centered cosine similarity
                    elif i == 1:
                        item_centeredAvgs.append(avgFun(v, itemsData[k], item_centeredSimilarityMatrix[k]))
                    # Pearson similarity
                    #elif i == 2:
                        #item_pearsonAvgs.append(avgFun(v, itemsData[k], item_pearsonSimilarityMatrix))
                        
            itemsAvgs.update({'cosine': item_cosineAvgs})
            itemsAvgs.update({'centered': item_centeredAvgs})
            #itemsAvgs.update({'pearson': item_pearsonAvgs})
        
    avgsDict = {'Users' : usersAvgs, 'Items' : itemsAvgs}
    return avgsDict

#######################################################################################


#######################################################################################
# Function to calculte final average
def getFinalAvg(normalAvgsDict, weightedAvgsDict):
    fi = {}
    for (key1, value1), (key2, value2) in zip(normalAvgsDict.items(), weightedAvgsDict.items()):
        dic = {}
        
        for (k1, v1), (k2, v2) in zip(value1.items(), value2.items()):
            li = []
            
            for i, j in zip(v1, v2):
                li.append((i + j) / 2)
            dic.update({k1 : li})
        fi.update({key1 : dic})
        
    return fi

#######################################################################################


#######################################################################################
# Function to print averages
def printAvgs(normalAvgsDict, weightedAvgsDict):
    for (key1, value1), (key2, value2) in zip(normalAvgsDict.items(), weightedAvgsDict.items()):
        print('User-to-User:') if key1 == 'Users' else print('Item-to-Item:')
        for (k1, v1), (k2, v2) in zip(value1.items(), value2.items()):
            print('Normal avg: {} -> {}'.format(k1, v1))
            print('Weighted avg: {} -> {}\n'.format(k2, v2))
    print('\n')
    
#######################################################################################


#######################################################################################
# Function to print averages
def printFinalAvg(avgs):
    for key, value in avgs.items():
        print('User-to-User:') if key == 'Users' else print('\nItem-to-Item:')
        for k, v in value.items():
            print('Final avg: {} -> {}'.format(k, v))
    print('\n')
    
#######################################################################################


#######################################################################################
# Generating new matrices by replacing zeroes with averages
def generateNewMatrices(dic, usersData):
    di = {}
    
    for key, value in dic.items():
        if key == 'Users':
            d = {}
            
            for k, v in value.items():
                if k == 'cosine':
                    cp = copy.deepcopy(usersData)
                    
                    for i in range(len(v)):
                        if cp[i].count(0) > 0:
                            cp[i] = replaceZeroesWith(cp[i], cp[i], v[i])
                    
                    cp1 = copy.deepcopy(cp)
                    print('Cosine similarity matrix (user-to-user):')
                    printMatrix(cp1)
                    d.update({k : cp1})
                
                elif k == 'centered':
                    cp = copy.deepcopy(usersData)
                    
                    for i in range(len(v)):
                        if cp[i].count(0) > 0:
                            cp[i] = replaceZeroesWith(cp[i], cp[i], v[i])
                    
                    cp1 = copy.deepcopy(cp)
                    print('Centered cosine similarity matrix (user-to-user):')
                    printMatrix(cp1)
                    d.update({k : cp1})
            
            di.update({key : d})
    return di

#######################################################################################


#######################################################################################
# Function to calculate accuracies
def calcAccuracies(dic, usersData):
    for key, value in dic.items():
        print('User-to-User') if key == 'Users' else print('Item-to-Item')
        
        for k, v in value.items():
            if k == 'cosine':
                print('Accuracies by using cosine method:')
            elif k == 'centered':
                print('Accuracies by using centered cosine method:')
                
            accuracies = []
            for i in range(len(v)):
                accuracies.append(cosineSimilarity(v[i], usersData[i]) * 100)
                
            print(accuracies)
            print()

#######################################################################################


#######################################################################################
# Getting similar USERS
sim_Users = getSimilarObjects(sortedSimilarityIndexedMatrix)
cen_Users = getSimilarObjects(sorted_centeredSimIndexedMatrix)
pea_Users = getSimilarObjects(sorted_pearsonSimIndexedMatrix)

# Getting similar ITEMS
sim_Items = getSimilarObjects(item_sortedSimilarityIndexedMatrix)
cen_Items = getSimilarObjects(item_sorted_centeredSimIndexedMatrix)
pea_Items = getSimilarObjects(item_sorted_pearsonSimIndexedMatrix)

#######################################################################################


#######################################################################################
# Making list of dictionaries
### USERS ###
usersList = [sim_Users, cen_Users, pea_Users]

### ITEMS ###
itemsList = [sim_Items, cen_Items, pea_Items]

# Making dictionary to store data
dictionary = {
        'Users' : usersList,
        'Items' : itemsList
        }

# Calculating normal and weighted averages
# Dictionary -> Dictionary -> List
normalAvgsDict = getAvgs(dictionary, avgFun=calcAvg)
weightedAvgsDict = getAvgs(dictionary, avgFun=calcWeightedAvg)
printAvgs(normalAvgsDict, weightedAvgsDict)

# Taking average of normal and weighted averages
finalAvgsDict = getFinalAvg(normalAvgsDict, weightedAvgsDict)
printFinalAvg(finalAvgsDict)

#######################################################################################


#######################################################################################
# Making and printing new matrices by replacing zeroes with averages
newMatricesDic = generateNewMatrices(finalAvgsDict, data)
calcAccuracies(newMatricesDic, data)

#######################################################################################