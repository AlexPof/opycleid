# -*- coding: utf-8 -*-

################################################
###### Copyright (c) 2016, Alexandre Popoff
###

import numpy as np
import itertools
import networkx as nx
from .categoryaction import *

class SetRigElement(object):
    def __init__(self,monoid):
        """Initializes a SetRigElement object.
           This is an element in the abelian monoid B[X], which can be associated
           to a subset of X, where X is the image set of a given monoid action.

        Parameters
        ----------
        monoid: an instance of MonoidAction representing the monoid and its action
                on a set X.

        Returns
        -------
        None
        Raise an exception if monoid is not an instance of MonoidAction.
        """
        if not isinstance(monoid,MonoidAction):
            raise Exception("A set rig element should be initialized with an instance of monoid")
        self.monoid = monoid
        self.element = set([])

    def set_value(self,elem_list):
        """Set the value of the element of B[X].

        Parameters
        ----------
        elem_list: a list of elements in the set X (the set upon which the monoid acts).

        Returns
        -------
        Itself. Raises an exception if an element does not belong to the set X.
        """
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
        """Adds two instances of SetRigElement according to the rules of the boolean rig B.

        Parameters
        ----------
        rhs: an instance of SetRigElement built on the same monoid action.

        Returns
        -------
        A new instance of SetRigElement whose value is set to be the boolean rig addition of
        the LHS and the RHS.
        """
        if not isinstance(rhs,SetRigElement):
            raise Exception("RHS should be a set rig element")
        new_vector = SetRigElement(self.monoid)
        new_vector.element = self.element.union(rhs.element)
        return new_vector

    def __eq__(self,rhs):
        """Compares two SetRigElement.

        Parameters
        ----------
        rhs: an instance of SetRigElement built on the same monoid action.

        Returns
        -------
        True if both LHS and RHS values are the same, False otherwise.
        """
        if not isinstance(rhs,SetRigElement):
            raise Exception("RHS should be a set rig element")
        return self.element==rhs.element

    def __repr__(self):
        """Returns a verbose description of the SetRigElement
        Overloads the 'str' operator of Python

        Parameters
        ----------
        None

        Returns
        -------
        A string representation of the sum of set elements with coefficients in the
        boolean rig B. If the sum is empty, displays ∅.
        """
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
        """Initializes a MonoidRigElement object.
           This is an element in the boolean rig B[M] where M is the monoid 
           in the given monoid action.

        Parameters
        ----------
        monoid: an instance of MonoidAction representing the monoid and its action
                on a set X.

        Returns
        -------
        None
        Raise an exception if monoid is not an instance of MonoidAction.
        """
        if not isinstance(monoid,MonoidAction):
            raise Exception("A monoid rig element should be initialized with an instance of MonoidAction")
        self.monoid = monoid
        self.element = set([])

    def set_value(self,group_elem_list):
        """Set the value of the element of B[M].

        Parameters
        ----------
        group_elem_list: a list of operations in the monoid.

        Returns
        -------
        Itself. Raises an exception if an operation does not belong to the given monoid.
        """
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
        """Adds two instances of MonoidRigElement, according to the addition in B[M].

        Parameters
        ----------
        rhs: an instance of MonoidRigElement built on the same monoid action.

        Returns
        -------
        An instance of MonoidRigElement representing the addition in B[M] of the LHS and RHS.
        """
        if not isinstance(rhs,MonoidRigElement):
            raise Exception("RHS should be a monoid rig element")
        new_grouprig_element = MonoidRigElement(self.monoid)
        new_grouprig_element.element = self.element.union(rhs.element)
        return new_grouprig_element

    def __mul__(self,rhs):
        """Overload the multiplication operator of Python to represent either
            -  the multiplication of two instances of MonoidRigElement,
               according to the multiplication in the rig B[M].
            -  or the action of an instance MonoidRigElement on an instance of
               SetRigElement, according to the action B[M] x B[X] -> B[X].

        Parameters
        ----------
        rhs: an instance of MonoidRigElement built on the same monoid action, or
             an instance of SetRigElement built on the same monoid action.

        Returns
        -------
        Depending on rhs, an instance of MonoidRigElement representing the
        multiplication in B[M] of the LHS and RHS, or an instance of SetRigElement representing
        the action of B[M] on B[X].
        """
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
        """Compares two MonoidRigElement.

        Parameters
        ----------
        rhs: an instance of MonoidRigElement built on the same monoid action.

        Returns
        -------
        True if both LHS and RHS values are the same, False otherwise.
        """
        if not isinstance(rhs,MonoidRigElement):
            raise Exception("RHS should be a monoid rig element")
        return self.element==rhs.element

    def __repr__(self):
        """Returns a verbose description of the MonoidRigElement
        Overloads the 'str' operator of Python

        Parameters
        ----------
        None

        Returns
        -------
        A string representation of the sum of monoid operations with
        coefficients in the boolean rig B. If the sum is empty, displays ∅.
        """
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

