# -*- coding: utf-8 -*-

################################################
###### Copyright (c) 2016, Alexandre Popoff
###

import numpy as np
import itertools
from .categoryaction import *

class SetRigElement(object):
    def __init__(self,monoid):
        if not isinstance(monoid,MonoidAction):
            raise Exception("A set rig element should be initialized with an instance of monoid")
        self.monoid = monoid
        self.element = set([])

    def set_value(self,elem_list):
        if not len(elem_list):
            self.element = set([])
            return self
        for x in elem_list:
            if x in self.monoid.get_objects()[0][1].get_elements():
                self.element = self.element.union(set([x]))
            else:
                raise Exception("Not a valid element")
        return self

    def __add__(self,rhs):
        if not isinstance(rhs,SetRigElement):
            raise Exception("RHS should be a set rig element")
        new_vector = SetRigElement(self.monoid)
        new_vector.element = self.element.union(rhs.element)
        return new_vector

    def __eq__(self,rhs):
        return self.element==rhs.element

    def __repr__(self):
        c="+".join(list(self.element))
        if not len(c):
            c=u"∅"
        return c
    def __str__(self):
        c="+".join(list(self.element))
        if not len(c):
            c=u"∅"
        return c


class MonoidRigElement(object):
    def __init__(self,monoid):
        if not isinstance(monoid,MonoidAction):
            raise Exception("A monoid rig element should be initialized with an instance of MonoidAction")
        self.monoid = monoid
        self.element = set([])

    def set_value(self,group_elem_list):
        if not len(group_elem_list):
            self.element = set([])
            return self
        for x in group_elem_list:
            if x in [y[0] for y in self.monoid.get_morphisms()]:
                self.element = self.element.union(set([x]))
            else:
                raise Exception("Not a valid operation")
        return self

    def __add__(self,rhs):
        if not isinstance(rhs,MonoidRigElement):
            raise Exception("RHS should be a monoid rig element")
        new_grouprig_element = MonoidRigElement(self.monoid)
        new_grouprig_element.element = self.element.union(rhs.element)
        return new_grouprig_element

    def __mul__(self,rhs):
        if isinstance(rhs,MonoidRigElement):
            new_grouprigelement = MonoidRigElement(self.monoid)
            mult_list = [self.monoid.mult(k1,k2) for k1 in self.element for k2 in rhs.element]
            new_grouprigelement.set_value(mult_list)
            return new_grouprigelement
        if isinstance(rhs,SetRigElement):
            new_vector = SetRigElement(rhs.monoid)
            mult_list = [self.monoid.apply_operation(m,x)[0] for m in self.element for x in rhs.element]
            new_vector.set_value(mult_list)
            return new_vector

    def __eq__(self,rhs):
        return self.element==rhs.element

    def __repr__(self):
        c="+".join(list(self.element))
        if not len(c):
            c=u"∅"
        return c
    def __str__(self):
        c="+".join(list(self.element))
        if not len(c):
            c=u"∅"
        return c


####################################################


class MatrixNetwork(object):
    def __init__(self):
        self.monoid = None
        self.matrix = None
        self.vector = None
        
    def set_network(self,matrix,vector):
        assert matrix==matrix@matrix, "Network matrix should be idempotent"
        assert vector==matrix@vector, "Vector should be invariant by matrix application"
        
        self.matrix = matrix
        self.vector = vector
        
        return self
        
    def from_generators(self,generators,vector,return_monoid=False):
        unit_matrix = MonoidRigMatrix(generators[0].shape,generators[0].monoid).set_unit()
        all_elements = [unit_matrix]
        added_elements = generators
        while len(added_elements)>0:
            for x in added_elements:
                all_elements.append(x)
            added_elements = []
            for g in generators:
                for el in all_elements:
                    new_matrix = g@el
                    if not np.any([x==new_matrix for x in all_elements]):
                        if not np.any([x==new_matrix for x in added_elements]):
                            added_elements.append(new_matrix)
        self.matrix = np.sum(all_elements)
        self.vector = self.matrix@vector
        
        if return_monoid:
            return self,all_elements
        else:
            return self

    def from_generator(self,matrix,vector,return_monoid=False):
        unit_matrix = MonoidRigMatrix(matrix.shape,matrix.monoid).set_unit()
        all_elements = [unit_matrix,matrix]
        added_elements = 2
        n=2
        while added_elements>0:
            added_elements = 0
            new_matrix = matrix**n
            if not np.any([x==new_matrix for x in all_elements]):
                all_elements.append(new_matrix)
                added_elements=1
        self.matrix = np.sum(all_elements)
        self.vector = self.matrix@vector
        
        if return_monoid:
            return self,all_elements
        else:
            return self
        
        
    def apply_categoryactionfunctor(self,catactionfunctor):
        assert isinstance(catactionfunctor,CategoryActionFunctor),"Not a CategoryActionFunctor"
        
        new_matrix = MonoidRigMatrix(self.matrix.shape,catactionfunctor.cat_action_target)
        new_vector = SetRigVector(self.vector.n,catactionfunctor.cat_action_target)
        
        for i in range(self.matrix.shape[0]):
            for j in range(self.matrix.shape[1]):
                image_elements = [catactionfunctor.cat_functor(x) for x in (self.matrix.matrix)[i,j].element]
                new_matrix.set_value((i,j),set(image_elements))
                
        for i in range(self.vector.n):
            image_elements = [y for x in (self.vector.vector)[i,0].element for y in catactionfunctor.nat_transform["."](x) ]
            new_vector.set_value([i],[set(image_elements)])
                
        return new_matrix,new_vector #MatrixNetwork().set_network(new_matrix,new_vector)
                    
        
    
        
