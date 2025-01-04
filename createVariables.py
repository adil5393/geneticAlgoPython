#importing all data objects.
# from utility import calculatePopulationScores
from getAllFiles import *
import itertools
import random

'''
importing below variables
classId
subid
subpriority
teacherid
subTeacher
subTeacherClass
nod
'''

classList=[classId["class"][item] for item in range(len(classId["class"]))]
teachersList=[teacherid["teachers"][item] for item in range(len(teacherid["teachers"]))]
days = ["monday","tuesday","wednesday","thursday","friday","saturday"]
numberofperiods=int(nod["value"][0])
subjectList=[subid["subject"][i] for i in range(len(subid["subject"]))]
periodsperteacherperday=numberofperiods-1
classes = None
if(classes == None):
    classes= classList

def createSubTeacherMap(subTeacher):
    subTeacherMap={}
    for i in range(len(subTeacher)):
        teacher=subTeacher["teachers"][i]
        subTeacherMap[teacher]=[]
        for key in subTeacher.keys():
            if(key == "teachers" or key == "total Subjects"):
                continue
            if(subTeacher[key][i]==1):
                subTeacherMap[teacher].append(key)
    return subTeacherMap

#subTeacher-------------------------------------
def subClassMap (subClass):
    subjectClass = {}
    for i in range(len(subClass['Class'])):
        cls = subClass['Class'][i]
        subjectClass[cls]=[]
        for subjects in subClass.keys():
            if(subjects=='Class'):
                continue
            if(subClass[subjects][i]==1):
                subjectClass[cls].append(subjects)
    return subjectClass

def createSubPriorityMap(subpriority):
    subPriorityMap={}
    for i in range(len(subpriority)):
        subject=subpriority["Class"][i]
        subPriorityMap[subject]={}
        for key in subpriority.keys():
            if(key == "Class" or key == "total"):
                continue
            if(subpriority[key][i]>0):
                subPriorityMap[subject][key]=int(subpriority[key][i])
    return subPriorityMap
#sbpriority map----------------------------------

def subjectTeacherPair(subTeacherMap):
    subjectTeacherPairs=[]
    for keys in subTeacherMap.keys():
        for subject in subTeacherMap[keys]:
            subjectTeacherPairs.append(keys+"-"+subject)
    return subjectTeacherPairs


def gettotalPeriodsPerSubject(subPriorityMap):
    totalPeriodsPerSubject = {}
    for cls in classList:
        totalPeriodsPerSubject[cls]={}
        for subject in subjectList:
            totalPeriodsPerSubject[cls][subject]={}
            try:
                totalPeriodsPerSubject[cls][subject]['days']=[]
                priority = subPriorityMap[cls][subject]#18
            except KeyError:
                continue
            if(priority<=len(days)):
                day = priority
                periods = 1
                totalPeriodsPerSubject[cls][subject]['days'].append((day,periods))
            else:
                remainingDays = priority%len(days)#0
                period = priority//len(days)# 2
                daysCheck = len(days)*period #12
                if(remainingDays>0):
                    totalPeriodsPerSubject[cls][subject]['days'].append((priority-daysCheck,period+1))
                totalPeriodsPerSubject[cls][subject]['days'].append((len(days)-remainingDays,period))            
    return totalPeriodsPerSubject


def createSubTeacherClassMap():
    subTeacherClassMap={}
    for keys in subTeacherClass.keys():
        if(keys=="Subject"):
            continue
        for i in range(len(subTeacherClass[keys])):
            if(subTeacherClass[keys][i] not in teachersList):
                print(subTeacherClass[keys][i],keys,i,"Not Recognised- Please add them in Teacherid.csv")
                
    for keys in subTeacherClass.keys():
        if(keys=="Subject"):
            continue
        subTeacherClassMap[keys]={}
        for teachers in teachersList:
            subTeacherClassMap[keys][teachers]=[]
        for index in range(len(list(subTeacherClass[keys]))):
            if(subTeacherClass[keys][index] not in teachersList):
                continue
            subTeacherClassMap[keys][subTeacherClass[keys][index]].append(subTeacherClass["Subject"][index])
    for cls in classList:
        for teacher in teachersList:
            if(len(subTeacherClassMap[cls][teacher])==0):
                del subTeacherClassMap[cls][teacher]
    return subTeacherClassMap

def createSubTeacherPairPerClass(subTeacherClassMap):
    pairsPerClass={}
    for cls in subTeacherClassMap:
        pairsPerClass[cls]=[]
        for teacher in subTeacherClassMap[cls]:
            for subject in subTeacherClassMap[cls][teacher]:
                pair = teacher+"-"+subject
                pairsPerClass[cls].append(pair)
    return pairsPerClass


import itertools

def createAllPermutations(pairsPerClass, totalPeriodsPerSubject, numberofperiods, subjectClassList, classes):
    allPermutations = {}
    maxSubjects = {}
    finalPermutations = {}

    # Step 1: Generate all permutations for each class
    for cls in pairsPerClass:
        allPermutations[cls] = list(itertools.product(pairsPerClass[cls], repeat=numberofperiods))
    
    # Step 2: Calculate maximum periods per subject for each class
    for cls in classes:
        maxSubjects[cls] = {
            subject: max(items[1] for items in totalPeriodsPerSubject[cls][subject]['days'])
            for subject in totalPeriodsPerSubject[cls]
        }
    
    # Step 3: Filter permutations based on constraints
    for cls in classes:
        finalPermutations[cls] = []
        for perm in allPermutations[cls]:
            permGood=True
            for pair in pairsPerClass[cls]:
                subject = pair.split("-")[1]
                if(maxSubjects[cls][subject] < perm.count(pair)):
                    permGood = False
                    break
            if(permGood):
                finalPermutations[cls].append(perm)
                    
                    

    return finalPermutations


subjectClassList = subClassMap(subjectClass)
subTeacherMap = createSubTeacherMap(subTeacher)
subPriorityMap = createSubPriorityMap(subpriority)
subjectTeacherPairs = subjectTeacherPair(subTeacherMap)
totalPeriodsPerSubject=gettotalPeriodsPerSubject(subPriorityMap)
subTeacherClassMap = createSubTeacherClassMap()
pairsPerClass = createSubTeacherPairPerClass(subTeacherClassMap)
allPermutations = createAllPermutations(pairsPerClass,totalPeriodsPerSubject,numberofperiods,subjectClassList,classes)


