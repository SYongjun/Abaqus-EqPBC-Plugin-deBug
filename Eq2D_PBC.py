# -*- coding: mbcs -*-
from abaqus import *
from abaqusConstants import *
#******************************************
def create_Eq_2D(A,B,C,D,eqName,Dir_Eq,myModel):
    myModel.Equation(name = eqName, terms=((1.0,A, Dir_Eq),(-1.0,B, Dir_Eq),(-1.0,C, Dir_Eq),(1.0,D, Dir_Eq))) 
        
#******************************************
#******************************************        
def keyX(elem):
    return elem[1]
def keyY(elem):
    return elem[2]
def keyZ(elem):
    return elem[3]
#******************************************
#******************************************
    
def PBC_Eq_2D(Edge_L,Edge_R,Edge_U,Edge_D,modelName):
    myModel = mdb.models[modelName]
    ass = myModel.rootAssembly
    LnodesO,RnodesO,UnodesO,DnodesO, = [],[],[],[]
    Lnodes,Rnodes,Unodes,Dnodes=[],[],[],[]
    for i in range(len(Edge_L)):
        for j in Edge_L[i].getNodes():
            Lnodes.append(j)
    for i in range(len(Edge_R)):
        for j in Edge_R[i].getNodes():
            Rnodes.append(j)
    for i in range(len(Edge_U)):
        for j in Edge_U[i].getNodes():
            Unodes.append(j)
    for i in range(len(Edge_D)):
        for j in Edge_D[i].getNodes():
            Dnodes.append(j)
#******************************************           
    for i in Lnodes:
        xtemp = [int(i.label),float( i.coordinates[0]),float(i.coordinates[1]),float(i.coordinates[2]),str(i.instanceName)]
        LnodesO.append(xtemp)
        del xtemp       
    for i in Rnodes:
        xtemp = [int(i.label),float( i.coordinates[0]),float(i.coordinates[1]),float(i.coordinates[2]),str(i.instanceName)]
        RnodesO.append(xtemp)  
        del xtemp
    for i in Unodes:
        xtemp = [int(i.label),float( i.coordinates[0]),float(i.coordinates[1]),float(i.coordinates[2]),str(i.instanceName)]
        UnodesO.append(xtemp)
        del xtemp
    for i in Dnodes:
        xtemp = [int(i.label),float( i.coordinates[0]),float(i.coordinates[1]),float(i.coordinates[2]),str(i.instanceName)]
        DnodesO.append(xtemp)
        del xtemp
    LnodesO.sort(key=keyY)
    RnodesO.sort(key=keyY)
    UnodesO.sort(key=keyX)
    DnodesO.sort(key=keyX)
#******************************************    
    Ln,Rn,Un,Dn=[],[],[],[]
    for i in range(len(LnodesO)-1):
        if (LnodesO[i][2]-LnodesO[i+1][2])**2<0.0001:
            continue
        Ln.append(LnodesO[i])
    Ln.append(LnodesO[-1])
    for i in range(len(RnodesO)-1):
        if (RnodesO[i][2]-RnodesO[i+1][2])**2<0.0001:
            continue
        Rn.append(RnodesO[i])
    Rn.append(RnodesO[-1])
    for i in range(len(UnodesO)-1):
        if (UnodesO[i][1]-UnodesO[i+1][1])**2<0.0001:
            continue
        Un.append(UnodesO[i])
    Un.append(UnodesO[-1])
    for i in range(len(DnodesO)-1):
        if (DnodesO[i][1]-DnodesO[i+1][1])**2<0.0001:
            continue
        Dn.append(DnodesO[i])
    Dn.append(DnodesO[-1])
#******************************************
#******************************************    
    LL=RnodesO[0][1]-LnodesO[0][1]
    HH=UnodesO[0][2]-DnodesO[0][2]
#******************************************
#******************************************
    for i in ass.features.keys():
        if i.startswith('RP'):
            del ass.features['%s' % (i)]
    Cx=(RnodesO[-1][1]+LnodesO[-1][1])/2 
    Cy=(RnodesO[-1][2]+RnodesO[0][2])/2    
    rp1=ass.ReferencePoint(point = (1.1*RnodesO[-1][1],Cy,0))
    rp2=ass.ReferencePoint(point = (Cx,1.1*RnodesO[-1][1],0))
    r1 = ass.referencePoints                        
    d=len(r1)
    
    for i in r1.keys():
        refPoints1=(r1[i], )
        ass.Set(referencePoints=refPoints1, name='Ctrl_P'+str(d))
        d=d-1
        
#********************************************************************************   
    LD,RD,LU = [Ln[0][0]],[Rn[0][0]],[Un[0][0]]
    ass.SetFromNodeLabels(name = 'LD' , nodeLabels=((Ln[0][4],LD),))
    ass.SetFromNodeLabels(name = 'RD' , nodeLabels=((Rn[0][4],RD),))
    ass.SetFromNodeLabels(name = 'LU' , nodeLabels=((Un[0][4],LU),))
#******************************************
#******************************************    
    for i in range(1,len(Ln)-1):
        con1='eqXX'+str(i)
        con2='eqXY'+str(i)
        Lnum = 'Lnode'+str(i)
        Rnum = 'Rnode'+str(i)
        ass.SetFromNodeLabels(name = Lnum , nodeLabels=((Ln[i][4],[Ln[i][0]]),))
        ass.SetFromNodeLabels(name = Rnum , nodeLabels=((Rn[i][4],[Rn[i][0]]),))
        create_Eq_2D(Rnum,Lnum,'RD','LD',con1,1,myModel)
        create_Eq_2D(Rnum,Lnum,'RD','LD',con2,2,myModel)
#******************************************
#******************************************        
    for i in range(1,len(Un)):
        con1='eqYX'+str(i)
        con2='eqYY'+str(i)
        Unum = 'Unode'+str(i)
        Dnum = 'Dnode'+str(i)
        ass.SetFromNodeLabels(name = Unum , nodeLabels=((Un[i][4],[Un[i][0]]),))
        ass.SetFromNodeLabels(name = Dnum , nodeLabels=((Dn[i][4],[Dn[i][0]]),))
        create_Eq_2D(Unum,Dnum,'LU','LD',con1,1,myModel)
        create_Eq_2D(Unum,Dnum,'LU','LD',con2,2,myModel) 
    myModel.Equation(name='ctrl_E11',terms=((1.0,'RD',1),(-1.0,'LD', 1),(-1.0*LL,'Ctrl_P1', 1)))
    myModel.Equation(name='ctrl_E12',terms=((1.0,'RD',2),(-1.0,'LD', 2),(-1.0*LL,'Ctrl_P1', 2)))
    myModel.Equation(name='ctrl_E22',terms=((1.0,'LU',2),(-1.0,'LD', 2),(-1.0*HH,'Ctrl_P2', 2)))
    myModel.Equation(name='ctrl_E21',terms=((1.0,'LU',1),(-1.0,'LD', 1),(-1.0*HH,'Ctrl_P2', 1))) 