####################################################



class MonoidRigMatrix(object):
    def __init__(self,shape, monoid):
        if shape[0]<1 or shape[1]<1:
            raise Exception("Matrix should have dimension at least 1")
        if not isinstance(monoid,MonoidAction):
            raise Exception("A monoid rig element should be initialized with an instance of MonoidAction")
        self.shape = shape
        self.monoid = monoid
        self.matrix = np.empty(self.shape,dtype=MonoidRigElement)
        self.set_zero()
                
    def set_unit(self):
        object_name = self.monoid.get_objects()[0][0]
        for i in range(self.shape[0]):
            self.set_value((i,i),["id_"+object_name])
        return self
        
    def set_zero(self):
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.matrix[i,j] = MonoidRigElement(self.monoid)
        return self

    def set_value(self,indices,value_list):
        if isinstance(indices,tuple):
            i,j = indices
            assert isinstance(i,int) and isinstance(j,int), "i and j should be both ints"
            self.matrix[i,j]=MonoidRigElement(self.monoid).set_value(value_list)
            return self
        elif isinstance(indices,list):
            assert len(indices)==len(value_list), "List lengths mismatch"
            for (i,j),x in zip(indices,value_list):
                assert isinstance(i,int) and isinstance(j,int), "i and j should be both ints"
                self.matrix[i,j]=MonoidRigElement(self.monoid).set_value(x)
            return self
        else:
            raise Exception("Unexpected types")
       

    def __add__(self,rhs):
        if not isinstance(rhs,MonoidRigMatrix):
            raise Exception("RHS should be a monoid rig matrix")
        if not self.shape==rhs.shape:
            raise Exception("Matrices should have identical shape")
        new_monoidrigmatrix = MonoidRigMatrix(self.shape,self.monoid)
        new_monoidrigmatrix.matrix = self.matrix+rhs.matrix
        return new_monoidrigmatrix

    def __mul__(self,rhs):
        if not isinstance(rhs,MonoidRigMatrix):
            raise Exception("RHS should be a monoid rig matrix")
        if not self.shape==rhs.shape:
            raise Exception("Matrices should have identical shape")
           
        new_monoidrigmatrix = MonoidRigMatrix(self.shape,self.monoid)
        new_monoidrigmatrix.matrix = self.matrix*rhs.matrix
        return new_monoidrigmatrix
       
    def __matmul__(self,rhs):
        if isinstance(rhs,MonoidRigMatrix):
            if not self.shape[1]==rhs.shape[0]:
                raise Exception("Matrices dimension mismatch")
            new_monoidrigmatrix = MonoidRigMatrix((self.shape[0],rhs.shape[1]),self.monoid)
            new_monoidrigmatrix.matrix = self.matrix@rhs.matrix
            return new_monoidrigmatrix
        if isinstance(rhs,SetRigVector):
            if not self.shape[1]==rhs.n:
                raise Exception("Matrix and vector dimension mismatch")
            new_vector = SetRigVector(self.shape[0],rhs.monoid)
            new_vector.vector = self.matrix@rhs.vector
            return new_vector
            
            
    def __pow__(self,n):
        assert isinstance(n,int) and n>=0,"Power should be a positive int"
        
        new_monoidrigmatrix = MonoidRigMatrix(self.shape,self.monoid).set_unit()
        for i in range(n):
            new_monoidrigmatrix = new_monoidrigmatrix@self
        return new_monoidrigmatrix
        
    def __eq__(self,rhs):
        return np.array_equal(self.matrix,rhs.matrix)

    def __repr__(self):
        return str(self.matrix)
        
    def __str__(self):
        return str(self.matrix)