class MonoidRigMatrix(object):
    def __init__(self,shape, monoid):
        """Initializes a MonoidRigMatrix object.
           This is an matrix with values in B[M] where M is the monoid 
           in the given monoid action.

        Parameters
        ----------
        shape: a tuple (m,n) with m>=1 and n>=1 representing the shape of the matrix.
        monoid: an instance of MonoidAction.

        Returns
        -------
        None. The matrix is empty upon initialization.
        Raise an exception if monoid is not an instance of MonoidAction, or if the shape is 
        not at least 1x1.
        """
        if shape[0]<1 or shape[1]<1:
            raise Exception("Matrix should have dimension at least 1")
        if not isinstance(monoid,MonoidAction):
            raise Exception("A monoid rig element should be initialized with an instance of MonoidAction")
        self.shape = shape
        self.monoid = monoid
        self.matrix = np.empty(self.shape,dtype=MonoidRigElement)
        self.set_zero()
                
    def set_unit(self):
        """Sets the diagonal elements of the matrix to be the unit element of
        the monoid.

        Parameters
        ----------
        None

        Returns
        -------
        Itself.
        """
        object_name = self.monoid.get_objects()[0][0]
        for i in range(self.shape[0]):
            self.set_value((i,i),["id_"+object_name])
        return self
        
    def set_zero(self):
        """Sets all the elements of the matrix to be the null
        element of B[M].

        Parameters
        ----------
        None

        Returns
        -------
        Itself.
        """
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.matrix[i,j] = MonoidRigElement(self.monoid)
        return self

    def set_values(self,indices,value_list):
        """Sets values of the matrix at the given indices.

        Parameters
        ----------
        indices: either a tuple (i,j) or a list of tuples (i,j) indicating
                 the indices at which the matrix values should be set.
        value_list: either a list of monoid operations, or a list of lists of
                 operations, indicating the values the matrix should take.

        Returns
        -------
        Itself.
        """
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
        """Adds two instances of MonoidRigMatrix of the same shape.

        Parameters
        ----------
        rhs: an instance of MonoidRigMatrix.

        Returns
        -------
        A new instance of MonoidRigMatrix representing the addition of two
        elements of Mat_{m,n}(B[M]). Raises an exception if the RHS is not 
        a MonoidRigMatrix, or if the shapes differ.
        """
        if not isinstance(rhs,MonoidRigMatrix):
            raise Exception("RHS should be a monoid rig matrix")
        if not self.shape==rhs.shape:
            raise Exception("Matrices should have identical shape")
        new_monoidrigmatrix = MonoidRigMatrix(self.shape,self.monoid)
        new_monoidrigmatrix.matrix = self.matrix+rhs.matrix
        return new_monoidrigmatrix

    def __mul__(self,rhs):
        """Multiplies two instances of MonoidRigMatrix of the same shape.

        Parameters
        ----------
        rhs: an instance of MonoidRigMatrix.

        Returns
        -------
        A new instance of MonoidRigMatrix representing the element_wise
        multiplication of two elements of Mat_{m,n}(B[M]). Raises an
        exception if the RHS is not a MonoidRigMatrix, or if the shapes differ.
        """
        if not isinstance(rhs,MonoidRigMatrix):
            raise Exception("RHS should be a monoid rig matrix")
        if not self.shape==rhs.shape:
            raise Exception("Matrices should have identical shape")
           
        new_monoidrigmatrix = MonoidRigMatrix(self.shape,self.monoid)
        new_monoidrigmatrix.matrix = self.matrix*rhs.matrix
        return new_monoidrigmatrix
       
    def __matmul__(self,rhs):
        """Matrix multiplication of two instances of MonoidRigMatrix, or
        application of a MonoidRigMatrix to a SetRigVector.

        Parameters
        ----------
        rhs: an instance of MonoidRigMatrix or SetRigVector.

        Returns
        -------
        If rhs is an instance of MonoidRigMatrix:
            A new instance of MonoidRigMatrix representing the matrix
            multiplication of two elements of Mat_{m,n}(B[M]). Raises an
            exception if the RHS is not a MonoidRigMatrix, or if the shapes
            do not match.
        If rhs is an instance of SetRigVector:
            A new instance of SetRigVector representing the action of
            a MonoidRigMatrix on the given vector.
        """
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
        """Matrix power of an instance of MonoidRigMatrix.

        Parameters
        ----------
        n: a positive integer.

        Returns
        -------
        A new instance of MonoidRigMatrix representing this matrix
        to the power n. Raises an exception if n is not a positive integer.
        """
        assert isinstance(n,int) and n>=0,"Power should be a positive int"
        
        new_monoidrigmatrix = MonoidRigMatrix(self.shape,self.monoid).set_unit()
        for i in range(n):
            new_monoidrigmatrix = new_monoidrigmatrix@self
        return new_monoidrigmatrix
        
    def __eq__(self,rhs):
        """Compares two MonoidRigMatrix.

        Parameters
        ----------
        rhs: an instance of MonoidRigMatrix built on the same monoid action.

        Returns
        -------
        True if both LHS and RHS values are the same, False otherwise.
        """
        return np.array_equal(self.matrix,rhs.matrix)

    def __repr__(self):
        return str(self.matrix)
        
    def __str__(self):
        return str(self.matrix)

