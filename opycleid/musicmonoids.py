# -*- coding: utf-8 -*-

################################################
###### Copyright (c) 2016, Alexandre Popoff 
###

import numpy as np
from monoidaction import MonoidAction

################################################
###### NOLL MONOID
###

class Noll_Monoid(MonoidAction):
    def __init__(self):
        self.objects = {"C":0,"Cs":1,"D":2,"Eb":3,"E":4,"F":5,"Fs":6,"G":7,"Gs":8,"A":9,"Bb":10,"B":11}

        F = np.zeros((12,12),dtype=bool)
        for i in range(12):
            F[(3*i+7)%12,i] = True

        G = np.zeros((12,12),dtype=bool)
        for i in range(12):
            G[(8*i+4)%12,i] = True
        
        self.generators = {"f":F,"g":G}
        self.generate_monoid()


################################################
###### TI GROUP FOR PITCH CLASSES
###

class TI_Group_PC(MonoidAction):
    def __init__(self):
        self.objects = {"C":0,"Cs":1,"D":2,"Eb":3,"E":4,"F":5,"Fs":6,"G":7,"Gs":8,"A":9,"Bb":10,"B":11}
        self.SIMPLY_TRANSITIVE=False

        T = np.zeros((12,12),dtype=bool)
        for i in range(12):
                T[(i+1)%12,i]=True

        I = np.zeros((12,12),dtype=bool)
        for i in range(12):
                I[(-i)%12,i]=True
        
        self.generators = {"T^1":T,"I^0":I}
        self.operations = {"e":np.eye(12,dtype=bool),"I^0":I}
        for i in range(1,12):
                x = self.operations['e']
                for j in range(i):
                        x = x.dot(T)
                self.operations["T^"+str(i)] = x
                self.operations["I^"+str(i)] = x.dot(I)


################################################
###### TI GROUP FOR TRIADS
###

class TI_Group_Triads(MonoidAction):
    def __init__(self):
        self.objects = {"C":0,"Cs":1,"D":2,"Eb":3,"E":4,"F":5,"Fs":6,"G":7,"Gs":8,"A":9,"Bb":10,"B":11,
                                        "c":12,"cs":13,"d":14,"eb":15,"e":16,"f":17,"fs":18,"g":19,"gs":20,"a":21,"bb":22,"b":23}
        self.SIMPLY_TRANSITIVE=True

        T = np.zeros((24,24),dtype=bool)
        for i in range(12):
                T[(i+1)%12,i]=True
                T[12+(i+1)%12,i+12]=True

        I = np.zeros((24,24),dtype=bool)
        for i in range(12):
                I[(5-i)%12 + 12,i]=True
                I[(5-i)%12, i+12]=True
        
        self.generators = {"T^1":T,"I^0":I}
        self.operations = {"e":np.eye(24,dtype=bool),"I^0":I}
        for i in range(1,12):
                x = self.operations['e']
                for j in range(i):
                        x = x.dot(T)
                self.operations["T^"+str(i)] = x
                self.operations["I^"+str(i)] = x.dot(I)

################################################
###### PRL GROUP
###

class PRL_Group(MonoidAction):
    def __init__(self):
        self.objects = {"C":0,"Cs":1,"D":2,"Eb":3,"E":4,"F":5,"Fs":6,"G":7,"Gs":8,"A":9,"Bb":10,"B":11,
                                        "c":12,"cs":13,"d":14,"eb":15,"e":16,"f":17,"fs":18,"g":19,"gs":20,"a":21,"bb":22,"b":23}
        self.SIMPLY_TRANSITIVE=True

        L = np.zeros((24,24),dtype=bool)
        for i in range(12):
                L[(i+4)%12 + 12,i]=True
                L[(i+8)%12,12+i]=True

        R = np.zeros((24,24),dtype=bool)
        for i in range(12):
                R[(i+9)%12 + 12,i]=True
                R[(i+3)%12,12+i]=True
        
        self.generators = {"L":L,"R":R}
        self.operations = {"e":np.eye(24,dtype=bool),"R":R}
        RL = R.dot(L)
        for i in range(1,12):
                x = self.operations['e']
                for j in range(i):
                        x = x.dot(RL)
                self.operations["(RL)^"+str(i)] = x
                self.operations["(RL)^"+str(i)+"R"] = x.dot(R)


