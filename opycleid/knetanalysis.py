# -*- coding: utf-8 -*-

################################################
###### Copyright (c) 2016, Alexandre Popoff
###

import numpy as np
from .categoryaction import MonoidAction

class KNet:
    """Class definition for a K-Net
    """


    def __init__(self,category):
        """Initialize a K_Net.
        Variables
        ----------
        - vertices : dictionary, keys are index numbers, values are elements in the K_Net category/monoid
        - edges : dictionary, keys are index numbers, values are 3-tuples (start,end,op) (see add_edges)
        - category : an instance of a MonoidAction class
        """

        if not isinstance(category,MonoidAction):
            raise Exception("Not a valid monoid action\n")
        else:
            self.vertices = {}
            self.edges = {}
            self.category = category


    def set_vertices(self,list_vertices):
        """Set vertices for the K_Net.
        Checks if:
            - the provided musical element is in the K_Net category action

        Parameters
        ----------
        list_vertices : list of musical elements

        Returns
        -------
        None
        """
        self.edges = {}
        for x in list_vertices:
            if self.category.get_object().is_in(x):
                self.vertices[len(self.vertices)] = x
            else:
                raise Exception("Element "+str(x)+" is not in the category action\n")

    def add_edges(self,list_edges):
        """Add labelled edges to a K_Net.
        Checks if:
            - There does not already an edge between the indicated vertices
            - The provided operation exists in the K_Net category
            - The provided operation is a valid one given the corresponding vertices
        Parameters
        ----------
        list_edges : list of 3-tuples (start,end,op), where
                - start is the index of the starting vertex
                - end is the index of the ending vertex
                - op is an operation in the K_Net category/monoid

        Returns
        -------
        None
        """
        for id_vertex_A,id_vertex_B,operation in list_edges:

            for edge_start,edge_end,edge_op in self.edges.itervalues():
                if edge_start == id_vertex_A and id_vertex_B == edge_end:
                    raise Exception("There already exists an edge between vertices "+str(edge_start)+" and "+str(edge_end)+"\n")

            if not operation in self.category.operations.keys():
                raise Exception(str(operation)+" is not a valid operation in the category\n")

            if operation in self.category.get_operation(self.vertices[id_vertex_A],self.vertices[id_vertex_B]):
                self.edges[len(self.edges)] = (id_vertex_A,id_vertex_B,operation)
            else:
                raise Exception(str(operation)+" is not a valid operation for the corresponding vertices\n")

    def path_knet_from_vertices(self):
        """Creates automatically all edges between successive vertices of the K_Net.
        Checks if:
            - the K_Net category/monoid action is simply transitive. Fails otherwise, since the determination of operations is ambiguous

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if not self.category.SIMPLY_TRANSITIVE:
            raise Exception("The category does not act in a simple transitive way: ambiguous determination of operations")
        else:
            for i in range(len(self.vertices)-1):
                self.add_edges([(i,i+1,self.category.get_operation(self.vertices[i],self.vertices[i+1])[0])])

    def complete_knet_from_vertices(self):
        """Creates automatically all edges between vertex i and all vertices j>i of the K_Net.
        Checks if:
            - the K_Net category/monoid action is simply transitive. Fails otherwise, since the determination of operations is ambiguous

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if not self.category.SIMPLY_TRANSITIVE:
            raise Exception("The category does not act in a simple transitive way: ambiguous determination of operations")
        else:
            for i in range(len(self.vertices)):
                for j in range(i+1,len(self.vertices)):
                    self.add_edges([(i,j,self.category.get_operation(self.vertices[i],self.vertices[j])[0])])


    def is_valid(self):
        """Checks the consistency of the K_Net.
        A K_Net is considered as consistent if:
            - it does not contain cycles
            - path consistency is respected:
                given two edges A->B, and B->C, with operations f, and g, respectively,
                the edge A->C (if it exists) has operation gf.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        ## Get the adjacency matrix
        n_obj = len(self.vertices)
        adj_matrix = np.zeros((n_obj,n_obj),dtype=bool)
        for x in self.edges:
            adj_matrix[self.edges[x][1],self.edges[x][0]] = True

        ## Check for the presence of cycles
        for i in range(2,n_obj+1):
            C = np.linalg.matrix_power(adj_matrix,i)
            if np.sum(C[range(n_obj),range(n_obj)]):
                return False

        ## Build the labelled adjacency matrix
        lbl_adj_matrix = np.zeros((n_obj,n_obj),dtype=object)
        for x in self.edges:
            lbl_adj_matrix[self.edges[x][1],self.edges[x][0]] = self.edges[x][2]

            ## Matrix multiplication with values in a monoid
            for i in range(n_obj):
                for j in range(n_obj):
                    l=[]
                    for k in range(n_obj):
                        if not (lbl_adj_matrix[i,k] == 0 or lbl_adj_matrix[k,j] == 0):
                            l.append(self.category.mult(lbl_adj_matrix[i,k],lbl_adj_matrix[k,j]))
                    if len(l):
                        if len(l)>1:
                            return False
                        if not lbl_adj_matrix[i,j] == 0 and not l[0] == lbl_adj_matrix[i,j]:
                            return False

        return True


    def apply_knet_morphism(self,monoidactionmorphism):
        """Apply a K-Net morphism to a given K_Net.
        A K-Net morphism consists in
            - a monoid morphism, defining how operations are transformed
            - a natural transformation, defining how the musical elements are transformed

        Parameters
        ----------
        monoidactionmorphism : a instance of MonoidActionMorphism

        Returns
        -------
        A new K-Net, whose vertices and edges are the images of the vertices and edges of the initial K-Net by the given K_net morphism
        """

        if monoidactionmorphism.is_valid():
            new_knet = KNet(monoidactionmorphism.monoidaction_dest)
            new_knet.vertices=self.vertices.copy()
            new_knet.edges=self.edges.copy()

            for i in range(len(new_knet.vertices)):
                vertex_image = monoidactionmorphism.nat_trans>>new_knet.vertices[i]
                if len(vertex_image)>1:
                    raise Exception("Rel-based MonoidAction morphisms are not implemented")
                new_knet.vertices[i] = vertex_image[0]
            for i in range(len(new_knet.edges)):
                id_vertex_A,id_vertex_B,operation = new_knet.edges[i]
                new_knet.edges[i] = (id_vertex_A,id_vertex_B,monoidactionmorphism.monoid_morphism[operation])

            return new_knet
        else:
            raise Exception("The given monoid morphism and/or the natural transformation do not constitute a valid K-Net morphism")


    ################################################
    ## KNet display


    def __str__(self):
        descr = "K-Net description: \n"
        for x in self.edges:
            name_A = self.vertices[self.edges[x][0]]
            name_B = self.vertices[self.edges[x][1]]
            name_op = self.edges[x][2]
            descr += "    "+" "*len(name_A)+name_op+" "*len(name_B)+"\n"
            descr += "    "+self.vertices[self.edges[x][0]]
            descr += "-"*len(name_op)+">"+self.vertices[self.edges[x][1]]+"\n"
        return descr