class SetRigVector(object):
    def __init__(self,n: int, monoid):
        """Initializes a SetRigVector object.
           This is a nx1 matrix with values in B[X].

        Parameters
        ----------
        n: a strictly positive integer representing the dimension of the vector.
        monoid: an instance of MonoidAction.

        Returns
        -------
        None. The vector is initialized with null elements of B[X].
        Raise an exception if monoid is not an instance of MonoidAction, or if the dimension
        is not at least 1.
        """
        if n<1:
            raise Exception("Matrix should have dimension at least 1")
        if not isinstance(monoid,MonoidAction):
            raise Exception("A set rig element should be initialized with an instance of MonoidAction")
        self.n = n
        self.vector = np.empty((n,1),dtype=SetRigElement)
        self.monoid = monoid
        for i in range(n):
            self.vector[i,0] = SetRigElement(self.monoid)

    def set_values(self,indices,value_list):
        """Sets values of the vector at the given indices.

        Parameters
        ----------
        indices: a list of indices at which the vector values should be set.
        value_list: a list of lists of elements defining instances of SetRigElement.

        Returns
        -------
        Itself.
        """
        assert isinstance(indices,list), "Indices should be a list"
        for i,x in zip(indices,value_list):
            self.vector[i,0]=SetRigElement(self.monoid).set_value(x)
        return self

    def __add__(self,rhs):
        """Adds two instances of SetRigVector of the same dimension.

        Parameters
        ----------
        rhs: an instance of SetRigVector.

        Returns
        -------
        A new instance of SetRigVector representing the addition of two
        elements of Mat_{n,1}(B[M]). Raises an exception if the RHS is not 
        a SetRigVector, or if the dimensions differ.
        """
        if not isinstance(rhs,SetRigVector):
            raise Exception("RHS should be a set rig vector")
        if not self.n==rhs.n:
            raise Exception("Vector dimension mismatch")
        new_setrigvector = SetRigVector(self.n,self.monoid)
        new_setrigvector.vector = self.vector+rhs.vector
        return new_setrigvector

    def __eq__(self,rhs):
        """Compares two SetRigVector.

        Parameters
        ----------
        rhs: an instance of SetRigVector built on the same monoid action.

        Returns
        -------
        True if both LHS and RHS values are the same, False otherwise.
        """
        return np.array_equal(self.vector,rhs.vector)

    def __repr__(self):
        return str(self.vector)
        
    def __str__(self):
        return str(self.vector)   

