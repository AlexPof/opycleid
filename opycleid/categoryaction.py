# -*- coding: utf-8 -*-

################################################
###### Copyright (c) 2016, Alexandre Popoff
###

import numpy as np
import itertools

class CatObject:
    def __init__(self,name,elements):
        self.name = name
        self.dict_elem2idx = dict([(x,i) for i,x in enumerate(elements)])
        self.dict_idx2elem = dict([(i,x) for i,x in enumerate(elements)])

    def get_idx_by_name(self,elem):
        if not elem in self.dict_elem2idx:
            raise Exception("The specified element cannot be found")
        return self.dict_elem2idx.get(elem)

    def get_name_by_idx(self,idx):
        return self.dict_idx2elem.get(idx)

    def get_elements(self):
        return list(self.dict_elem2idx.keys())

    def get_cardinality(self):
        return len(self.dict_idx2elem)

    def is_in(self,elem):
        return elem in self.dict_elem2idx

class CatMorphism:
    def __init__(self,name,source,target):
        self.name = name
        self.source = source
        self.target = target

    def set_name(self,name):
        self.name = name

    def set_to_identity(self):
        if not (self.source==self.target):
            raise Exception("Source and target should be identical")
        card_source = self.source.get_cardinality()
        self.matrix = np.eye(card_source,dtype=bool)

    def set_mapping(self,mapping):
        card_source = self.source.get_cardinality()
        card_target = self.target.get_cardinality()
        self.matrix = np.zeros((card_target,card_source),dtype=bool)
        for elem,images in mapping.items():
            id_elem = self.source.get_idx_by_name(elem)
            for image in images:
                id_image = self.target.get_idx_by_name(image)
                self.matrix[id_image,id_elem] = True

    def set_mapping_matrix(self,matrix):
        self.matrix = matrix

    def get_mapping(self):
        dest_cardinality,source_cardinality = self.matrix.shape
        return dict([(self.source.get_name_by_idx(i),
                [self.target.get_name_by_idx(x) for x in np.where(self.matrix[:,i])[0]]) \
                for i in range(source_cardinality)])

    def get_mapping_matrix(self):
        return self.matrix

    def __str__(self):
        """Returns a verbose description of the morphism
        Overloads the 'str' operator of Python

        Parameters
        ----------
        None

        Returns
        -------
        A description of the morphism via its source, target, and mapping.
        """
        descr = self.name+":"+self.source.name+"->"+self.target.name+"\n\n"
        for s,t in self.get_mapping().items():
            descr += " "*(len(self.name)+1)
            descr += s+"->"+(",".join(t))+"\n"
        return descr

    def __rshift__(self,elem):
        """Apply the current morphism to an element of its domain
        Overloads the '>>' operator of Python

        Parameters
        ----------
        elem : string representing an element of self.source

        Returns
        -------
        The image of elem by the current morphism
        """
        idx_elem = self.source.get_idx_by_name(elem)
        return [self.target.get_name_by_idx(x) for x in np.where(self.matrix[:,idx_elem])[0]]

    def __mul__(self,morphism):
        """Compose two morphisms
        Overloads the '*' operator of Python

        Parameters
        ----------
        morphism : an instance of CatMorphism

        Returns
        -------
        The product self * morphism. Raises an exception if the two morphisms
        are not composable
        """
        if not morphism.target==self.source:
            raise Exception("Morphisms are not composable")
        new_morphism =  CatMorphism(self.name+morphism.name,morphism.source,self.target)
        new_morphism.set_mapping_matrix((self.matrix.dot(morphism.matrix))>0)

        return new_morphism

    def __eq__(self,morphism):
        """Checks if the given morphism is equal to 'morphism'
        Overloads the '=' operator of Python

        Parameters
        ----------
        morphism : an instance of CatMorphism

        Returns
        -------
        True if 'self' is equal to 'morphism'
        """
        return (self.source == morphism.source) and \
               (self.target == morphism.target) and \
               (np.array_equal(self.matrix,morphism.matrix))

    def __lt__(self, morphism):
        """Checks if the given morphism is included in 'morphism', i.e. if there
        is a 2-morphism in Rel from 'self' to 'morphism'.
        Overloads the '<' operator of Python

        Parameters
        ----------
        morphism : an instance of CatMorphism

        Returns
        -------
        True if 'self' is included in 'morphism'
        """

        if not (self.source == morphism.source) and (self.target == morphism.target):
            raise Exception("Morphisms should have the same domain and codomain")
        return np.array_equal(self.matrix,self.matrix & morphism.matrix)