################################################
###### HOOK's UTT GROUP FOR TRIADS
###

class UTT_Group(MonoidAction):
    def __init__(self):
        self.objects = {"C":0,"Cs":1,"D":2,"Eb":3,"E":4,"F":5,"Fs":6,"G":7,"Gs":8,"A":9,"Bb":10,"B":11,
                                        "c":12,"cs":13,"d":14,"eb":15,"e":16,"f":17,"fs":18,"g":19,"gs":20,"a":21,"bb":22,"b":23}
        self.SIMPLY_TRANSITIVE=False

        T = np.zeros((24,24),dtype=bool)
        for i in range(12):
                T[(i+1)%12,i]=True
                T[i+12,i+12]=True

        I = np.zeros((24,24),dtype=bool)
        for i in range(12):
                I[i + 12,i]=True
                I[i, i+12]=True
        
        self.generators = {"T":T,"I":I}
        self.generate_monoid()

        ## Quick rewriting of the operation names to conform to
        ## Hook's terminology for UTTs
        
        for x in self.operations.keys():
            op = [0,0,0]
            for j in x[::-1]:
                if j=="T":
                    op[op[2]]=op[op[2]]+1
                if j=="I":
                    op[2]=1-op[2]
            newkey = "<"+str(op[0])+","+str(op[1])+","+("+"*(op[2]==0)+"-"*(op[2]==1))+">"
            self.operations[newkey] = self.operations.pop(x)
        self.generators = {"<1,0,+>":T,"<0,0,->":I}

################################################
###### LEFT Z3Q8 GROUP FOR TRIADS
###

class Left_Z3Q8_Group(MonoidAction):
    def __init__(self):
        self.objects = {"C":0,"Cs":1,"D":2,"Eb":3,"E":4,"F":5,"Fs":6,"G":7,"Gs":8,"A":9,"Bb":10,"B":11,
                                        "c":12,"cs":13,"d":14,"eb":15,"e":16,"f":17,"fs":18,"g":19,"gs":20,"a":21,"bb":22,"b":23}
        self.SIMPLY_TRANSITIVE=True

        T = np.zeros((24,24),dtype=bool)
        for i in range(12):
                T[(i+1)%12,i]=True
                T[12+(i+1)%12,i+12]=True

        J = np.zeros((24,24),dtype=bool)
        for i in range(12):
                J[(-i)%12 + 12,i]=True
                J[(-i+6)%12, i+12]=True
        
        self.generators = {"T^1":T,"J^0":J}
        self.operations = {"e":np.eye(24,dtype=bool),"J^0":J}
        for i in range(1,12):
                x = self.operations['e']
                for j in range(i):
                        x = x.dot(T)
                self.operations["T^"+str(i)] = x
                self.operations["J^"+str(i)] = x.dot(J)

################################################
###### RIGHT Z3Q8 GROUP FOR TRIADS
###

class Right_Z3Q8_Group(MonoidAction):
    def __init__(self):
        self.objects = {"C":0,"Cs":1,"D":2,"Eb":3,"E":4,"F":5,"Fs":6,"G":7,"Gs":8,"A":9,"Bb":10,"B":11,
                                        "c":12,"cs":13,"d":14,"eb":15,"e":16,"f":17,"fs":18,"g":19,"gs":20,"a":21,"bb":22,"b":23}
        self.SIMPLY_TRANSITIVE=True

        T = np.zeros((24,24),dtype=bool)
        for i in range(12):
                T[(i+1)%12,i]=True
                T[12+(i-1)%12,i+12]=True

        J = np.zeros((24,24),dtype=bool)
        for i in range(12):
                J[i + 12,i]=True
                J[(i+6)%12, i+12]=True
        
        self.generators = {"T^1":T,"J^0":J}
        self.operations = {"e":np.eye(24,dtype=bool),"J^0":J}
        for i in range(1,12):
                x = self.operations['e']
                for j in range(i):
                        x = x.dot(T)
                self.operations["T^"+str(i)] = x
                self.operations["J^"+str(i)] = x.dot(J)