####################################################


class MatrixNetwork(object):
    def __init__(self,matrix=None,vector=None):
        """Initializes a MatrixNetwork object.

        Parameters
        ----------
        matrix: an idempotent instance of MonoidRigMatrix.
        vector: an invariant instance of SetRigVector upon the action of 'matrix'

        Returns
        -------
        None. The network is empty by default.
        If 'matrix' and 'vector' are provided, calls set_network to initialize the MatrixNetwork.
        """
        self.monoidelements = None
        self.matrix = None
        self.vector = None
        if (matrix is not None) and (vector is not None):
            self.set_network(matrix,vector)
        
    def set_network(self,matrix,vector):
        """Defines the components of the matrix network.

        Parameters
        ----------
        matrix: an idempotent instance of MonoidRigMatrix.
        vector: an invariant instance of SetRigVector upon the action of 'matrix'

        Returns
        -------
        The current instance of MatrixNetwork.
        """
        assert isinstance(matrix,MonoidRigMatrix),"matrix should be an instance of MonoidRigMatrix"
        assert isinstance(vector,SetRigVector),"vector should be an instance of SetRigVector"
        assert matrix==matrix@matrix, "Network matrix should be idempotent"
        assert vector==matrix@vector, "Vector should be invariant by matrix application"
        
        self.matrix = matrix
        self.vector = vector
        
        return self

    def from_multidigraphs(self,multidigraph_dict,monoid,return_monoid=False):
        """Build the network from networkx MultiDigraphs
        
        Parameters
        ----------
        multidigraph_dict: a dictionary of MultiDiGraphs. The nodes must have an attribute
                      named "element" with a list of valid values in the monoid.
                      The edges must have an attribute named "operations" with a list of
                      valid values in the monoid.

        monoid:       an instance of MonoidAction.
                      
        Returns
        -------
        An instance of the matrix network, with self.matrix and self.vector set to be
            the matrix and vector derived from the MultiDiGraph.
        """

        assert isinstance(monoid,MonoidAction),"This is not a valid instance of networkx MultiDiGraph"

        generators={}
        vectors={}
        
        for digraph_name,multidigraph in multidigraph_dict.items():
        
            assert isinstance(multidigraph,nx.MultiDiGraph),"This is not a valid instance of networkx MultiDiGraph"
            for node in multidigraph.nodes:
                assert multidigraph.nodes[node].get("element") is not None,"The node {} is missing the 'element' attribute".format(node)
            for edge in multidigraph.edges:
                assert multidigraph.edges[edge].get("operations") is not None,"The edge {} is missing the 'operations' attribute".format(edge)
    
            N_nodes,N_edges = len(multidigraph.nodes()),len(multidigraph.edges())
            dict_idx2nodes = dict(enumerate(multidigraph.nodes()))
            
            M = MonoidRigMatrix(shape=(N_nodes,N_nodes),monoid=monoid)
            X = SetRigVector(n=N_nodes,monoid=monoid)
            
            for idx_node,node in enumerate(multidigraph.nodes):
                X.set_value([idx_node],[multidigraph.nodes[node]["element"]])
            
            for i in range(N_nodes):
                for j in range(N_nodes):
                    operations=[]
                    for idx_edge,edge in enumerate(multidigraph.edges):
                        src,trgt,_ = edge
                        if src==dict_idx2nodes[i] and trgt==dict_idx2nodes[j]:
                            operations.append(*multidigraph.edges[edge]["operations"])
                    M = M.set_value([(j,i)],[operations])

            generators[digraph_name] = M
            vectors[digraph_name] = X

        return self.from_generators(generators,np.sum([x for x in vectors.values()]),return_monoid=return_monoid)
        
    
    def from_generators(self,generators,vector,return_monoid=False):
        """Build the network from generators

        Parameters
        ----------
        generators: a dictionary, whose keys are strings indicating matrix names
                    and whose values are matrices with values in a group rig.

        vector: a matrix of shape (N,1), whose whose values are elements in a set rig.

        return_monoid: a boolean. If True, returns all elements in the monoid as
                       a dictionary.

        Returns
        -------
        An instance of the matrix network, with self.matrix and self.vector set to be
            the idempotent matrix and the fixed point vectors derived from the generators
            and the given vector.

            If return_monoid is True, it also returns a dictionary, whose keys are the names
            of the elements in the monoid, and whose values are the matrices in the monoid.
        """
        unit_matrix = MonoidRigMatrix(list(generators.values())[0].shape,list(generators.values())[0].monoid).set_unit()
        self.monoidelements = {"e":unit_matrix}
        added_elements = generators.copy()
        
        while len(added_elements)>0:
            for k,v in added_elements.items():
                self.monoidelements[k] = v
            added_elements = {}
            for name_m,m in generators.items():
                for name_el,el in self.monoidelements.items():
                    new_matrix = m@el
                    if not np.any([x==new_matrix for x in self.monoidelements.values()]):
                        if not np.any([x==new_matrix for x in added_elements.values()]):
                            added_elements[name_m+name_el] = new_matrix
        self.matrix = np.sum(list(self.monoidelements.values()))
        self.vector = self.matrix@vector
        
        if return_monoid:
            return self,self.monoidelements
        else:
            return self

    def get_multidigraph(self):
        """Returns a multidigraph from the matrix network

        Parameters
        ----------
        None

        Returns
        -------
        An instance of networkx MultiDigraph, the nodes of which having an 'element'
        attribute indicating the musical objects on this node, the edges of which
        having an 'operations' attribute indicating the operations between them.
        """

        N_nodes,_ = self.matrix.matrix.shape
        DG = nx.MultiDiGraph()
        for i in range(N_nodes):
            DG.add_node(i,element=list(self.vector.vector[i,0].element))
        for i in range(N_nodes):
            for j in range(N_nodes):
                if len(self.matrix.matrix[j,i].element):
                    for op in self.matrix.matrix[j,i].element:
                        DG.add_edge(i,j,operations=[op])
                    
        return DG

        
        
    def apply_categoryactionfunctor(self,catactionfunctor):
        """Applies a category action functor to the matrix network and 
            returns the corresponding matrix network image.

        Parameters
        ----------
        catactionfunctor: an instance of CategoryActionFunctor to apply to
                          the current network.

        Returns
        -------
        An instance of MatrixNetwork.
        """
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
                
        return new_matrix,new_vector
        
    
    def is_conjugated(self,matnet,P):
        """Determines if two matrix networks are conjugated by the matrix P, i.e.
           if the matrices M and N of each network obey PM=NP, and the vectors X and Y
           of each network obey Y=PX.

        Parameters
        ----------
        matnet: an instance of MatrixNetwork.
        P: an instance of MonoidRigMatrix

        Returns
        -------
        True if the two matrix networks are conjugated, False otherwise.
        """
        assert isinstance(matnet,MatrixNetwork),"matnet should be an instance of MatrixNetwork"
        assert isinstance(P,MonoidRigMatrix),"Conjugating matrix should be an instance of MonoidRigMatrix"
        
        check_matrices = np.array_equal(P@self.matrix,matnet.matrix@P)
        check_vectors = np.array_equal(P@self.vector,matnet.vector)
        
        return (check_matrices and check_vectors)