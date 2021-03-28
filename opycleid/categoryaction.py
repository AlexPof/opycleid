# -*- coding: utf-8 -*-

################################################
###### Copyright (c) 2016, Alexandre Popoff
###

import numpy as np
import itertools
import time

class CatObject(object):
    def __init__(self,name,elements):
        """Initializes a category object (set)

        Parameters
        ----------
        name: a string representing the name of the object
        elements: a list of strings representing the elements of the set

        Returns
        -------
        None
        Raise an exception if the set is empty or if the set elements are not
        distinct from each other.
        """
        self.name = name
        if not len(elements):
            raise Exception("Empty sets are not admissible")
        if not len(np.unique(elements))==len(elements):
            raise Exception("Set elements are not unique")
        self.dict_elem2idx = dict([(x,i) for i,x in enumerate(elements)])
        self.dict_idx2elem = dict([(i,x) for i,x in enumerate(elements)])

    def get_idx_by_name(self,elem):
        """Returns the index of the given element

        Parameters
        ----------
        elem: the name of the element

        Returns
        -------
        The index of the element in the set.
        Raises an exception if the element does not belong to the set.
        """
        if not elem in self.dict_elem2idx:
            raise Exception("The specified element cannot be found")
        return self.dict_elem2idx.get(elem)

    def get_name_by_idx(self,idx):
        """Returns the name of the given element

        Parameters
        ----------
        idx: the index of the element in the set

        Returns
        -------
        The name of the element
        """
        return self.dict_idx2elem.get(idx)

    def get_elements(self):
        """Returns the list of the elements in this object

        Parameters
        ----------
        None

        Returns
        -------
        The list of element names in this object
        """
        return sorted(self.dict_elem2idx.keys())

    def get_cardinality(self):
        """Returns the cardinality of this object (set)

        Parameters
        ----------
        None

        Returns
        -------
        An int corresponding to the number of elements in this object
        """
        return len(self.dict_idx2elem)

    def is_in(self,elem):
        """Checks if a given element is in this object

        Parameters
        ----------
        elem: the name of the element to be checked

        Returns
        -------
        True if the element is inside the set, False otherwise
        """
        return elem in self.dict_elem2idx

