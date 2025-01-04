
import createVariables as cv
import random

def createOrderMaps(totalPeriodsPerSubject,cls):
    orderMaps = {}
    for i in range(cv.numberofperiods):
        orderMaps[i+1]={}
        for subject in totalPeriodsPerSubject[cls]:
            for tup in totalPeriodsPerSubject[cls][subject]['days']:
                if(tup[1] == i+1):
                    orderMaps[i+1][subject]=(tup)
    return orderMaps
def getOrders(target,cls):
    orders=[]
    maxDays={}
    # print(target)
    for i in target:
        maxDays = {}
        for k, v in target[i].items():
            maxDays[k] = v[0]
        
        if(len(maxDays.values())==0):
            continue
        maxDay = max(maxDays.values())
        filterforSubjects = {
            key: target[i][key][1]
            for key, value in maxDays.items()
            if value == maxDay and key in target[i]
        }
        if(len(orders)!=0):
            pass
        count = 0
        while count<maxDay:
            pick = random.randint(0,len(cv.allPermutations[cls])-1)
            candidate = cv.allPermutations[cls][pick]
            changeCandidate =False
            # print(candidate)
            for subs in target[i]:
                gotSubject = False
                for subTeacher in candidate:
                    subject = subTeacher.split("-")[1]
                    teacher = subTeacher.split("-")[0]
                    if(subject==subs):
                        if(candidate.count(subTeacher)==target[i][subs][1]):
                            gotSubject = True
                            break
                        else:
                            changeCandidate =True
                            break
                if(not gotSubject):
                    changeCandidate = True
                if(changeCandidate):
                    break
            if(not changeCandidate):
                count+=1
                orders.append(list(candidate))
                
    return orders
        

def orderPerClass(totalPeriodsPerSubject,classes):
    ordersPerClass = {}
    for cls in classes:
        orderMap = createOrderMaps(totalPeriodsPerSubject,cls)
        ordersPerClass[cls] = getOrders(orderMap,cls)
    return ordersPerClass

def createTimetable(ordersPerClass):
    timetable = {}
    for day in cv.days:
        timetable[day]={}
        for cls in ordersPerClass:
                pick=random.randint(0,len(ordersPerClass[cls])-1)
                order = ordersPerClass[cls][pick]
                timetable[day][cls]=(order)
    return timetable


def swap(a,b):
    return (b,a)
def display(timetable):
    for key1 in timetable:
        print(key1)
        for key2 in timetable[key1]:
            print(key2,timetable[key1][key2])
def overLapScore(populationspace,population,classes,prnt=False):
    overLapScores = {}
    for popIndex in range(population):
        overLapScores[popIndex]= calcTeacherOverlapScore(populationspace,popIndex,classes,prnt)
    return overLapScores

def initializeStructure(population,rforce,classes=None):
    population=population
    rforce = rforce
    classes=classes
    if(classes == None):
        classes = cv.classList
    return (population,classes,rforce)
    
def scoreShouldBeofClassesAndPopulation(classes):
    scoresShouldbeOfClasses ={}
    for cls in classes:
        scoresShouldbeOfClasses[cls]=scoreShouldbe(cls)[0]
    scoreShouldbePopulation = sum(scoresShouldbeOfClasses.values())
    return scoresShouldbeOfClasses, scoreShouldbePopulation

def getTeacherScores(cls):
    subPriorityTeacherScore=[ (cv.numberofperiods-1) for item in cv.subPriorityMap[cls].keys()]
    return subPriorityTeacherScore

def periodDistributionScores(cls):
    priorityMap = cv.subPriorityMap
    periodsPerSubject = cv.gettotalPeriodsPerSubject(priorityMap)
    periodDistributionList =[]
    periodDistributionMap ={}
    for subject in periodsPerSubject[cls].keys():
        for dist in periodsPerSubject[cls][subject]['days']:
            periodDistributionList.append(dist[0]/dist[1])
        periodDistributionMap[subject] = sum(periodDistributionList)
        periodDistributionList =[]
    return periodDistributionMap

def scoreShouldbe(cls):
    score=0
    subPrioritySubjectScrore = cv.subPriorityMap[cls].values()
    teacheroverLapScore = (1*len(cv.classes)-1)*cv.numberofperiods*len(cv.days)
    #subPriorityTeacherScore = getTeacherScores(cls)
    #score = sum(subPrioritySubjectScrore) + sum(subPriorityTeacherScore)
    periodDistributionMap = periodDistributionScores(cls)
    periodDistributionScore = periodDistributionMap.values()
    score += sum(periodDistributionScore) + sum(subPrioritySubjectScrore) + teacheroverLapScore
    return score, periodDistributionMap


def calcPriorityScore(cls,populationspace,popIndex):
    days = cv.days
    subjectTeacherClassMap = cv.subTeacherClassMap
    totalPriorityScore = 0
    for values in subjectTeacherClassMap[cls].values():
        for subject in values:
            prioriTyScore = 0
            prirotyVal = cv.subPriorityMap[cls][subject]
            for day in days: 
                for subTeacher in populationspace[popIndex][day][cls]:
                    if(subject == subTeacher.split("-")[1]):
                        prioriTyScore += 1
            if(prioriTyScore>prirotyVal):
                prioriTyScore = prioriTyScore-prirotyVal
            totalPriorityScore+=prioriTyScore 
    return(totalPriorityScore)


