# -*- coding: utf-8 -*-

################################################
###### Copyright (c) 2016, Alexandre Popoff
###

import numpy as np
from .categoryaction import CatObject,CatMorphism,CategoryAction,CategoryFunctor,CategoryActionFunctor

class PKNet(object):
    """The class PKNet defines a relational PK-Net (Poly-Klumpenhouwer network)
    as defined in the paper:
    - Alexandre Popoff, Moreno Andreatta & Andrée Ehresmann (2018),
      Relational poly-Klumpenhouwer networks for transformational and
      voice-leading analysis, Journal of Mathematics and Music,
      12:1, 35-55, DOI: 10.1080/17459737.2017.1406011.

    It is basically a category action functor between a category action called
    the 'diagram action', and a category action called the 'context action'.
    The diagram action defines sets of elements and relations between them; the
    category action functor maps the elements and the relations to musical
    elements and transformations in the context action.

    PKNets can be transformed by applying a category action functor, in order
    to change the musical context action.
    """

    def __init__(self,context_action):
        """Instantiates a PKNet.

        Parameters
        ----------
        context_action : an instance of CategoryAction, representing the musical
                         context of analysis for the PK-Net. Elements and
                         relations have their 'image' in this category action.

        Returns
        -------
        None
        """
        self.diagram_action = None
        self.context_action = context_action
        self.cat_action_functor = None


    def set_edges(self,list_edges):
        """Defines the generating edges of the PK-Net

        Parameters
        ----------
        list_edges : a list of CatMorphism, each one representing a generating
                     morphism for the 'diagram' category action. Objects need
                     not be specified, as they will be automatically extracted
                     from the list of morphisms.

        Returns
        -------
        None
        """
        unique_objects = []
        for edge in list_edges:
            if not edge.source in unique_objects:
                unique_objects.append(edge.source)
            if not edge.target in unique_objects:
                unique_objects.append(edge.target)
        self.diagram_action = CategoryAction()
        self.diagram_action.set_objects(unique_objects)
        self.diagram_action.set_generators(list_edges)
        self.diagram_action.generate_category()

    def set_mappings(self,edges_map,elements_map):
        """Defines the category action functor through the mapping of the edges
           and of the elements of the diagram action.

        Parameters
        ----------
        edges_map : a dictionary, the keys of which are the names of the
                    edges (i.e. the generating morphisms of the diagram action),
                    the values of which are the names of morphisms in the
                    context action.

        elements_map : a dictionary, the keys of which are the names of the
                       elements in the objects of the diagram action, the values
                       of which are lists of elements names in the objects of
                       the context action. The method will automatically
                       build the components of the natural transformation of
                       the category action functor.
        Returns
        -------
        None. Raises exceptions if the edge or elements mapping are not valid.
        """
        F = CategoryFunctor(self.diagram_action,self.context_action)
        if not F.set_from_generator_mapping(edges_map):
            raise Exception("Edge mapping is not valid")
        object_mapping = F.get_object_mapping()

        ## We now build the natural transformation, component by component, i.e.
        ## object by object in the diagram action.
        phi = {}
        for name_obj,obj in self.diagram_action.get_objects():
            target_obj = self.context_action.objects[object_mapping[name_obj]]

            component_map = {}
            for elem in obj.get_elements():
                component_map[elem] = elements_map[elem]
            phi_component = CatMorphism("phi_{}".format(name_obj),obj,target_obj)
            phi_component.set_mapping(component_map)
            if not phi_component._is_lefttotal():
                raise Exception("Element mappings must be left total")
            phi[name_obj] = phi_component

        self.cat_action_functor = CategoryActionFunctor(self.diagram_action,
                                                        self.context_action,
                                                        F,phi)
        if not self.cat_action_functor.is_valid():
            raise Exception("Element mapping is not valid")

    def get_edge_mapping(self):
        """Gets the mapping of *all* edges in the diagram action.

        Parameters
        ----------
        None

        Returns
        -------
        A dictionary, the keys of which are morphism names in the diagram action,
        the values of which are the names of the image morphisms in the context
        action by the category functor of the category action functor which
        defines this PK-Net.
        """
        return self.cat_action_functor.cat_functor.get_morphism_mapping()

    def get_elements_mapping(self):
        """Gets the mapping of all elements in the diagram action.

        Parameters
        ----------
        None

        Returns
        -------
        A dictionary, the keys of which are element names in the objects of the
        diagram action, the values of which are the names of the image elements
        in the context action by the natural transformation of the category
        action functor which defines this PK-Net.
        """
        return {k:v for obj,morph in self.cat_action_functor.nat_transform.items()
                      for k,v in morph.get_mapping().items()}

    def from_progression(self,elements):
        """From a list of n element names in the context action, yields all
        PK-Nets with a diagram action built on the ordinal n category.
        In other words, it yields all PK-Nets with n objects and n-1 edges,
        each edge f_i corresponding to a transformation in the context action
        between elements[i] and elements[i+1].

        Parameters
        ----------
        elements: a list of element names in the objects of the context action.

        Yields
        -------
        The next PK-Net with n objects and n-1 edges, each edge f_i
        corresponding to a transformation in the context action between
        elements[i] and elements[i+1].
        Raises an exception if no transformation exists between consecutive
        elements.
        """
        singletons = [CatObject("X_{}".format(i),["x_{}".format(i)]) for i in range(len(elements))]
        edges = []
        for i in range(len(elements)-1):
            f = CatMorphism("f_{}".format(i),singletons[i],singletons[i+1])
            f.set_mapping({"x_{}".format(i):["x_{}".format(i+1)]})
            edges.append(f)

        elements_mapping = {"x_{}".format(i):[v] for i,v in enumerate(elements)}
        for list_operations in self._possible_operations(elements):
            transf_mapping = {"f_{}".format(i):v for i,v in enumerate(list_operations)}
            pknet = PKNet(self.context_action)
            pknet.set_edges(edges)
            pknet.set_mappings(transf_mapping,elements_mapping)

            yield pknet

    def _possible_operations(self,elements,list_op=[]):
        """From a list of n element names, yields all transformations between
        consecutive elements.

        Parameters
        ----------
        elements: a list of element names in the objects of the context action.

        Yields
        -------
        The next list of morphism names, such that the i-th morphism is a
        transformation in the context action between elements[i] and
        elements[i+1]. Raises an exception if no transformation exists between
        consecutive elements.
        """
        next_ops = self.context_action.get_operation(elements[0],elements[1])
        if not len(next_ops):
            raise Exception("No transformation can be found between elements {} and {}".format(elements[0],elements[1]))
        if len(elements)>2:
            for op in next_ops:
                for thelist in self._possible_operations(elements[1:],list_op+[op]):
                    yield thelist
        else:
            for op in next_ops:
                yield list_op+[op]

    def global_transform(self,cat_action_functor):
        """Apply a category action functor and returns the corresponding new
        PK-Net.

        Parameters
        ----------
        cat_action_functor: an instance of Category Action Functor.

        Returns
        -------
        A new PK-Net
            - with the same diagram action,
            - whose context action corresponds to the target category
              action of cat_action_functor,
            - and whose category action functor is the product of the initial
              category action functor by cat_action_functor
        """
        new_PKNet = PKNet(self.cat_action_functor.cat_action_target)
        new_PKNet.diagram_action = self.diagram_action
        new_PKNet.cat_action_functor = cat_action_functor*self.cat_action_functor

        return new_PKNet

    def local_transform(self,cat_functor,local_dict):
        """Apply a local transformation and returns the corresponding new
        PK-Net.

        Parameters
        ----------
        cat_functor: an instance of Category Functor, which should be an
                     automorphism.

        local_dict:  a dictionary defining a natural transformation, the keys of
                     which are objects names in the diagram category action, the
                     values of which are morphism names in the context category
                     action.

        Returns
        -------
        A new PK-Net
            - with the same diagram action and context action,
            - and whose category action functor is the product of the initial
              category action functor by the image by S of the natural
              transformation defined by local_dict.

        Raises an exception if local_dict does not define a valid natural
        transformation, or if cat_functor is not an automorphism.
        """

        new_PKNet = PKNet(self.context_action)
        new_PKNet.diagram_action = self.diagram_action

        new_cat_functor = cat_functor*self.cat_action_functor.cat_functor
        if not cat_functor.is_automorphism():
            raise Exception("Not an automorphism")

        edge_mapping = self.get_edge_mapping()
        cat_functor_morphism_mapping = new_cat_functor.get_morphism_mapping()
        ## Testing for the natural transformation condition
        for name_f,f in self.diagram_action.get_morphisms():
            source_obj_name = f.source.name
            target_obj_name = f.target.name

            image_name_f = edge_mapping[name_f]
            if not self.context_action.mult(local_dict[target_obj_name],image_name_f) == \
                   self.context_action.mult(cat_functor_morphism_mapping[name_f],local_dict[source_obj_name]):
                raise Exception("Natural transformation condition not verified")

        new_nat_transform = {}
        for obj,component in self.cat_action_functor.nat_transform.items():
            new_nat_transform[obj] = self.context_action.morphisms[local_dict[obj]]*component

        new_cat_action_functor = CategoryActionFunctor(self.diagram_action,
                                                       self.context_action,
                                                       new_cat_functor,
                                                       new_nat_transform
                                                       )
        if not new_cat_action_functor.is_valid():
            raise Exception("Local transform is not valid")

        new_PKNet.cat_action_functor = new_cat_action_functor

        return new_PKNet


    def __str__(self):
        """Returns a verbose description of the PK-Net.
        Overloads the 'str' operator of Python

        Parameters
        ----------
        None

        Returns
        -------
        A description of the PK-Net listing for each edge its name, its source
        and target, and the corresponding maps between elements, expressed as
        their image in the context action.
        """
        str_rep=""
        edge_mapping = self.get_edge_mapping()
        elements_mapping = self.get_elements_mapping()
        for name_f,f in self.diagram_action.get_generators():
            edge_name = edge_mapping[name_f]
            source_elements = [elements_mapping[x] for x in f.source.get_elements()]
            target_elements = [elements_mapping[x] for x in f.target.get_elements()]
            str_rep += "{} -- {} --> {}\n".format(f.source.name,edge_name,f.target.name)
            str_rep+="{} -> {}\n".format(source_elements,target_elements)
        return str_rep
