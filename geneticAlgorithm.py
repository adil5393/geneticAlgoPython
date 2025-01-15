from createVariables import totalPeriodsPerSubject,classes,days,numberofperiods
import copy
from utility import calculatePopulationScores,scoreShouldBeofClassesAndPopulation, display,orderPerClass,createTimetable,probabilityDistribution,getClassProbs
import random
orders = orderPerClass(totalPeriodsPerSubject,classes)
initialtimetable = [createTimetable(orders)]
# from createPopulation import scoreShouldBeofClassesAndPopulation
totalpopulation = 100
generations = 1000
mutationRate = 0.01
crossoverrate = 0.5


def createPopulation(totalPopulation,orders):
    generation = []
    for i in range(totalPopulation):
        timetable = createTimetable(orders)
        generation . append(timetable)
    return generation

def createChildFromClasses2(classProbs, populaitonspace):
    
    pass
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
            newChild[day][cls] = populationspace[space][day][cls]
    return newChild

def createChildFromPopulation(populationprobabilityDistribution,populationspace):
    keys = populationprobabilityDistribution.keys()
    weights = populationprobabilityDistribution.values()
    parents = random.choices(list(keys),list(weights),k=2)
    parent1 = populationspace[parents[0]]
    parent2 = populationspace[parents[1]]
    crossoverpointday = random.randint(0,len(days)-1)
    days1 = days[:crossoverpointday]
    days2 = days[crossoverpointday:]
    newchild = {}
    for day in days1:
        newchild[day] = copy.deepcopy(parent1[day])
    for day in days2:
        newchild[day] = copy.deepcopy(parent2[day])
    return newchild
def mutate(timetable, mutation_rate):
    for day in timetable:
        for cls in timetable[day]:
            if random.random() < mutation_rate:
                timetable[day][cls] = random.sample(timetable[day][cls], len(timetable[day][cls]))
    return timetable

scoresShouldbeOfClasses, scoreShouldbePopulation, clsPriorityScore, distScore =scoreShouldBeofClassesAndPopulation(classes)
populationspace = createPopulation(totalpopulation,orders)
populationScoresMap,maxPopScore,minPopScore,scoreOfClasses,scoreDistributionMap, overlapscoresMap,overlapScoreValuesMap,maxPopScoreMap,minPopScoreMap, prScore = calculatePopulationScores(totalpopulation,populationspace,classes,clsPriorityScore,distScore)
populationprobabilityDistribution=probabilityDistribution(totalpopulation,populationScoresMap)
classProbs = getClassProbs(scoreOfClasses,classes)
oldScore=frstScore = maxPopScore

target = scoreShouldbePopulation
genCount = 0
while True:
    newGen = []
    while len(newGen)<totalpopulation:
        r= random.random()
        if(r<=0):         
            child = createChildFromPopulation(populationprobabilityDistribution,populationspace)
        else:
            child = createChildFromClasses(classProbs,populationspace)
        child = mutate(child,mutationRate)
        newGen.append(child)
    genCount+=1
    populationspace = newGen
    if(genCount == 500):
        print(genCount)
        n =10
        populationspace[:n] = createPopulation(n,orders)
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
    