class CategoryAction:
    def __init__(self):
        self.objects={}
        self.generators={}
        self.operations={}

    def set_objects(self,list_objects):
        self.objects={}
        self.generators={}
        self.operations={}
        for catobject in list_objects:
            self.objects[catobject.name] = catobject

    def add_generators(self,list_morphisms):
        for catmorphism in list_morphisms:
            self.generators[catmorphism.name] = catmorphism

    def add_morphisms(self,list_morphisms):
        for catmorphism in list_morphisms:
            self.operations[catmorphism.name] = catmorphism

    def add_identities(self):
        for name,catobject in self.objects.items():
            identity_morphism = CatMorphism("id_"+name,catobject,catobject)
            identity_morphism.set_to_identity()
            self.add_morphisms([identity_morphism])

    def generate_category(self):
        self.operations = self.generators.copy()
        self.add_identities()
        new_liste = self.generators.copy()
        added_liste = self.generators.copy()
        while(len(added_liste)>0):
            added_liste = {}
            for name_x,morphism_x in new_liste.items():
                for name_g,morphism_g in self.generators.items():
                    try:
                        c=0
                        new_morphism = morphism_g*morphism_x
                        for name_y,morphism_y in self.operations.items():
                            if new_morphism==morphism_y:
                                c=1
                        if c==0:
                            added_liste[new_morphism.name] = new_morphism
                            self.operations[new_morphism.name] = new_morphism
                    except:
                        pass
            new_liste = added_liste

    def mult(self,name_g,name_f):
        new_morphism = self.operations[name_g]*self.operations[name_f]
        return [x for x in self.operations if self.operations[x]==new_morphism][0]

    def apply_operation(self,name_f,elem):
        return self.operations[name_f]>>elem

    def get_operation(self,elem1,elem2):
        res = []
        for name_f,f in self.operations.items():
            try:
                if elem2 in f>>elem1:
                    res.append(name_f)
            except:
                pass
        return res

    def get_description(self,name_f):
        return str(self.operations[name_f])


class MonoidAction(CategoryAction):
    """Defines a monoid action,
    i.e. a functor from a monoid-as-category to Sets or Rel.

    Variables
    ----------
    objects : dictionary of musical elements. Keys are string describing
              the elements (for example "C"), values are indices.
    generators : dictionary of monoid operations, which are
                generators of the monoid.
                Keys are string describing the operations (for example "I^3"),
                values are boolean matrices representing the action
                of the operation.

    operations : dictionary of monoid operations. Keys are string describing the
                operations (for example "I^3"), values are boolean matrices
                representing the action of the operation.

    SIMPLY_TRANSITIVE: boolean, indicating whether the action is
                        simply transitive or not.
    """
    def __init__(self):
        self.objects = {}
        self.generators = {}
        self.operations = {}
        self.SIMPLY_TRANSITIVE=False

    def set_objects(self,list_objects):
        """Add musical objects to the monoid action.

        Parameters
        ----------
        object_list : a list of XXXX should

        Returns
        -------
        None
        """
        self.objects={}
        self.generators={}
        self.operations={}
        if len(list_objects)>1:
            raise Exception("A monoid must have a single object")
        for catobject in list_objects:
            self.objects[catobject.name] = catobject

    def get_object(self):
        """XXX should
        """
        return self.objects.values()[0]

    def get_automorphisms(self):
        """Returns all automorphisms of the monoid as a list of dictionaries.

        Parameters
        ----------
        None

        Returns
        -------
        A list of dictionaries. Each dictionary maps the generators (the keys)
        to their image in the monoid (the values)
        """
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
        """Checks if a given map of operations is an automorphism.

        Parameters
        ----------
        autom_dict : dictionary, whose keys are generators of the monoid,
                    and values are the image of the generators in the monoid
                    by the map.
        full_map :  if True, returns the full mapping of all the operations in
                    the monoid as a dictionary.

        Returns
        -------
        A tuple (valid,fullmap) where:
            - valid is a boolean indicating if the map defined by autom_dict
               is an automorphism
            - fullmap is None if full_map=False, a dictionary mapping all
               operations of the monoid (keys) to their image (values)
               if full_map=True.
        """
        new_liste = self.generators
        added_liste = self.generators
        full_mapping = autom_dict.copy()
        full_mapping["id_."]="id_."


        ## This is a variant of the monoid generation method.
        ## It generates the monoid and their images by the map of generators.
        ## If it does not give a multi-valued function, and if it generates the same number of elements
        ## then it is a bijection, hence a valid automorphism

        while(len(added_liste)>0):
            added_liste = []
            for name_x in new_liste:
                for name_g in self.generators:
                    name_product = self.mult(name_g,name_x)
                    name_imageproduct = self.mult(full_mapping[name_g],full_mapping[name_x])
                    if not name_product in full_mapping:
                        added_liste.append(name_product)
                        full_mapping[name_product] = name_imageproduct
                    else:
                        ## If the generated element already exists, we check that its existing image corresponds
                        ## to the image which has just been calculated
                        if not full_mapping[name_product] == name_imageproduct:
                            ## We have a multi-valued function so the algorithm stops there
                            return (False,None)
            new_liste = added_liste[:]

        if not len(np.unique(full_mapping.values()))==len(self.operations):
            return (False,None)
        else:
            if full_map:
                return (True,full_mapping)
            else:
                return (True,None)

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
        I1 = np.unique([self.mult(op_name,x) for x in self.operations])
        for op in self.operations:
            I2 = np.unique([self.mult(op,x) for x in self.operations])
            if sorted(I2) == sorted(I1):
                list_Req.append(op)
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
        I1 = np.unique([self.mult(x,op_name) for x in self.operations])
        for op in self.operations:
            I2 = np.unique([self.mult(x,op) for x in self.operations])
            if sorted(I2) == sorted(I1):
                list_Req.append(op)
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
        """Computes all L classes for the monoid.

        Parameters
        ----------
        None

        Returns
        -------
        A list of lists, each list being an L class.
        """
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
            for f in self.operations:
                t = self.mult(f,m)
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
            for f in self.operations:
                t = self.mult(m,f)
                if not t in S:
                    return False
        return True
