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
	
    def add_objects(self,object_list):
        N = len(self.objects)
        for i,x in enumerate(object_list):
            self.objects[x]=i+N

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
            if self.is_automorphism(autom_dict)[0]:
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

    def get_leftIdeals(self):
        leftIdeals = []

        L_classes = self.get_Lclasses()
        for i in range(len(L_classes)+1):
            for x in itertools.combinations(L_classes, i):
                subset = list(itertools.chain.from_iterable(x))
                if self.is_leftIdeal(subset):
                    leftIdeals.append(subset)

        return leftIdeals
		
    def is_leftIdeal(self,S):
        for m in S:
            for f in self.operations.keys():
                t = self.mult(f,m)
                if not t in S:
                    return False
        return True
        
    def get_rightIdeals(self):
        rightIdeals = []

        R_classes = self.get_Rclasses()
        for i in range(len(R_classes)+1):
            for x in itertools.combinations(R_classes, i):
                subset = list(itertools.chain.from_iterable(x))
                if self.is_rightIdeal(subset):
                    rightIdeals.append(subset)

        return rightIdeals
		
    def is_rightIdeal(self,S):
        for m in S:
            for f in self.operations.keys():
                t = self.mult(m,f)
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