################################################
###### UPL MONOID
###

class UPL_Monoid(MonoidAction):
    def __init__(self):
        self.objects = {"C":0,"Cs":1,"D":2,"Eb":3,"E":4,"F":5,"Fs":6,"G":7,"Gs":8,"A":9,"Bb":10,"B":11,
                        "c":12,"cs":13,"d":14,"eb":15,"e":16,"f":17,"fs":18,"g":19,"gs":20,"a":21,"bb":22,"b":23,
                        "C_aug":24,"F_aug":25,"D_aug":26,"G_aug":27}
        
        P = np.zeros((28,28),dtype=bool)
        for i in range(12):
            P[i+12,i]=True
            P[i,i+12]=True
        for i in range(24,28):
            P[i,i]=True

        L = np.zeros((28,28),dtype=bool)
        for i in range(12):
            L[(i+4)%12+12,i]=True
            L[(i+8)%12,12+i]=True
        for i in range(24,28):
            L[i,i]=True

        U = np.zeros((28,28),dtype=bool)

        for i in range(12):
            U[24+(i%4),i]=True
            U[i,24+(i%4)]=True

            U[24+((i+3)%4),12+i]=True
            U[12+i,24+((i+3)%4)]=True

        self.generators = {"P":P,"L":L,"U":U}
        self.generate_monoid()

################################################
###### 	S-MONOID (Relation P_1,0)
###

class S_Monoid(MonoidAction):
    def __init__(self):
        self.objects = {"C":0,"Cs":1,"D":2,"Eb":3,"E":4,"F":5,"Fs":6,"G":7,"Gs":8,"A":9,"Bb":10,"B":11,
                        "c":12,"cs":13,"d":14,"eb":15,"e":16,"f":17,"fs":18,"g":19,"gs":20,"a":21,"bb":22,"b":23,
                        "C_aug":24,"F_aug":25,"D_aug":26,"G_aug":27}
        
        S = np.zeros((28,28),dtype=bool)

        for i in range(12):
            S[24+(i%4),i]=True
            S[i,24+(i%4)]=True

            S[24+((i+3)%4),12+i]=True
            S[12+i,24+((i+3)%4)]=True
            
            S[12+i,i]=True
            S[i,12+i]=True
            
            S[12+(i+4)%12,i]=True
            S[i,12+(i+4)%12]=True

        self.generators = {"S":S}
        self.generate_monoid()


################################################
###### 	T-MONOID (Relation P_2,0)
###

class T_Monoid(MonoidAction):
    def __init__(self):
        self.objects = {"C":0,"Cs":1,"D":2,"Eb":3,"E":4,"F":5,"Fs":6,"G":7,"Gs":8,"A":9,"Bb":10,"B":11,
                        "c":12,"cs":13,"d":14,"eb":15,"e":16,"f":17,"fs":18,"g":19,"gs":20,"a":21,"bb":22,"b":23,
                        "C_aug":24,"F_aug":25,"D_aug":26,"G_aug":27}
        
        T = np.zeros((28,28),dtype=bool)

        for i in range(12):
            T[(i+4)%12,i]=True
            T[i,(i+4)%12]=True
            
            T[(i+8)%12,i]=True
            T[i,(i+8)%12]=True
            
            T[12+(i+1)%12,i]=True
            T[i,12+(i+1)%12]=True

            T[12+(i+5)%12,i]=True
            T[i,12+(i+5)%12]=True

            T[24+((i+3)%4),i]=True
            T[i,24+((i+3)%4)]=True
               
        for i in range(12):
            T[24+(i%4),12+i]=True
            T[12+i,24+(i%4)]=True

            T[12+(i+4)%12,12+i]=True
            T[12+i,12+(i+4)%12]=True
            
            T[12+(i+8)%12,12+i]=True
            T[12+i,12+(i+8)%12]=True

        self.generators = {"T":T}
        self.generate_monoid()

################################################
###### 	K-MONOID (Relation P_2,1)
###