class SetRigVector(object):
    def __init__(self,n: int, monoid):
        if n<1:
            raise Exception("Matrix should have dimension at least 1")
        if not isinstance(monoid,MonoidAction):
            raise Exception("A set rig element should be initialized with an instance of MonoidAction")
        self.n = n
        self.vector = np.empty((n,1),dtype=SetRigElement)
        self.monoid = monoid
        for i in range(n):
            self.vector[i,0] = SetRigElement(self.monoid)

    def set_value(self,indices,value_list):
        assert isinstance(indices,list), "Indices should be a list"
        for i,x in zip(indices,value_list):
            self.vector[i,0]=SetRigElement(self.monoid).set_value(x)
        return self

    def __add__(self,rhs):
        if not isinstance(rhs,SetRigVector):
            raise Exception("RHS should be a set rig vector")
        if not self.n==rhs.n:
            raise Exception("Vector dimension mismatch")
        new_setrigvector = SetRigVector(self.n,self.monoid)
        new_setrigvector.vector = self.vector+rhs.vector
        return new_monoidrigmatrix

    def __eq__(self,rhs):
        return np.array_equal(self.vector,rhs.vector)

    def __repr__(self):
        return str(self.vector)
        
    def __str__(self):
        return str(self.vector)    

class MatrixRigMonoid(object):
    def __init__(self,dict_gens):
        shape_check=[]
        for name,m in dict_gens.items():
            n = m.shape[0]
            monoid = m.monoid
            if not m.shape[0]==m.shape[1]:
                raise Exception("Matrices should be square")
            shape_check.append(m.shape)
        if len(set(shape_check))>1:
            raise Exception("Matrices should be of the same shape")
        self.n = n
        self.monoid = monoid
        self.morphisms = {}
        self.generators = dict_gens
        self.generate_category()

    def get_morphisms(self):
        """Returns the morphisms in the monoid.

        Parameters
        ----------
        None

        Returns
        -------
        A list of pairs (x,y), where:
            - x is the name of the morphism
            - y is the corresponding MonoidRigMatrix
        """
        return list(sorted(self.morphisms.items()))

    def _add_identities(self):
        """Automatically add identity morphisms on each object of the category
        action

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        iid = MonoidRigElement(self.monoid)
        iid.set_value(["id_."])

        ID = MonoidRigMatrix(shape=(self.n,self.n),monoid=self.monoid)
        ID = ID.set_value([[k,k,iid] for k in range(self.n)])
        
        self.morphisms["e"] = ID

    def generate_category(self):
        """Generates all morphisms in the monoid based on the given list of
        generators. The generation proceeds by successive multiplication of
        generators and morphisms until completion. This is suited to small
        monoids, but the performance would be prohibitive for very
        large monoids containing many morphisms.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.morphisms = self.generators.copy()
        self._add_identities()
        new_liste = self.generators.copy()
        added_liste = self.generators.copy()
        while(len(added_liste)>0):
            added_liste = {}
            for name_x,morphism_x in sorted(new_liste.items()):
                for name_g,morphism_g in self.get_generators():
                    new_morphism = morphism_g*morphism_x
                    if not new_morphism is None:
                        c=0
                        for name_y,morphism_y in self.get_morphisms():
                            if new_morphism==morphism_y:
                                c=1
                        if c==0:
                            added_liste[name_g+name_x] = new_morphism
                            self.morphisms[name_g+name_x] = new_morphism
            new_liste = added_liste

    def get_generators(self):
        """Returns the generators in the monoid.

        Parameters
        ----------
        None

        Returns
        -------
        A list of pairs (x,y), where:
            - x is the name of the generator
            - y is the corresponding instance of MonoidRigMatrix
        """
        return list(sorted(self.generators.items()))

    def mult(self,name_g,name_f):
        """Multiplies two morphisms and returns the corresponding morphism.

        Parameters
        ----------
        name_g, name_f: a string representing the names of the morphisms
                        to be multiplied.

        Returns
        -------
        A string representing the name of the morphism corresponding
        to name_g*name_f.
        """
        new_morphism = self.morphisms[name_g]*self.morphisms[name_f]
        if new_morphism is None:
            return new_morphism
        else:
            return [name_x for name_x,x in self.get_morphisms() if x==new_morphism][0]

    def element_Rclass(self,op_name):
        """Generates the R class for a given operation x in the monoid,
        i.e. all elements y of the monoid such that
        we have xRy for Green's R relation.
        Recall that we have xRy if xS=yS where S is the monoid.


        Parameters
        ----------
        op_name : a string describing an operation of the monoid.

        Returns
        -------
        A list of operations related to op_name by Green's R relation.
        """
        list_Req = []
        I1 = np.unique([self.mult(op_name,name_x) for name_x,x in self.get_morphisms()])
        for name_g,g in self.get_morphisms():
            I2 = np.unique([self.mult(name_g,name_x) for name_x,x in self.get_morphisms()])
            if sorted(I2) == sorted(I1):
                list_Req.append(name_g)
        return list_Req

    def element_Lclass(self,op_name):
        """Generates the L class for a given operation x in the monoid,
        i.e. all elements y of the monoid such that
        we have xLy for Green's L relation.
        Recall that we have xLy if Sx=Sy where S is the monoid.


        Parameters
        ----------
        op_name : a string describing an operation of the monoid.

        Returns
        -------
        A list of operations related to op_name by Green's L relation.
        """
        list_Req = []
        I1 = np.unique([self.mult(name_x,op_name) for name_x,x in self.get_morphisms()])
        for name_g,g in self.get_morphisms():
            I2 = np.unique([self.mult(name_x,name_g) for name_x,x in self.get_morphisms()])
            if sorted(I2) == sorted(I1):
                list_Req.append(name_g)
        return list_Req

    def get_Rclasses(self):
        """Computes all R classes for the monoid.

        Parameters
        ----------
        None

        Returns
        -------
        A list of lists, each list being an R class.
        """
        list_op = list(zip(sorted(self.morphisms.keys()),
                           [0]*len(self.morphisms.keys())))
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
        """Computes all L classes for the monoid.

        Parameters
        ----------
        None

        Returns
        -------
        A list of lists, each list being an L class.
        """
        list_op = list(zip(sorted(self.morphisms.keys()),
                           [0]*len(self.morphisms.keys())))
        L_classes = []
        for x,visited in list_op:
            if not visited:
                L_class = self.element_Lclass(x)
                L_classes.append(L_class)
                for i,(y,flag) in enumerate(list_op):
                    if y in L_class:
                        list_op[i]=(y,1)
        return L_classes

    def get_leftIdeals(self):
        """Computes all left ideals for the monoid.
        A left ideal is a subset X of the monoid S, such that for any operation
        m in the monoid, we have mX included in X.
        In other words, if x belongs to X, then Sx is included in X. Thus, any
        left ideal can be decomposed as the union of distinct L classes.

        Parameters
        ----------
        None

        Returns
        -------
        A list of lists, each list being a left ideal of the monoid.
        """
        leftIdeals = []

        L_classes = self.get_Lclasses()
        for i in range(len(L_classes)+1):
            for x in itertools.combinations(L_classes, i):
                subset = list(itertools.chain.from_iterable(x))
                if self.is_leftIdeal(subset):
                    leftIdeals.append(subset)

        return leftIdeals

    def is_leftIdeal(self,S):
        """Checks if a subset S is a left ideal.

        Parameters
        ----------
        S : list of operations in the monoid.

        Returns
        -------
        A boolean indicating if S is a left ideal.
        """
        for m in S:
            for name_f,f in self.get_morphisms():
                t = self.mult(name_f,m)
                if not t in S:
                    return False
        return True

    def get_rightIdeals(self):
        """Computes all right ideals for the monoid.
        A right ideal is a subset X of the monoid S, such that for any operation
        m in the monoid, we have Xm included in X.
        In other words, if x belongs to X, then xS is included in X.
        Thus, any right ideal can be decomposed as the union of distinct R classes.

        Parameters
        ----------
        None

        Returns
        -------
        A list of lists, each list being a right ideal of the monoid.
        """
        rightIdeals = []

        R_classes = self.get_Rclasses()
        for i in range(len(R_classes)+1):
            for x in itertools.combinations(R_classes, i):
                subset = list(itertools.chain.from_iterable(x))
                if self.is_rightIdeal(subset):
                    rightIdeals.append(subset)

        return rightIdeals

    def is_rightIdeal(self,S):
        """Checks if a subset S is a right ideal.

        Parameters
        ----------
        S : list of operations in the monoid.

        Returns
        -------
        A boolean indicating if S is a right ideal.
        """
        for m in S:
            for name_f,f in self.get_morphisms():
                t = self.mult(m,name_f)
                if not t in S:
                    return False
        return True
