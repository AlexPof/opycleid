# -*- coding: utf-8 -*-

################################################
###### Copyright (c) 2016, Alexandre Popoff 
###

import numpy as np
import itertools

################################################
###### GENERIC CLASS FOR MONOID ACTION
###

class MonoidAction:
    def __init__(self):
        self.objects = {}
        self.generators = {}
        self.operations = {}
        self.SIMPLY_TRANSITIVE=None

	############
	###### TRANSFORMATIONAL MUSIC THEORY METHODS

    def apply_operation(self,operation_name,element_name):
        idx_element = self.objects[element_name]
        op = self.operations[operation_name]
        list_indices = np.where(op[:,idx_element])[0]
        return [x for x in self.objects.keys() for y in list_indices if self.objects[x]==y]

    def get_operation(self,elem_1,elem_2):
        idx_1 = self.objects[elem_1]
        idx_2 = self.objects[elem_2]

        return [op for op in self.operations if self.operations[op][idx_2,idx_1] ]

	############
	###### MONOID STRUCTURE

    def add_generator(self,gen_name,gen_matrix):
        self.generators[gen_name] = gen_matrix

    def mult(self,op_2,op_1):
        m = (self.operations[op_2].dot(self.operations[op_1])>0)
        for x in self.operations:
            if np.array_equal(m,self.operations[x]):
                return x

    def generate_monoid(self):
        self.operations = self.generators.copy()
        self.operations["e"] = np.eye(len(self.objects),dtype=bool)
        new_liste = self.generators.copy()
        added_liste = self.generators.copy()

        while(len(added_liste)>0):
            added_liste = {}
            for name_x in new_liste.keys():
                for name_g in self.generators.keys():
                    elem_name = name_g+name_x
                    elem_matrix = (self.generators[name_g].dot(new_liste[name_x])>0)
                    c=0
                    for name_y in self.operations.keys():
                        if np.array_equal(self.operations[name_y],elem_matrix):
                            c=1
                    if c==0:
                        added_liste[elem_name] = elem_matrix
                        self.operations[elem_name] = elem_matrix
            new_liste = added_liste


    def get_automorphisms(self):
        ## Returns all automorphisms of the monoid as a list of dictionaries.
        ## Each dictionary maps the generators (the keys) to their image in the monoid (the values) 

        l1 = self.generators.keys()
        l2 = self.operations.keys()
        list_automorphisms = []
        
        ## Get all maps from the generator set to itself
        for mapping in itertools.permutations(l2,len(l1)):
            ## Builds a dictionary representing the map...
            autom_dict={}
            for x,y in zip(l1,mapping):
                autom_dict[x]=y
            ## Tests if the given map of generators is indeed an automorphism...
            if self.is_automorphism(autom_dict):
                list_automorphisms.append(autom_dict)
        return list_automorphisms

    def is_automorphism(self,autom_dict,full_map=False):
        new_liste = self.generators.keys()
        added_liste = self.generators.keys()
        full_mapping = autom_dict.copy()
        full_mapping["e"]="e"

        ## This is a variant of the monoid generation method.
        ## It generates the monoid and their images by the map of generators.
        ## If it does not give a multi-valued function, and if it generates the same number of elements
        ## then it is a bijection, hence a valid automorphism

        while(len(added_liste)>0):
            added_liste = []
            for name_x in new_liste:
                for name_g in self.generators.keys():
                    name_product = self.mult(name_g,name_x)
                    name_imageproduct = self.mult(full_mapping[name_g],full_mapping[name_x])
                    if not name_product in full_mapping.keys():
                        added_liste.append(name_product)
                        full_mapping[name_product] = name_imageproduct
                    else:
                        ## If the generated element already exists, we check that its existing image corresponds
                        ## to the image which has just been calculated
                        if not full_mapping[name_product] == name_imageproduct:
                            ## We have a multi-valued function so the algorithm stops there
                            return (False,None)
            new_liste = added_liste[:]

        if not len(np.unique(full_mapping.values()))==len(self.operations.keys()):
            return (False,None)
        else:
            if full_map:
                return (True,full_mapping)
            else:
                return (True,None)

    def is_action_automorphism(self,autom_dict,nat_trans):
		## Build the matrix representation (permutation matrix) corresponding to the natural isomorphism given by nat_trans
        nat_trans_matrix = np.zeros((len(self.objects),len(self.objects)),dtype=bool)
        for x in self.objects.keys():
            nat_trans_matrix[self.objects[nat_trans[x]],self.objects[x]]=True
        
		## Check the commutativity of the natural transformation square for all operations of the monoid        
        for x in self.operations.keys():
            K = np.dot(nat_trans_matrix,self.operations[x])
            L = np.dot(self.operations[autom_dict[x]],nat_trans_matrix)

            if not np.array_equal(K,L):
                return False

        return True
            


	############
	###### ALGEBRAIC STRUCTURE AND GREEN'S RELATIONS

    def is_leftIdeal(self,S):
        for m in S.keys():
            for f in self.operations.keys():
                t = self.mult(f,m)
                if not t in S:
                    return False
        return True
	
    def element_Rclass(self,op_name):
        list_Req = []
        I1 = np.unique([self.mult(op_name,x) for x in self.operations.keys()])
        for op in self.operations.keys():
            I2 = np.unique([self.mult(op,x) for x in self.operations.keys()])
            if sorted(I2) == sorted(I1):
                list_Req.append(op)
        return list_Req

    def element_Lclass(self,op_name):
        list_Req = []
        I1 = np.unique([self.mult(x,op_name) for x in self.operations.keys()])
        for op in self.operations.keys():
            I2 = np.unique([self.mult(x,op) for x in self.operations.keys()])
            if sorted(I2) == sorted(I1):
                list_Req.append(op)
        return list_Req

    def get_Rclasses(self):
        list_op = zip(self.operations.keys(),[0]*len(self.operations.keys()))
        R_classes = []
        for x,visited in list_op:
            if not visited:
                R_class = self.element_Rclass(x)
                R_classes.append(R_class)
                for i,(y,flag) in enumerate(list_op):
                    if y in R_class:
                        list_op[i]=(y,1)
        return R_classes

    def get_Lclasses(self):
        list_op = zip(self.operations.keys(),[0]*len(self.operations.keys()))
        L_classes = []
        for x,visited in list_op:
            if not visited:
                L_class = self.element_Lclass(x)
                L_classes.append(L_class)
                for i,(y,flag) in enumerate(list_op):
                    if y in L_class:
                        list_op[i]=(y,1)
        return L_classes


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
