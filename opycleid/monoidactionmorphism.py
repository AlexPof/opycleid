# -*- coding: utf-8 -*-

################################################
###### Copyright (c) 2016, Alexandre Popoff
###

import numpy as np
from .categoryaction import MonoidAction, CatMorphism

class MonoidActionMorphism:

    def __init__(self,monoidaction_source,monoid_action_dest,monoid_morphism,nat_trans_mapping):
        """Initializes a morphism of monoid action class

        Variables
        ----------
            - monoidaction_source:  the source monoid action of the morphism
            - monoidaction_dest:    the destination monoid action of the morphism
            - monoid_morphism:      a monoid morphism, defining how
                                    operations are transformed
                                    This is a dictionary, the keys of which
                                    are operations in monoidaction_source,
                                    the values of which are operations
                                    in monoidaction_dest
            - nat_trans_mapping:    a natural transformation, defining how
                                    the musical elements are transformed.
                                    This is a dictionary, the keys of which are
                                    elements in monoidaction_source, the values
                                    of which are list of elements in monoidaction_dest
        """
        if not isinstance(monoidaction_source,MonoidAction):
           raise Exception("Source is not a valid monoid action\n")
        if not isinstance(monoid_action_dest,MonoidAction):
            raise Exception("Target is not a valid monoid action\n")
        self.monoidaction_source = monoidaction_source
        self.monoidaction_dest = monoid_action_dest
        self.monoid_morphism = monoid_morphism

        N = CatMorphism("N",
                        self.monoidaction_source.get_object(),
                        self.monoidaction_dest.get_object())
        N.set_mapping(nat_trans_mapping)

        self.nat_trans = N


    def is_monoidmorphism_valid(self):
        """Checks if the specified monoid morphism is a valid one.
           We should have f(g2*g1)=f(g2)*f(g1).

        Returns
        -------
        A boolean indicating if this is a valid monoid morphism.
        """
        for op1 in self.monoidaction_source.operations:
            for op2 in self.monoidaction_source.operations:
                image_op_1 = self.monoid_morphism[self.monoidaction_source.mult(op1,op2)]
                image_op_2 = self.monoidaction_dest.mult(self.monoid_morphism[op1],
                                                         self.monoid_morphism[op2])
                if not image_op_1 == image_op_2:
                    return False
        return True

    def is_nattransformation_valid(self):
        """Checks if the specified lax natural transformation is a valid one.
           In particular, the commutativity condition
           of the natural transformation should be respected.
           In the 2-category Rel, given a lax natural transformation N between
           two functors F and G, this means that there should be a 2-morphism
           from N_Y*F(f) to G(f)*N_X (i.e. the relation N_Y*F(f) is included in
           G(f)*N_X) for all morphisms f.

        Returns
        -------
        A boolean indicating if this is a valid lax natural transformation.
        """

        ## Check the validity of the lax natural transformation square for all operations of the monoid
        for name_x,x in self.monoidaction_source.operations.items():
            K = self.nat_trans * x
            L = self.monoidaction_dest.operations[self.monoid_morphism[name_x]] * self.nat_trans
            if not K<L:
                return False

        return True

    def is_valid(self):
        """Checks if this is a valid morphism of the monoid action functor.

        Returns
        -------
        A boolean indicating if this is a valid morphism.
        """
        return self.is_monoidmorphism_valid() and self.is_nattransformation_valid()
