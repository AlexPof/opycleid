# -*- coding: utf-8 -*-

################################################
###### Copyright (c) 2016, Alexandre Popoff
###

import numpy as np
from .categoryaction import CatObject,CatMorphism,CategoryAction,CategoryFunctor,CategoryActionFunctor

class PKNet(object):
    def __init__(self,cat_action):
        self.diagram_action = None
        self.cat_action = cat_action ## CHANGE NAME
        self.cat_action_functor = None

    def set_edges(self,list_edges):
        unique_objects = []
        for edge in list_edges:
            if not edge.source in unique_objects:
                unique_objects.append(edge.source)
            if not edge.target in unique_objects:
                unique_objects.append(edge.target)
        self.diagram_action = CategoryAction()
        self.diagram_action.set_objects(unique_objects)
        self.diagram_action.add_generators(list_edges)
        self.diagram_action.generate_category()

    def set_mappings(self,transf_dict,elements_dict):
        F = CategoryFunctor(self.diagram_action,self.cat_action)
        F.set_from_generator_mapping(transf_dict)

        phi = {}
        object_mapping = F.get_object_mapping()
        for name_obj,obj in self.diagram_action.get_objects():
            target_obj = self.cat_action.objects[object_mapping[name_obj]]

            element_mapping = {}
            for elem in obj.get_elements():
                element_mapping[elem] = elements_dict[elem]
            phi_component = CatMorphism("phi_{}".format(name_obj),obj,target_obj)
            phi_component.set_mapping(element_mapping)
            phi[name_obj] = phi_component

        self.cat_action_functor = CategoryActionFunctor(self.diagram_action,self.cat_action,F,phi)

    def get_edge_mapping(self):
        return self.cat_action_functor.category_functor.get_morphism_mapping()

    def get_elements_mapping(self):
        return {k:v for obj,morph in self.cat_action_functor.nat_transform.items()
                      for k,v in morph.get_mapping().items()}

    def transform(self,cat_action_functor):
        ## CHANGE NAME of CAT_ACTION_1 !!
        new_PKNet = PKNet(self.cat_action_functor.cat_action_1)
        new_PKNet.diagram_action = self.diagram_action
        new_PKNet.cat_action_functor = cat_action_functor*self.cat_action_functor

        return new_PKNet