class CatMorphism(object):
    def __init__(self,name,source,target,mapping=None):
        """Initializes a category morphism between two objects

        Parameters
        ----------
        name: a string representing the name of the morphism
        source: an instance of CatObject representing the domain of the morphism
        target: an instance of CatObject representing the codomain of
                the morphism
        mapping: optional argument representing the mapping of elements
                 between the domain and the codomain. The mapping can be
                 given as a NumPy array matrix or as a dictionary.

        Returns
        -------
        None
        """
        if not isinstance(source,CatObject):
           raise Exception("Source is not a valid CatObject class\n")
        if not isinstance(target,CatObject):
            raise Exception("Target is not a valid CatObject class\n")
        self.name = name
        self.source = source
        self.target = target
        if mapping is not None:
            if isinstance(mapping,np.ndarray)==False:
                self.set_mapping(mapping)
            else:
                self.set_mapping_matrix(mapping)

    def set_name(self,name):
        """Sets the name of the morphism

        Parameters
        ----------
        name: a string representing the new name of the morphism

        Returns
        -------
        None
        """
        if not len(name):
            raise Exception("The specified morphism name is empty")
        self.name = name

    def set_to_identity(self):
        """Sets the morphism to be an identity morphism. The domain and codomain
        must be identical.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if not (self.source==self.target):
            raise Exception("Source and target should be identical")
        card_source = self.source.get_cardinality()
        self.matrix = np.eye(card_source,dtype=bool)

    def set_mapping(self,mapping):
        """Sets the mapping of elements between the domain and the codomain

        Parameters
        ----------
        mapping: a dictionary, with:
                - keys: the element names in the domain of the morphism
                - values: a list of element names in the codomain of the morphism

        The mapping can be one-on-many as we are working in the category Rel of
        finite sets and relations

        Returns
        -------
        None
        """
        card_source = self.source.get_cardinality()
        card_target = self.target.get_cardinality()
        self.matrix = np.zeros((card_target,card_source),dtype=bool)
        for elem,images in sorted(mapping.items()):
            id_elem = self.source.get_idx_by_name(elem)
            for image in images:
                id_image = self.target.get_idx_by_name(image)
                self.matrix[id_image,id_elem] = True

    def set_mapping_matrix(self,matrix):
        """Sets the mapping of elements between the domain and the codomain

        Parameters
        ----------
        matrix: a boolean matrix (m,n), where m is the cardinality of the codomain
        and n the cardinality of the domain, indicating the image of the elements.

        Returns
        -------
        None
        """
        self.matrix = matrix

    def get_mapping(self):
        """Retrieves the mapping in the form of a dictionary

        Parameters
        ----------
        None

        Returns
        -------
        A dictionary, with:
                - keys: the element names in the domain of the morphism
                - values: a list of element names in the codomain of the morphism
        """
        dest_cardinality,source_cardinality = self.matrix.shape
        return dict([(self.source.get_name_by_idx(i),
                [self.target.get_name_by_idx(x) for x in np.where(self.matrix[:,i])[0]]) \
                for i in range(source_cardinality)])

    def get_mapping_matrix(self):
        """Retrieves the mapping in matrix form

        Parameters
        ----------
        None

        Returns
        -------
        A boolean matrix representing the morphism in Rel
        """
        return self.matrix

    def copy(self):
        """Copy the current morphism

        Parameters
        ----------
        None

        Returns
        -------
        A new instance of CatMorphism with the same domain, codomain, and mapping
        """
        U = CatMorphism(self.name,self.source,self.target)
        U.set_mapping_matrix(self.get_mapping_matrix())

        return U

    def _is_lefttotal(self):
        """Checks if the morphism is left total

        Parameters
        ----------
        None

        Returns
        -------
        True if the morphism is left total, False otherwise.
        """

        return np.all(np.sum(self.matrix,axis=0))


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
        for s,t in sorted(self.get_mapping().items()):
            descr += " "*(len(self.name)+1)
            descr += s+"->"+(",".join(t))+"\n"
        return descr

    def __call__(self,elem):
        """Apply the current morphism to an element of its domain

        Parameters
        ----------
        elem : string representing an element of self.source

        Returns
        -------
        The image of elem by the current morphism
        """
        idx_elem = self.source.get_idx_by_name(elem)
        return [self.target.get_name_by_idx(x) for x in np.where(self.matrix[:,idx_elem])[0]]

    def __pow__(self,int_power):
        """Raise the morphism to the power int_power
        Overloads the '**' operator of Python

        Parameters
        ----------
        int_power : an integer

        Returns
        -------
        The power self^int_power. Raises an exception if the morphism is not an endomorphism
        """
        if not self.target==self.source:
            raise Exception("Morphism should be an endomorphism")
        U = self.copy()
        U.set_to_identity()
        for i in range(int_power):
            U = self*U
        U.set_name(self.name+"^"+str(int_power))

        return U

    def __mul__(self,morphism):
        """Compose two morphisms
        Overloads the '*' operator of Python

        Parameters
        ----------
        morphism : an instance of CatMorphism

        Returns
        -------
        The product self * morphism.
        Returns None if the two morphisms are not composable
        """

        if not isinstance(morphism,CatMorphism):
           raise Exception("RHS is not a valid CatMorphism class\n")

        if not morphism.target==self.source:
            return None
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
        if not isinstance(morphism,CatMorphism):
           raise Exception("RHS is not a valid CatMorphism class\n")
        if self is None or morphism is None:
           return False
        return (self.source == morphism.source) and \
               (self.target == morphism.target) and \
               (np.array_equal(self.matrix,morphism.matrix))

    def __le__(self, morphism):
        """Checks if the given morphism is included in 'morphism', i.e. if there
        is a 2-morphism in Rel from 'self' to 'morphism'.
        Overloads the '<=' operator of Python

        Parameters
        ----------
        morphism : an instance of CatMorphism

        Returns
        -------
        True if 'self' is included in 'morphism'
        """
        if not isinstance(morphism,CatMorphism):
           raise Exception("RHS is not a valid CatMorphism class\n")
        if self is None or morphism is None:
            return False
        if not (self.source == morphism.source) and (self.target == morphism.target):
            raise Exception("Morphisms should have the same domain and codomain")
        return np.array_equal(self.matrix,self.matrix & morphism.matrix)

    def __lt__(self, morphism):
        """Checks if the given morphism is strictly included in 'morphism', i.e. if there
        is a non-identity 2-morphism in Rel from 'self' to 'morphism'.
        Overloads the '<' operator of Python

        Parameters
        ----------
        morphism : an instance of CatMorphism

        Returns
        -------
        True if 'self' is strictly included in 'morphism'
        """

        if not isinstance(morphism,CatMorphism):
           raise Exception("RHS is not a valid CatMorphism class\n")
        if self is None or morphism is None:
           return False
        return (self<=morphism) and (not self==morphism)


class CategoryAction(object):
    def __init__(self,objects=None,generators=None,generate=True):
        """Instantiates a CategoryAction class

        Parameters
        ----------
        objects: optional list of CatObject instances representing
                 the objects in the category.

        generators: optional list of CatMorphism instances
                 representing the generators of the category.

        generator: optional boolean indicating whether the category
                   should be generated upon instantiation.

        Returns
        -------
        None
        """
        self.objects={}
        self.generators={}
        self.morphisms={}
        self.equivalences=[]
        if objects is not None:
            self.set_objects(objects)
        if generators is not None:
            self.set_generators(generators)
            if generate==True:
                self.generate_category()

    def set_objects(self,list_objects):
        """Sets the objects constituting the category action. This erases
        all previous objects, morphisms, and generators.

        Parameters
        ----------
        list_objects: a list of CatObject classes representing the objects in
        the category.

        Returns
        -------
        None. Checks if all objects have distinct names, raises an Exception
        otherwise.
        """
        self.objects={}
        self.generators={}
        self.morphisms={}
        self.equivalences=[]

        ob_names = [catobject.name for catobject in list_objects]
        if not len(ob_names)==len(np.unique(ob_names)):
            raise Exception("Objects should have distinct names")

        for catobject in list_objects:
            self.objects[catobject.name] = catobject

    def get_objects(self):
        """Returns the objects in the category action.

        Parameters
        ----------
        None

        Returns
        -------
        A list of pairs (x,y), where:
            - x is the name of the object
            - y is the corresponding instance of CatObject
        """
        return list(sorted(self.objects.items()))

    def get_morphisms(self):
        """Returns the morphisms in the category action.

        Parameters
        ----------
        None

        Returns
        -------
        A list of pairs (x,y), where:
            - x is the name of the morphism
            - y is the corresponding instance of CatMorphism
        """
        return list(sorted(self.morphisms.items()))

    def get_generators(self):
        """Returns the generators in the category action.

        Parameters
        ----------
        None

        Returns
        -------
        A list of pairs (x,y), where:
            - x is the name of the generator
            - y is the corresponding instance of CatMorphism
        """
        return list(sorted(self.generators.items()))

    def set_generators(self,list_morphisms):
        """Set generators to the category action. This erases
        all previous morphisms and generators.

        Parameters
        ----------
        list_morphisms: a list of CatMorphism instances representing the
                        generator morphisms to be added.

        Returns
        -------
        None.
        Checks if sources and targets of generators are objects present
        in the category, raises an Exception otherwise
        Checks if all generators have distinct names, raises an Exception
        otherwise.
        """
        self.generators={}
        self.morphisms={}
        self.equivalences=[]

        all_gennames = [m.name for m in list_morphisms]
        if not len(all_gennames)==len(np.unique(all_gennames)):
            raise Exception("Generators must have distinct names")

        cat_obj_names = [x[0] for x in self.get_objects()]

        for m in list_morphisms:
            if not isinstance(m,CatMorphism):
                raise Exception("Generator is not a valid CatMorphism class\n")
            if not m.source.name in cat_obj_names:
                raise Exception("Domain or codomain of a generator is not present in the category")
            if not m.target.name in cat_obj_names:
                raise Exception("Domain or codomain of a generator is not present in the category")
            self.generators[m.name] = m

    def _add_morphisms(self,list_morphisms):
        """Add morphisms to the category action.

        Parameters
        ----------
        list_morphisms: a list of CatMorphism instances representing the
                        morphisms to be added.

        Returns
        -------
        None
        Checks if sources and targets of generators are objects present
        in the category, raises an Exception otherwise.
        Checks if the morphisms have a distinct name, raises an Exception
        otherwise.
        """

        cat_obj_names = [x[0] for x in self.get_objects()]
        cat_mor_names = [x[0] for x in self.get_morphisms()]

        for m in list_morphisms:
            if not m.source.name in cat_obj_names:
                raise Exception("Domain or codomain of a generator is not present in the category")
            if not m.target.name in cat_obj_names:
                raise Exception("Domain or codomain of a generator is not present in the category")
            if m.name in cat_mor_names:
                raise Exception("Morphisms should have distinct names")
            self.morphisms[m.name] = m

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
        for name,catobject in sorted(self.objects.items()):
            identity_morphism = CatMorphism("id_"+name,catobject,catobject)
            identity_morphism.set_to_identity()
            self._add_morphisms([identity_morphism])

    def generate_category(self):
        """Generates all morphisms in the category based on the given list of
        generators. The generation proceeds by successive multiplication of
        generators and morphisms until completion. This is suited to small
        category action, but the performance would be prohibitive for very
        large categories containing many morphisms.

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
                                self.equivalences.append([new_morphism.name,morphism_y.name])
                        if c==0:
                            added_liste[new_morphism.name] = new_morphism
                            self.morphisms[new_morphism.name] = new_morphism
            new_liste = added_liste

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

    def apply_operation(self,name_f,element):
        """Applies a morphism to a given element.

        Parameters
        ----------
        name_f: a string representing the name of the morphisms to be applied.
        elem: a string representing the name of the element.

        Returns
        -------
        A list of strings representing the images of elem by name_f
        """
        return self.morphisms[name_f](element)

    def get_operation(self,element_1,element_2):
        """Returns the operations taking the element element_1 to the element
        element_2.

        Parameters
        ----------
        element_1,element_2 : strings representing the name of the elements.

        Returns
        -------
        A list of strings representing the morphisms f such that element_2 is
        an image of element_1 by f.
        """
        res = []
        for name_f,f in self.get_morphisms():
            try:
                if element_2 in f(element_1):
                    res.append(name_f)
            except:
                pass
        return res

    def rename_operation(self,name_f,new_name):
        """Renames a morphism in the category

        Parameters
        ----------
        name_f: a string representing the name of the morphism to be renamed.
        new_name: a string representing the new name of the morphism.

        Returns
        -------
        None
        """
        if not name_f in self.morphisms:
            raise Exception("The specified operation cannot be found")
        new_op = self.morphisms[name_f].copy()
        new_op.set_name(new_name)
        del self.morphisms[name_f]
        self.morphisms[new_name] = new_op

    def rewrite_operations(self):
        """Rewrites morphism names in the category action by trying to reduce
        repeated substrings.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        operation_names = sorted(self.morphisms.keys())
        for op_name in operation_names:
            self.rename_operation(op_name,self._rewrite(op_name))

        equivalences_new=[]
        for x,y in self.equivalences:
            equivalences_new.append([self._rewrite(x),self._rewrite(y)])
        self.equivalences = equivalences_new

    def _rewrite(self,the_string):
        """Rewrites a string by trying to reduce repeated patterns of the
        category action generator names.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if "id" in the_string:
            return the_string

        generator_names = sorted(self.generators.keys())

        count_list=[["",0]]
        while(len(the_string)):
            flag=0
            for name_g in generator_names:
                if the_string[:len(name_g)]==name_g:
                    flag=1
                    if count_list[-1][0]==name_g:
                        count_list[-1][1]+=1
                    else:
                        count_list.append([name_g,1])
                    the_string=the_string[len(name_g):]
            if not flag:
                raise Exception("Operation name cannot be rewritten")
        new_string=""
        for name,count in count_list:
            if count>1:
                new_string+="("+name+"^"+str(count)+")"
            else:
                new_string+=name
        return new_string


    def get_description(self,name_f):
        """Gets a string description of a given morphism.

        Parameters
        ----------
        name_f: a string representing the name of the morphism

        Returns
        -------
        A string representing the corresponding morphism
        """
        return str(self.morphisms[name_f])

    def get_automorphisms(self):
        """Returns all automorphisms of the category action.

        Parameters
        ----------
        None

        Returns
        -------
        A list of CategoryFunctor instances corresponding to an automorphism.
        """
        l1 = sorted(self.generators.keys())
        l2 = sorted(self.morphisms.keys())
        list_automorphisms = []

        ## Get all maps from the generator set to itself
        for mapping in itertools.permutations(l2,len(l1)):
            ## Builds a dictionary representing the generator mapping
            gen_mapping=dict(zip(l1,mapping))

            N = CategoryFunctor(self,self)
            if N.set_from_generator_mapping(gen_mapping):
                ## Tests if the given map of generators is indeed an automorphism...
                if N.is_automorphism():
                    list_automorphisms.append(N)
        return list_automorphisms

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
        super(MonoidAction,self).__init__()

    def set_objects(self,list_objects):
        """Add musical objects to the monoid action.

        Parameters
        ----------
        object_list : a list with a single object.

        Returns
        -------
        None
        """
        self.objects={}
        self.generators={}
        self.morphisms={}
        if len(list_objects)>1:
            raise Exception("A monoid must have a single object")
        for catobject in list_objects:
            self.objects[catobject.name] = catobject

    def get_object(self):
        """Returns the unique object of the monoid.

        Parameters
        ----------
        None

        Returns
        -------
        The unique object of the monoid.
        """
        return self.get_objects()[0]

    def is_simplytransitive(self):
        """Checks if the monoid action is simply transitive.


        Parameters
        ----------
        None

        Returns
        -------
        Returns True if the monoid action is simply transitive.
        """
        N = self.get_object()[1].get_cardinality()
        M = np.zeros((N,N))
        for name_f,f in self.get_morphisms():
            M += (f.get_mapping_matrix()).astype(int)
        return np.array_equal(M,np.ones((N,N)))

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


