import pandas as pd

folder="demo"

pathtoclassid = f"{folder}\\classId.csv"
pathtosubId=f"{folder}\\subjectId.csv"
pathtosubpriority=f"{folder}\\subjectPriority.csv"
pathtosubTeacherClass=f"{folder}\\subjectTeachersClass.csv"
pathtosubjectTeacher=f"{folder}\\subjectTeacher.csv"
pathtoteacherId=f"{folder}\\teacherId.csv"
pathtostructure=f"{folder}\\structure.csv"
pathtosubClass = f"{folder}\\subjectClass.csv"

classId = pd.read_csv(pathtoclassid)
subid = pd.read_csv(pathtosubId)
subpriority = pd.read_csv(pathtosubpriority)
teacherid = pd.read_csv(pathtoteacherId)
subTeacher = pd.read_csv(pathtosubjectTeacher)
subTeacherClass=pd.read_csv(pathtosubTeacherClass)
nod=pd.read_csv(pathtostructure)
subjectClass = pd.read_csv(pathtosubClass)


subid=subid.fillna(0)
subpriority=subpriority.fillna(0)
teacherid=teacherid.fillna(0)
subTeacher=subTeacher.fillna(0)



