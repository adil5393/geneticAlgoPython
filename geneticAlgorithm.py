from createVariables import totalPeriodsPerSubject,classes,days,numberofperiods, totalpopulation,mutationRate
import copy
from utility import calculatePopulationScores,scoreShouldBeofClassesAndPopulation, display,orderPerClass,createTimetable,probabilityDistribution,getClassProbs,calcPriorityScore
import random
orders = orderPerClass(totalPeriodsPerSubject,classes)
initialtimetable = [createTimetable(orders)]
# from createPopulation import scoreShouldBeofClassesAndPopulation


stagnantscores = []
def createPopulation(totalPopulation,orders):
    generation = []
    for i in range(totalPopulation):
        timetable = createTimetable(orders)
        generation . append(timetable)
    return generation

def createChildFromClasses(classProbs,populationspace):
    newChild = {}
    for day in days:
        newChild[day]={}
        for cls in classes:
            keys = list(classProbs[cls].keys())
            weights = list(classProbs[cls].values())
            parents = random.choices(keys,weights,k=2)
            if(classProbs[cls][parents[0]]>classProbs[cls][parents[1]]):
                space = parents[0]
            else:
                space = parents[1]
            newChild[day][cls] = copy.deepcopy(populationspace[space][day][cls])
    return newChild

def createChildFromPopulation(classProbs,populationspace):
    newChild = {}
    for day in days:
        newChild[day]={}
        for cls in classes:
            keys = list(classProbs[cls].keys())
            weights = list(classProbs[cls].values())
            parents = random.choices(keys,weights,k=2)
            if(classProbs[cls][parents[0]]>classProbs[cls][parents[1]]):
                space = parents[0]
            else:
                space = parents[1]
            newChild[day] = copy.deepcopy(populationspace[space][day])
            break
    return newChild
def createChildFromPeriods(populationprobabilityDistribution,populationspace):
    newChild = {}
    keys = list(populationprobabilityDistribution.keys())
    weights = list(populationprobabilityDistribution.keys())
    parents = random.choices(keys,weights,k=2)
    pop1 = parents[0]
    pop2 = parents[1]
    crossoverpoint = random.randint(0,numberofperiods-1)
    days1 = days[:crossoverpoint]
    days2 = days[crossoverpoint:]
    for day in days1:
        newChild[day] = populationspace[pop1][day]
    for day in days2:
        newChild[day] = populationspace[pop2][day]
    return newChild
def mutate(timetable, mutation_rate):
    r = random.random()
    if(r<=0.5):
        for day in timetable:
            for cls in timetable[day]:
                if random.random() < mutation_rate:
                    timetable[day][cls] = random.sample(timetable[day][cls], len(timetable[day][cls]))
    else:
        p1 = random.randint(0,numberofperiods-1)
        p2 = random.randint(0,numberofperiods-1)
        for cls in classes:
            if random.random()<mutation_rate:
                for day in timetable:
                    timetable[day][cls][p1],timetable[day][cls][p2] = timetable[day][cls][p2],timetable[day][cls][p1] 
    return timetable

scoresShouldbeOfClasses, scoreShouldbePopulation, clsPriorityScore, distScore =scoreShouldBeofClassesAndPopulation(classes)
populationspace = createPopulation(totalpopulation,orders)
populationScoresMap,maxPopScore,minPopScore,scoreOfClasses,scoreDistributionMap, overlapscoresMap,overlapScoreValuesMap,maxPopScoreMap,minPopScoreMap, prScore = calculatePopulationScores(totalpopulation,populationspace,classes,clsPriorityScore,distScore)
populationprobabilityDistribution=probabilityDistribution(totalpopulation,populationScoresMap)
classProbs = getClassProbs(scoreOfClasses,classes)
oldScore=frstScore = maxPopScore

target = scoreShouldbePopulation
genCount = 0
try:
    while True:
        newGen = []
        while len(newGen)<totalpopulation:
            r= random.random()
            if(r<=0.3):         
                child = createChildFromPopulation(classProbs,populationspace)
            elif(0.3<r<0.9):
                child = createChildFromClasses(classProbs,populationspace)
            else:
                child = createChildFromPeriods(populationprobabilityDistribution,populationspace)
            child = mutate(child,mutationRate)
            newGen.append(child)
        genCount+=1
        populationspace = newGen
        for i in range(totalpopulation):
            for cls in classes:
                populationspace = calcPriorityScore(cls,populationspace,i)
        if(genCount == 100):
            print(genCount)
            n =10
            oldScore = 0
            populationspace  = createPopulation(totalpopulation,orders)
            stagnantscores.append(maxPopScore)
            genCount = 0
        populationScoresMap,maxPopScore,minPopScore,scoreOfClasses,scoreDistributionMap, overlapscoresMap,overlapScoreValuesMap,maxPopScoreMap,minPopScoreMap, prScore = calculatePopulationScores(totalpopulation,populationspace,classes,clsPriorityScore,distScore)
        populationprobabilityDistribution=probabilityDistribution(totalpopulation,populationScoresMap)
        classProbs = getClassProbs(scoreOfClasses,classes)
        # print(frstScore,maxPopScore,minPopScore,scoreShouldbePopulation)
        if(maxPopScore>oldScore ):
            oldScore = maxPopScore
            print(frstScore,maxPopScore,minPopScore,scoreShouldbePopulation,)
            genCount = 0
        
            if(maxPopScore==target):
                break
except KeyboardInterrupt as e:
    print(stagnantscores)
    

print(frstScore,maxPopScore,minPopScore,scoreShouldbePopulation)
for k,v in populationScoresMap.items():
    if(v==maxPopScore):
        print(maxPopScore,scoreShouldbePopulation,k)
        print(overlapscoresMap[k])
        print(prScore[k])
        display(populationspace[k])
        break
for k,v in populationScoresMap.items():
    if(v==minPopScore):
        print(minPopScore,scoreShouldbePopulation,k)
        print(overlapscoresMap[k])
        display(populationspace[k])
        break
    