class CategoryFunctor(object):
    def __init__(self,cat_action_source,cat_action_target):
        """Instantiates a CategoryFunctor class, i.e. a functor from one category
        to another. Although we are dealing with category action, a CategoryFunctor
        object only focuses on morphisms and their images.

        Parameters
        ----------
        cat_action_1, cat_action_2: instances of CategoryAction, the domain
        and codomain of the functor

        Returns
        -------
        None
        """
        if not isinstance(cat_action_source,CategoryAction):
           raise Exception("Source is not a valid CategoryAction class\n")
        if not isinstance(cat_action_target,CategoryAction):
            raise Exception("Target is not a valid CategoryAction class\n")
        self.cat_action_source = cat_action_source
        self.cat_action_target = cat_action_target
        self.object_mapping = None
        self.morphisms_mapping = None
        self.generators_mapping = None


    def set_fullmapping(self,object_mapping,morphism_mapping):
        """Sets the mapping of morphisms and objects between the domain and
        codomain category actions. The method checks if the given mappings are
        valid and returns the corresponding True/False values.

        Parameters
        ----------
        object_mapping: a dictionary, the keys of which are object names in the
                        source category action, the values of which are object
                        names in the target category action.

        morphism_mapping: a dictionary, the keys of which are morphism names in
                         the source category action, the values of which are
                         morphism names in the target category action.

        Returns
        -------
        True if the given mappings are valid, False otherwise.
        """
        self.object_mapping = object_mapping
        self.morphisms_mapping = morphism_mapping
        self.generators_mapping = {}
        for name_f,f in self.cat_action_source.get_generators():
            self.generators_mapping[name_f] = morphism_mapping[name_f]
        return self.is_valid()

    def set_from_generator_mapping(self,gen_mapping):
        """Sets the mapping of morphisms and objects between the domain and
        codomain category actions from a mapping of the generators. The method
        checks if the given mappings are valid and returns the corresponding
        True/False values.

        Parameters
        ----------
        gen_mapping: a dictionary, the keys of which are generator names in the
                        source category action, the values of which are morphism
                        names in the target category action.

        Returns
        -------
        True if the given mappings is valid, False otherwise.
        """

        if not gen_mapping.keys()==self.cat_action_source.generators.keys():
            return False

        ## First we need to check if the mapping defines a valid mapping
        ## between objects
        num_objects = len(self.cat_action_source.get_objects())

        object_mapping=[]
        for f,image_f in gen_mapping.items():
            s1 = self.cat_action_source.morphisms[f].source.name
            s2 = self.cat_action_target.morphisms[image_f].source.name
            t1 = self.cat_action_source.morphisms[f].target.name
            t2 = self.cat_action_target.morphisms[image_f].target.name
            object_mapping.append((s1,s2))
            object_mapping.append((t1,t2))
        object_mapping = set(object_mapping)
        if not len(object_mapping)==num_objects:
            return False

        full_mapping = gen_mapping.copy()
        for obj,image_obj in object_mapping:
            full_mapping["id_"+obj] = "id_"+image_obj

        new_liste = self.cat_action_source.generators.copy()
        added_liste = self.cat_action_source.generators.copy()

        ## This is a variant of the category action generation method.
        ## It generates the category and their images by the map of generators.
        ## If it does not give a multi-valued function, we get the corresponding
        ## functor.

        while(len(added_liste)>0):
            added_liste = []
            for name_x in new_liste:
                for name_g,g in self.cat_action_source.get_generators():
                    name_product = self.cat_action_source.mult(name_g,name_x)
                    name_imageproduct = self.cat_action_target.mult(full_mapping[name_g],full_mapping[name_x])
                    if name_product is not None and name_imageproduct is not None:
                        if not name_product in full_mapping:
                            added_liste.append(name_product)
                            full_mapping[name_product] = name_imageproduct
                        elif not full_mapping[name_product] == name_imageproduct:
                            ## If the generated element already exists, we check that its existing image corresponds
                            ## to the image which has just been calculated
                            return False
            new_liste = added_liste[:]

        self.generators_mapping = gen_mapping.copy()
        self.object_mapping = dict(object_mapping)
        self.morphisms_mapping = full_mapping.copy()

        ## By construction, this is functorial, so there is no need to check
        ## with the is_valid() method
        return True

    def __call__(self,rhs):
        """Gets the image of an object or a morphism by the category functor.

        Parameters
        ----------
        rhs: a string representing the name of an object or the name
        of a morphism in the domain category of this functor.

        Returns
        -------
        A string representing the image of the object by this functor.
        """

        source_obj_names = [x[0] for x in self.cat_action_source.get_objects()]
        source_mor_names = [x[0] for x in self.cat_action_source.get_morphisms()]

        if rhs in source_obj_names:
            return self.get_image_object(rhs)
        elif rhs in source_mor_names:
            return self.get_image_morphism(rhs)
        else:
            raise Exception("Not an object or a morphism")

    def get_image_object(self,object_name):
        """Gets the image of an object by the category functor.

        Parameters
        ----------
        object_name: a string representing the name of an object in the domain
        category of this functor.

        Returns
        -------
        A string representing the image of the object by this functor.
        """
        return self.object_mapping[object_name]

    def get_image_morphism(self,morphism_name):
        """Gets the image of a morphism by the category functor.

        Parameters
        ----------
        morphism_name: a string representing the name of a morphism in the domain
        category of this functor.

        Returns
        -------
        A string representing the image of the morphism by this functor.
        """
        return self.morphisms_mapping[morphism_name]

    def get_object_mapping(self):
        """Gets the mapping of objects by the category functor.

        Parameters
        ----------
        None

        Returns
        -------
        A dictionary representing the mapping of the objects.
        """
        return sorted(self.object_mapping)

    def get_morphism_mapping(self):
        """Gets the mapping of a morphisms by the category functor.

        Parameters
        ----------
        None

        Returns
        -------
        A dictionary representing the mapping of the morphisms.
        """
        return sorted(self.morphisms_mapping)

    def is_valid(self):
        """Checks if the specified functor is a valid one.

        Parameters
        ----------
        None

        Returns
        -------
        True if the given mapping is valid, False otherwise.
        """
        ## We first need that the source and targets of each morphisms
        ## are correctly mapped, i.e. to check that for f:X->Y in the source
        ## category, the image N(f) is a morphism from N(X) to N(Y)

        for name_f,f in self.cat_action_source.get_morphisms():
            source_name = f.source.name
            target_name = f.target.name

            image_name_f = self(name_f)

            source_image_name = self.cat_action_target.morphisms[image_name_f].source.name
            target_image_name = self.cat_action_target.morphisms[image_name_f].target.name
            if not ((self(source_name)==source_image_name) and \
                    (self(target_name)==target_image_name)):
                return False

        ## Then we need to check if N is an actual functor, i.e. for all
        ## f:X->Y and g:Y->Z in the source category, we have N(gf)=N(g)N(f)

        for name_f,f in self.cat_action_source.get_morphisms():
            for name_g,g in self.cat_action_source.get_morphisms():
                prod = self.cat_action_source.mult(name_g,name_f)
                if prod is not None:
                    image_name_f = self(name_f)
                    image_name_g = self(name_g)
                    image_prod = self.cat_action_target.mult(image_name_g,image_name_f)
                    if image_prod is None:
                        ## N(g) and N(f) are not composable, so this is not a functor
                        return False
                    ## Finally we check if we indeed have N(gf)=N(g)N(f)
                    if not self(prod)==image_prod:
                        return False
        return True

    def is_automorphism(self):
        """Checks if the specified functor is an automorphism.

        Parameters
        ----------
        None

        Returns
        -------
        True if the given mapping is an automorphism, False otherwise.
        """

        if not self.cat_action_source == self.cat_action_target:
            return False

        ## We first need to check that the object mapping is bijective

        num_objects = len(self.cat_action_source.get_objects())
        if not (len(set(self.object_mapping.keys()))==num_objects and \
               len(set(self.object_mapping.values()))==num_objects):
            return False

        ## Then we need to check if the morphism mapping is bijective

        num_morphisms = len(self.cat_action_source.get_morphisms())

        if not (len(set(self.morphisms_mapping.keys()))==num_morphisms and \
               len(set(self.morphisms_mapping.values()))==num_morphisms):
            return False

        return True

    def __mul__(self,cat_functor):
        """Compose two category functors
        Overloads the '*' operator of Python

        Parameters
        ----------
        cat_functor : an instance of CategoryFunctor

        Returns
        -------
        The product self * cat_functor. Returns None if the two morphisms
        are not composable
        """
        if not cat_functor.cat_action_target==self.cat_action_source:
            return None


        new_cat_functor =  CategoryFunctor(cat_functor.cat_action_source,
                                           self.cat_action_target)
        gen_mapping = {}
        for name_g,g in cat_functor.cat_action_source.get_generators():
            image_name_g = cat_functor(name_g)
            gen_mapping[name_g] = self(image_name_g)
        new_cat_functor.set_from_generator_mapping(gen_mapping)

        return new_cat_functor

    def __eq__(self,cat_functor):
        """Test if two functors are equal.

        Parameters
        ----------
        cat_functor : an instance of CategoryFunctor

        Returns
        -------
        Returns True if the morphisms mappings are identical, False otherwise.
        """
        if not isinstance(cat_functor,CategoryFunctor):
            raise Exception("RHS is not a category functor\n")

        if self is None or cat_functor is None:
            return False

        return cat_functor.morphisms_mapping==self.morphisms_mapping