class K_Monoid(MonoidAction):
    def __init__(self):
        self.objects = {"C":0,"Cs":1,"D":2,"Eb":3,"E":4,"F":5,"Fs":6,"G":7,"Gs":8,"A":9,"Bb":10,"B":11,
                        "c":12,"cs":13,"d":14,"eb":15,"e":16,"f":17,"fs":18,"g":19,"gs":20,"a":21,"bb":22,"b":23,
                        "C_aug":24,"F_aug":25,"D_aug":26,"G_aug":27}
        
        K = np.zeros((28,28),dtype=bool)

        for i in range(12):
            K[12+(i+3)%12,i]=True
            K[i,12+(i+3)%12]=True
            
            K[12+(i+11)%12,i]=True
            K[i,12+(i+11)%12]=True

            K[24+((i+1)%4),i]=True
            K[i,24+((i+1)%4)]=True

            K[24+((i+2)%4),12+i]=True
            K[12+i,24+((i+2)%4)]=True

        self.generators = {"K":K}
        self.generate_monoid()

################################################
###### 	W-MONOID (Relation P_1,2)
###

class W_Monoid(MonoidAction):
    def __init__(self):
        self.objects = {"C":0,"Cs":1,"D":2,"Eb":3,"E":4,"F":5,"Fs":6,"G":7,"Gs":8,"A":9,"Bb":10,"B":11,
                        "c":12,"cs":13,"d":14,"eb":15,"e":16,"f":17,"fs":18,"g":19,"gs":20,"a":21,"bb":22,"b":23,
                        "C_aug":24,"F_aug":25,"D_aug":26,"G_aug":27}
        
        W = np.zeros((28,28),dtype=bool)

        for i in range(12):
            W[12+(i+2)%12,i]=True
            W[i,12+(i+2)%12]=True
            
            W[12+(i+6)%12,i]=True
            W[i,12+(i+6)%12]=True

            W[24+((i+2)%4),i]=True
            W[i,24+((i+2)%4)]=True

            W[24+((i+1)%4),12+i]=True
            W[12+i,24+((i+1)%4)]=True

        self.generators = {"W":W}
        self.generate_monoid()
	
################################################
###### 	ST-MONOID
###

class ST_Monoid(MonoidAction):
    def __init__(self):
        self.objects = {"C":0,"Cs":1,"D":2,"Eb":3,"E":4,"F":5,"Fs":6,"G":7,"Gs":8,"A":9,"Bb":10,"B":11,
                        "c":12,"cs":13,"d":14,"eb":15,"e":16,"f":17,"fs":18,"g":19,"gs":20,"a":21,"bb":22,"b":23,
                        "C_aug":24,"F_aug":25,"D_aug":26,"G_aug":27}
        

        S = np.zeros((28,28),dtype=bool)

        for i in range(12):
            S[24+(i%4),i]=True
            S[i,24+(i%4)]=True

            S[24+((i+3)%4),12+i]=True
            S[12+i,24+((i+3)%4)]=True
            
            S[12+i,i]=True
            S[i,12+i]=True
            
            S[12+(i+4)%12,i]=True
            S[i,12+(i+4)%12]=True

        T = np.zeros((28,28),dtype=bool)

        for i in range(12):
            T[(i+4)%12,i]=True
            T[i,(i+4)%12]=True
            
            T[(i+8)%12,i]=True
            T[i,(i+8)%12]=True
            
            T[12+(i+1)%12,i]=True
            T[i,12+(i+1)%12]=True

            T[12+(i+5)%12,i]=True
            T[i,12+(i+5)%12]=True

            T[24+((i+3)%4),i]=True
            T[i,24+((i+3)%4)]=True
               
        for i in range(12):
            T[24+(i%4),12+i]=True
            T[12+i,24+(i%4)]=True

            T[12+(i+4)%12,12+i]=True
            T[12+i,12+(i+4)%12]=True
            
            T[12+(i+8)%12,12+i]=True
            T[12+i,12+(i+8)%12]=True

        self.generators = {"S":S,"T":T}
        self.generate_monoid()