def calcDistributionScore(cls,populationspace,popIndex):
    days = cv.days
    numberofperiods = cv.numberofperiods
    subjectList = cv.subjectList
    subjectDistributionMap ={}
    distributionScoreList = []
    dayCount=0
    for subject in subjectList:
        subjectDistributionMap[subject]=[]
        for i in range(1,numberofperiods+1):
            dayCount=0    
            subCountNew =0
            for day in days:
                subCount = 0                
                for subTeacher in populationspace[popIndex][day][cls]:
                    if(subject == subTeacher.split("-")[1]):
                        subCount +=1#############
                if(subCount == i):
                    dayCount+=1
                    subCountNew =subCount
            if(dayCount>0):
                subjectDistributionMap[subject].append((dayCount,subCountNew))
                distributionScoreList.append(dayCount/subCountNew)
    distributionScore = sum(distributionScoreList)
    return distributionScore,subjectDistributionMap

def totalFitnessOfPopSpace(populationScoresMap):
    totalFitness = sum(populationScoresMap.values())
    return totalFitness

def probabilityDistribution(population,populationScoresMap):
    totalFitness = totalFitnessOfPopSpace(populationScoresMap)
    probabilityDist ={}
    for i in range(population):
        probabilityDist[i] = populationScoresMap[i]/totalFitness
    return probabilityDist

def calcTeacherOverlapScore(populationspace, popIndex, classes, prnt=False):
    days = cv.days
    numberofperiods = cv.numberofperiods
    overlapScoremap = {}

    # Initialize overlapScoremap for all classes
    for cls in classes:
        overlapScoremap[cls] = {}
        for cls2 in classes:
            if cls != cls2:
                overlapScoremap[cls][cls2] = 0

    # Loop through all days and aggregate scores
    for day in days:
        for period in range(numberofperiods):
            for cls in classes:
                teacher = populationspace[popIndex][day][cls][period].split("-")[0]

                for cls2 in classes:
                    if cls != cls2:
                        teacher2 = populationspace[popIndex][day][cls2][period].split("-")[0]

                        # Increment or decrement based on teacher match
                        if teacher == teacher2:
                            overlapScoremap[cls][cls2] += 1
                        else:
                            overlapScoremap[cls][cls2] -= 1

    # Print the final cumulative dictionary
    if prnt:
        print("Final cumulative overlap scores:")
        print(overlapScoremap)

    return overlapScoremap


def calculatePopulationScores(population,populationspace,classes,prnt=False):
    populationScoresMap ={}
    scoreOfClasses ={}
    scoreDistributionMap = {}
    overlapScoreValuesMap = {}
    overLapscoresMap = overLapScore(populationspace,population,classes,prnt)
    
    for popIndex in range(population):
        overlapScoreValuesMap[popIndex]={}
        for k,v in overLapscoresMap[popIndex].items():
            overlapScoreValuesMap[popIndex][k] = sum(v.values())
    for popIndex in range(population):
        scoreOfClasses[popIndex] = {}
        scoreDistributionMap[popIndex] = {}
        totalscore = 0
        mpr = 0
        for cls in classes:       
            distributionDetail=calcDistributionScore(cls,populationspace,popIndex)
            priorityScore = calcPriorityScore(cls,populationspace,popIndex)
            distributionScore = distributionDetail[0]
            scoreDistributionMap[popIndex][cls] = distributionDetail[1]            
            overlapLoss = overlapScoreValuesMap[popIndex][cls]
            score = distributionScore + priorityScore -overlapLoss
            scoreOfClasses[popIndex][cls] = score
            totalscore += score
        populationScoresMap[popIndex]=totalscore
    maxScore = max(populationScoresMap.values())
    minScore = min(populationScoresMap.values())
    for popIndex,popScore in populationScoresMap.items():
        if(popScore==maxScore):
            maxPopscoreMap ={popIndex:maxScore}
    for popIndex,popScore in populationScoresMap.items():
        if(popScore == minScore):
            minPopscoreMap = {popIndex:minScore}
    return populationScoresMap,maxScore,minScore,scoreOfClasses,scoreDistributionMap,overLapscoresMap, overlapScoreValuesMap,maxPopscoreMap,minPopscoreMap
        
    
def getClassProbs(scoreoclasses,classes):
    clasprobabilities = {}
    for cls in classes:
        totalProb = 0
        clasprobabilities[cls]={}
        for i in scoreoclasses:
            totalProb+=scoreoclasses[i][cls]
        #     print(scoreoclasses[i][cls])
        # print(totalProb)
        for i in scoreoclasses:
            clasprobabilities[cls][i]=scoreoclasses[i][cls]/totalProb
        # print(clasprobabilities)
    return clasprobabilities
    
    