# -*- coding: utf-8 -*-

################################################
###### Copyright (c) 2016, Alexandre Popoff 
###

import numpy as np
from monoidaction import MonoidAction

class MonoidActionMorphism:

    def __init__(self,monoidaction_source,monoid_action_dest,monoid_morphism,nat_trans):
        """Initializes a morphism of monoid action class
        
        Variables
        ----------
            - monoidaction_source:  the source monoid action of the morphism
            - monoidaction_dest:    the destination monoid action of the morphism
            - monoid_morphism:      a monoid morphism, defining how operations are transformed
                                    This is a dictionary, the keys of which are operations in monoidaction_source, the values of which are operations in monoidaction_dest
            - nat_trans:            a natural transformation, defining how the musical elements are transformed.
                                    This is a dictionary, the keys of which are objects in monoidaction_source, the values of which are objects in monoidaction_dest
        """
        self.monoidaction_source = monoidaction_source
        self.monoidaction_dest = monoid_action_dest
        self.monoid_morphism = monoid_morphism
        self.nat_trans = nat_trans
        

    def is_monoidmorphism_valid(self):
        """Checks if the specified monoid morphism is a valid one.
           We should have f(g2*g1)=f(g2)*f(g1).

        Returns
        -------
        A boolean indicating if this is a valid monoid morphism. 
        """
        for op1 in self.monoidaction_source.operations.keys():
            for op2 in self.monoidaction_source.operations.keys():
                image_op_1 = self.monoid_morphism[self.monoidaction_source.mult(op1,op2)]
                image_op_2 = self.monoidaction_dest.mult(self.monoid_morphism[op1],self.monoid_morphism[op2])
                if not image_op_1 == image_op_2:
                    return False
        return True

    def is_nattransformation_valid(self):
        """Checks if the specified natural transformation is a valid one.
           In particular, the commutativity condition of the natural transformation should be respected.

        Returns
        -------
        A boolean indicating if this is a valid natural transformation. 
        """
        ## Build the matrix representation (permutation matrix) corresponding to the natural isomorphism given by nat_trans
        nat_trans_matrix = np.zeros((len(self.monoidaction_dest.objects),len(self.monoidaction_source.objects)),dtype=bool)
        for x in self.monoidaction_source.objects.keys():
            nat_trans_matrix[self.monoidaction_dest.objects[self.nat_trans[x]],self.monoidaction_source.objects[x]]=True
        
        ## Check the commutativity of the natural transformation square for all operations of the monoid        
        for x in self.monoidaction_source.operations.keys():
            K = np.dot(nat_trans_matrix,self.monoidaction_source.operations[x])
            L = np.dot(self.monoidaction_dest.operations[self.monoid_morphism[x]],nat_trans_matrix)

            if not np.array_equal(K,L):
                return False

        return True

    def is_valid(self):
        """Checks if this is a valid morphism of the monoid action functor.
  
        Returns
        -------
        A boolean indicating if this is a valid morphism. 
        """
        return self.is_monoidmorphism_valid() and self.is_nattransformation_valid()
