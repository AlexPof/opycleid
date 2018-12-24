# -*- coding: utf-8 -*-

################################################
###### Copyright (c) 2016, Alexandre Popoff
###

import numpy as np
from .categoryaction import CategoryAction, MonoidAction, CatMorphism

class CategoryMorphism(object):
    def __init__(self,cat_action_1,cat_action_2,object_mapping,morphism_mapping):
        if not isinstance(cat_action_1,CategoryAction):
           raise Exception("Source is not a valid CategoryAction class\n")
        if not isinstance(cat_action_2,CategoryAction):
            raise Exception("Target is not a valid CategoryAction class\n")
        self.cat_action_1 = cat_action_1
        self.cat_action_2 = cat_action_2
        self.object_mapping = object_mapping
        self.morphism_mapping = morphism_mapping

    def get_image_object(self,object_name):
        return self.object_mapping[object_name]

    def get_image_morphism(self,morphism_name):
        return self.morphism_mapping[morphism_name]

    def is_valid(self):

        ## We first need that the source and targets of each morphisms
        ## are correctly mapped, i.e. to check that for f:X->Y in the source
        ## category, the image N(f) is a morphism from N(X) to N(Y)

        for name_f,f in self.cat_action_1.get_morphisms():
            source_name = f.source.name
            target_name = f.target.name

            image_name_f = self.get_image_morphism(name_f)

            source_image_name = self.cat_action_2.morphisms[image_name_f].source.name
            target_image_name = self.cat_action_2.morphisms[image_name_f].target.name
            if not ((self.get_image_object(source_name)==source_image_name) and \
                    (self.get_image_object(target_name)==target_image_name)):
                return False

        ## Then we need to check if N is an actual functor, i.e. for all
        ## f:X->Y and g:Y->Z in the source category, we have N(gf)=N(g)N(f)

        for name_f,f in self.cat_action_1.get_morphisms():
            for name_g,g in self.cat_action_1.get_morphisms():
                try:
                    prod = self.cat_action_1.mult(name_g,name_f)
                except:
                    ## g and f are not composable, so no need to check any
                    ## further
                    continue

                image_name_f = self.get_image_morphism(name_f)
                image_name_g = self.get_image_morphism(name_g)
                try:
                    image_prod = self.cat_action_2.mult(image_name_g,image_name_f)
                except:
                    ## N(g) and N(f) are not composable, so this is not a functor
                    return False
                ## Finally we check if we indeed have N(gf)=N(g)N(f)
                if not self.get_image_morphism(prod)==image_prod:
                    return False
        return True

class CategoryActionMorphism(object):
    def __init__(self,cat_action_1,cat_action_2,category_morphism,nat_transform):
        ## Nat transform is a dictionary of CatMorphism, with keys the object
        ## names of cat_action_1

        if not isinstance(cat_action_1,CategoryAction):
           raise Exception("Source is not a valid CategoryAction class\n")
        if not isinstance(cat_action_2,CategoryAction):
            raise Exception("Target is not a valid CategoryAction class\n")
        if not isinstance(category_morphism,CategoryMorphism):
            raise Exception("The category morphism is not a valid CategoryMorphism class\n")
        self.cat_action_1 = cat_action_1
        self.cat_action_2 = cat_action_2
        self.category_morphism = category_morphism
        self.nat_transform = nat_transform

    def is_valid(self):
        ## see def of Rel_PKNets
        ## names of cat_action_1
        for name_f,f in self.cat_action_1.get_morphisms():
            source_name = f.source.name
            target_name = f.target.name
            nat_transform_source = self.nat_transform[source_name]
            nat_transform_target = self.nat_transform[target_name]
            image_name_f = self.category_morphism.get_image_morphism(name_f)
            image_morphism = self.cat_action_2.morphisms[image_name_f]
            if not (nat_transform_target*f)<=(image_morphism*nat_transform_source):
                return False
        return True

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
                        self.monoidaction_source.get_object()[1],
                        self.monoidaction_dest.get_object()[1])
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
        for name_x,x in sorted(self.monoidaction_source.morphisms.items()):
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
