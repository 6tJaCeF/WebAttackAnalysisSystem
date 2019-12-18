from math import e
from math import log

#权值
w={"SQLi":60.0,"XSS":60.0,"SSI":90.0,
   "BufferOverflow":80.0,"CRLFi":20.0,"XPath":40.0,
   "LDAPi":80.0,"FormatString":20.0,"anomalous":20.0,"normal":100.0}


def calculate_Three(objectList):
   SQLi = objectList.setdefault('SQLi',0)
   XSS = objectList.setdefault('XSS',0)
   SSI = objectList.setdefault('SSI',0)
   BufferOverflow = objectList.setdefault('BufferOverflow',0)
   CRLFi = objectList.setdefault('CRLFi',0)
   XPath = objectList.setdefault('XPath',0)
   LDAPi = objectList.setdefault('LDAPi',0)
   FormatString = objectList.setdefault('FormatString',0)
   anomalous = objectList.setdefault('anomalous',0)
   normal = objectList.setdefault('normal',0)
   sum = SQLi+XSS+SSI+BufferOverflow+CRLFi+XPath+LDAPi+FormatString+anomalous+normal
   if sum==0:
      return [0,0,0]
   elif SQLi == 0 and XSS == 0 and SSI == 0 and BufferOverflow == 0 and CRLFi == 0 and XPath == 0 and LDAPi == 0 and FormatString == 0 and anomalous == 0 and normal != 0:
      return [100,100,100]
   else:
      Jurisdiction = Atomic_situation(SQLi,sum,"SQLi") + Atomic_situation(XPath,sum,"XPath") + Atomic_situation(LDAPi,sum,"LDAPi")+Atomic_situation(FormatString,sum,"FormatString") + Atomic_situation(BufferOverflow,sum,"BufferOverflow")

      Completeness = Atomic_situation(XSS,sum,"XSS") + Atomic_situation(CRLFi,sum,"CRLFi")

      Controllability = Atomic_situation(SSI, sum, "SSI")

      li=[Jurisdiction/12.0,Completeness/12.0,Controllability/5.0]
      return li


def calculate_All(objectList):
   li=calculate_Three(objectList)
   sum = 100-(li[0]**6.1+li[1]**8.5+li[2]**5.5)/8000
   return sum

def calculate_One(objectList):
   SQLi = objectList.setdefault('SQLi', 0)
   XSS = objectList.setdefault('XSS', 0)
   SSI = objectList.setdefault('SSI', 0)
   BufferOverflow = objectList.setdefault('BufferOverflow', 0)
   CRLFi = objectList.setdefault('CRLFi', 0)
   XPath = objectList.setdefault('XPath', 0)
   LDAPi = objectList.setdefault('LDAPi', 0)
   FormatString = objectList.setdefault('FormatString', 0)
   anomalous = objectList.setdefault('anomalous', 0)
   normal = objectList.setdefault('normal', 0)
   sum = SQLi+XSS+SSI+BufferOverflow+CRLFi+XPath+LDAPi+FormatString+anomalous+normal
   list_all = []
   list_one = ["SQLi",SQLi / sum,w["SQLi"],SQLi,Atomic_situation(SQLi,sum,"SQLi")]
   print(list_one)
   list_all.append(list_one)
   list_one = ["XSS",  XSS / sum, w["XSS"], XSS, Atomic_situation(XSS,sum,"XSS")]
   list_all.append(list_one)
   list_one = ["SSI", SSI / sum, w["SSI"], SSI, Atomic_situation(SSI,sum,"SSI")]
   list_all.append(list_one)
   list_one = ["BufferOverflow", BufferOverflow / sum, w["BufferOverflow"], BufferOverflow, Atomic_situation(BufferOverflow,sum,"BufferOverflow")]
   list_all.append(list_one)
   list_one = ["CRLFi", CRLFi / sum, w["CRLFi"], CRLFi,Atomic_situation(CRLFi, sum, "CRLFi")]
   list_all.append(list_one)
   list_one = ["XPath", XPath / sum, w["XPath"], XPath, Atomic_situation(XPath,sum,"XPath")]
   list_all.append(list_one)
   list_one = ["LDAPi", LDAPi / sum, w["LDAPi"], LDAPi, Atomic_situation(LDAPi,sum,"LDAPi")]
   list_all.append(list_one)
   list_one = ["FormatString", FormatString / sum, w["FormatString"], FormatString, Atomic_situation(FormatString,sum,"FormatString")]
   list_all.append(list_one)
   return list_all

def Atomic_situation(value,sum,label):
   if value == 0:
      return 0
   else:
      return -1/log(value/sum,e)*w[label]