class CategoryActionFunctor(object):
    def __init__(self,cat_action_source,cat_action_target,
                      cat_functor,nat_transform):
        """Instantiates a CategoryActionFunctor class, i.e. a functor from one
        category action S:C->Rel to another S':C'->Rel. This corresponds to the
        data of a functor N: C->C' along with a natural transformation
        eta: S->S'N.

        Parameters
        ----------
        cat_action_source, cat_action_target: instances of CategoryAction,
                    the domain and codomain of the category action functor.

        category_functor: an instance of CategoryFunctor, the functor N:C->C'.

        nat_transform: a dictionary representing the natural transformation
                       eta:S->S'N, where:
                       - the keys are object names in the source category action
                       S:C->Rel
                       - the values are instances of CatMorphism from the object
                       to their images.

        Returns
        -------
        None
        """
        ## Nat transform is a dictionary of CatMorphism, with keys the object
        ## names of cat_action_1

        if not isinstance(cat_action_source,CategoryAction):
           raise Exception("Source is not a valid CategoryAction class\n")
        if not isinstance(cat_action_target,CategoryAction):
            raise Exception("Target is not a valid CategoryAction class\n")
        if not isinstance(cat_functor,CategoryFunctor):
            raise Exception("The category morphism is not a valid CategoryFunctor class\n")
        self.cat_action_source = cat_action_source
        self.cat_action_target = cat_action_target
        self.cat_functor = cat_functor
        self.nat_transform = nat_transform

    def is_valid(self):
        """Checks if the given mappings are valid.
           In particular, the commutativity condition of the natural
           transformation should be respected.
           In the 2-category Rel, given a lax natural transformation N between
           two functors F and G, this means that there should be a 2-morphism
           from N_Y*F(f) to G(f)*N_X (i.e. the relation N_Y*F(f) is included in
           G(f)*N_X) for all morphisms f.

        Parameters
        ----------
        None

        Returns
        -------
        True if the given category action functor is valid, False otherwise
        """
        if not self.cat_functor.is_valid():
            return False

        ## see def of Rel_PKNets
        ## names of cat_action_1
        for name_f,f in self.cat_action_source.get_morphisms():
            source_name = f.source.name
            target_name = f.target.name
            nat_transform_source = self.nat_transform[source_name]
            nat_transform_target = self.nat_transform[target_name]
            image_name_f = self.cat_functor(name_f)
            image_morphism = self.cat_action_target.morphisms[image_name_f]
            if not (nat_transform_target*f)<=(image_morphism*nat_transform_source):
                return False
        return True

    def __mul__(self,cat_action_functor):
        """Compose two category action functors
        Overloads the '*' operator of Python

        Parameters
        ----------
        cat_action_functor : an instance of CategoryActionFunctor

        Returns
        -------
        The product self * cat_action_functor. Returns None if the two morphisms
        are not composable
        """
        if not cat_action_functor.cat_action_target==self.cat_action_source:
            return None

        new_cat_functor = self.cat_functor*cat_action_functor.cat_functor

        new_nat_transform = {}
        for obj,component in cat_action_functor.nat_transform.items():
            image_obj = component.target.name
            new_nat_transform[obj] = self.nat_transform[image_obj]*component

        new_cat_action_functor =  CategoryActionFunctor(cat_action_functor.cat_action_source,
                                                        self.cat_action_target,
                                                        new_cat_functor,
                                                        new_nat_transform)

        return new_cat_action_functor

    def __eq__(self,cat_action_functor):
        """Tests if two category action functors are equal

        Parameters
        ----------
        cat_action_functor : an instance of CategoryActionFunctor

        Returns
        -------
        Returns True if both the category functor, and the natural transformation
        are equal.
        """

        return self.cat_functor==cat_action_functor.cat_functor and \
               self.nat_transform==cat_action_functor.nat_transform
