# -*- coding: utf-8 -*-

################################################
###### Copyright (c) 2016, Alexandre Popoff
###

import numpy as np
import itertools
import time
from .categoryaction import CatObject

class MultQ(object):
    def __init__(self,x):
        """Initializes an element of the multiplicative quantale.

        Parameters
        ----------
        x: a float value between 0 and 1

        Returns
        -------
        None
        Raise an exception if the float value is not in the interval [0,1].
        """
        if x<0 or x>1:
            raise Exception("Real number should be comprised between 0 and 1")
        self.x = x

    @staticmethod
    def Unit():
        """Static method returning the unit of the monoid operation in the
        quantale.

        Parameters
        ----------
        None

        Returns
        -------
        The unit of the multiplicative quantale for the monoid operation.
        """
        return MultQ(1.0)

    @staticmethod
    def Zero():
        """Static method returning the zero value in the
        quantale.

        Parameters
        ----------
        None

        Returns
        -------
        The zero value in the quantale.
        """
        return MultQ(0.0)

    def __mul__(self,rhs):
        """Compose two numbers in the multiplicative quantale
        Overloads the '*' operator of Python

        Parameters
        ----------
        rhs : an instance of MultQ

        Returns
        -------
        The product self * rhs.
        In the case of the multiplicative quantale, it is the ordinary
        product of the two numbers.
        """
        if not isinstance(rhs,self.__class__):
            raise Exception("RHS is not a valid MultQ")
        return self.__class__(self.x*rhs.x)

    def __add__(self,rhs):
        """Compute the supremum in the multiplicative quantale
        Overloads the '+' operator of Python

        Parameters
        ----------
        rhs : an instance of MultQ

        Returns
        -------
        The supremum self v rhs.
        In the case of the multiplicative quantale, 'v' is the maximum
        of the two numbers.
        """
        if not isinstance(rhs,self.__class__):
            raise Exception("RHS is not a valid MultQ")
        return self.__class__(max([self.x,rhs.x]))

    def __eq__(self,rhs):
        """Checks if the two numbers in the multiplicative quantale are equal.
        Overloads the '==' operator of Python

        Parameters
        ----------
        rhs : an instance of MultQ

        Returns
        -------
        True if 'self' is equal to 'rhs'
        """
        if not isinstance(rhs,self.__class__):
            raise Exception("RHS is not a valid MultQ")
        return self.x==rhs.x

    def __lt__(self,rhs):
        """Checks if the given number is strictly inferior to the rhs given the
        poset structure of the multiplicative quantale.
        Overloads the '<' operator of Python

        Parameters
        ----------
        rhs : an instance of MultQ

        Returns
        -------
        True if 'self' is strictly inferior 'rhs'
        """
        if not isinstance(rhs,self.__class__):
            raise Exception("RHS is not a valid MultQ")
        return self.x<rhs.x

    def __le__(self,rhs):
        """Checks if the given number is inferior to the rhs given the
        poset structure of the multiplicative quantale.
        Overloads the '<=' operator of Python

        Parameters
        ----------
        rhs : an instance of MultQ

        Returns
        -------
        True if 'self' is inferior or equal to 'rhs'
        """
        if not isinstance(rhs,self.__class__):
            raise Exception("RHS is not a valid MultQ")
        return self.x<=rhs.x

    def __str__(self):
        """Returns a verbose description of the number in the multiplicative
        quantale.
        Overloads the 'str' operator of Python

        Parameters
        ----------
        None

        Returns
        -------
        A string description of the number value.
        """
        return str(self.x)

    def __repr__(self):
        return "MultQ({})".format(self.x)

class IntvQ(object):
    def __init__(self,x):
        """Initializes an element of the interval quantale.

        Parameters
        ----------
        x: a float value between 0 and 1

        Returns
        -------
        None
        Raise an exception if the float value is not in the interval [0,1].
        """
        if x<0 or x>1:
            raise Exception("Real number should be comprised between 0 and 1")
        self.x = x

    @staticmethod
    def Unit():
        """Static method returning the unit of the monoid operation in the
        quantale.

        Parameters
        ----------
        None

        Returns
        -------
        The unit of the multiplicative quantale for the monoid operation.
        """
        return IntvQ(1.0)

    @staticmethod
    def Zero():
        """Static method returning the zero value in the
        quantale.

        Parameters
        ----------
        None

        Returns
        -------
        The zero value in the quantale.
        """
        return IntvQ(0.0)

    def __mul__(self,rhs):
        """Compose two numbers in the interval quantale
        Overloads the '*' operator of Python

        Parameters
        ----------
        rhs : an instance of IntvQ

        Returns
        -------
        The product self * rhs.
        In the case of the interval quantale, it is the min of the two numbers.
        """
        if not isinstance(rhs,self.__class__):
            raise Exception("RHS is not a valid IntvQ")
        return self.__class__(min([self.x,rhs.x]))

    def __add__(self,rhs):
        """Compute the supremum in the interval quantale
        Overloads the '+' operator of Python

        Parameters
        ----------
        rhs : an instance of IntvQ

        Returns
        -------
        The supremum self v rhs.
        In the case of the interval quantale, 'v' is the maximum
        of the two numbers.
        """
        if not isinstance(rhs,self.__class__):
            raise Exception("RHS is not a valid IntvQ")
        return self.__class__(max([self.x,rhs.x]))

    def __eq__(self,rhs):
        """Checks if the two numbers in the interval quantale are equal.
        Overloads the '==' operator of Python

        Parameters
        ----------
        rhs : an instance of IntvQ

        Returns
        -------
        True if 'self' is equal to 'rhs'
        """
        if not isinstance(rhs,self.__class__):
            raise Exception("RHS is not a valid IntvQ")
        return self.x==rhs.x

    def __lt__(self,rhs):
        """Checks if the given number is strictly inferior to the rhs given the
        poset structure of the interval quantale.
        Overloads the '<' operator of Python

        Parameters
        ----------
        rhs : an instance of IntvQ

        Returns
        -------
        True if 'self' is strictly inferior 'rhs'
        """
        if not isinstance(rhs,self.__class__):
            raise Exception("RHS is not a valid IntvQ")
        return self.x<rhs.x

    def __le__(self,rhs):
        """Checks if the given number is inferior to the rhs given the
        poset structure of the interval quantale.
        Overloads the '<=' operator of Python

        Parameters
        ----------
        rhs : an instance of IntvQ

        Returns
        -------
        True if 'self' is inferior or equal to 'rhs'
        """
        if not isinstance(rhs,self.__class__):
            raise Exception("RHS is not a valid IntvQ")
        return self.x<=rhs.x

    def __str__(self):
        """Returns a verbose description of the number in the interval
        quantale.
        Overloads the 'str' operator of Python

        Parameters
        ----------
        None

        Returns
        -------
        A string description of the number value.
        """
        return str(self.x)

    def __repr__(self):
        return "IntvQ({})".format(self.x)


class Lin3Q(IntvQ):
    def __init__(self,x):
        """Initializes an element of the linear order quantale with 3 elements.
        It is a sub-quantale of the interval quantale with values 0, 1/2, and 1.

        Parameters
        ----------
        x: a float value between being either 0, 1/2, or 1.

        Returns
        -------
        None
        Raise an exception if the float value is not one of the above-mentionned
        values.
        """
        if not (x==0 or x==0.5 or x==1):
            raise Exception("The possibles values are 0, 1/2, and 1")
        super().__init__(x)

    @staticmethod
    def Unit():
        """Static method returning the unit of the monoid operation in the
        quantale.

        Parameters
        ----------
        None

        Returns
        -------
        The unit of the linear order quantale for the monoid operation.
        """
        return Lin3Q(1.0)

    @staticmethod
    def Zero():
        """Static method returning the zero value in the
        quantale.

        Parameters
        ----------
        None

        Returns
        -------
        The zero value in the quantale.
        """
        return Lin3Q(0.0)

    def __str__(self):
        return str(self.x)

    def __repr__(self):
        return "Lin3Q({})".format(self.x)


########################################################

class QMorphism(object):
    def __init__(self,name,source,target,qtype=None,mapping=None):
        """Initializes a quantaloid morphism between two sets.

        Parameters
        ----------
        name: a string representing the name of the morphism
        source: an instance of CatObject representing the domain of the morphism
        target: an instance of CatObject representing the codomain of
                the morphism
        qtype: class of quantale for the morphism
        mapping: optional argument representing the mapping of elements
                 between the domain and the codomain. The mapping can be
                 given as a NumPy array matrix or as a dictionary.

        Returns
        -------
        None
        Raises an exception if
        - the source is not an instance of a CatObject
        - the target is not an instance of a CatObject
        - the type (class) of quantale is not specified
        """
        if not isinstance(source,CatObject):
            raise Exception("Source is not a valid CatObject class\n")
        if not isinstance(target,CatObject):
            raise Exception("Target is not a valid CatObject class\n")
        if qtype is None:
            raise Exception("Type of quantale should be specified")
        self.name = name
        self.source = source
        self.target = target
        self.qtype = qtype
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
        M = np.empty((card_source,card_source),dtype=self.qtype)
        for i in range(card_source):
            for j in range(card_source):
                if i==j:
                    M[i,j] = self.qtype.Unit()
                else:
                    M[i,j] = self.qtype.Zero()
        self.matrix = M

    def set_mapping(self,mapping):
        """Sets the mapping of elements between the domain and the codomain

        Parameters
        ----------
        mapping: a dictionary, with:
                - keys: the element names in the domain of the morphism
                - values: a list of pairs of element names in the codomain of
                          the morphism and a number in the specified quantale.

        The mapping can be one-on-many as we are working in the category Rel(Q)
        of finite sets and quantale-valued relations.

        Returns
        -------
        None
        """
        card_source = self.source.get_cardinality()
        card_target = self.target.get_cardinality()

        self.matrix = np.empty((card_target,card_source),dtype=self.qtype)
        for i in range(card_source):
            for j in range(card_target):
                self.matrix[j,i] = self.qtype.Zero()

        for elem,images in sorted(mapping.items()):
            id_elem = self.source.get_idx_by_name(elem)
            for image,value in images:
                id_image = self.target.get_idx_by_name(image)
                self.matrix[id_image,id_elem] = self.qtype(value)

    def set_mapping_matrix(self,matrix):
        """Sets the mapping of elements between the domain and the codomain

        Parameters
        ----------
        matrix: a quantale-valued matrix (m,n), where m is the cardinality of the codomain
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
                - values: a list of pairs of element names in the
                          codomain of the morphism with the value in the
                          quantale
        """
        dest_cardinality,source_cardinality = self.matrix.shape
        d={}
        for i in range(source_cardinality):
            l=[]
            for j in range(dest_cardinality):
                v = self.matrix[j,i]
                l.append((self.target.get_name_by_idx(j),v.x))
            d[self.source.get_name_by_idx(i)]=l
        return d

    def get_mapping_matrix(self):
        """Retrieves the mapping in matrix form

        Parameters
        ----------
        None

        Returns
        -------
        A boolean matrix representing the morphism in Rel(Q)
        """
        return self.matrix

    def copy(self):
        """Copy the current morphism

        Parameters
        ----------
        None

        Returns
        -------
        A new instance of QMorphism with the same domain, codomain, and mapping
        """
        U = QMorphism(self.name,self.source,self.target,qtype=self.qtype)
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

        return np.all(np.sum(self.matrix,axis=0)>self.qtype.Zero())


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
            descr += s+"->"+(",".join([(x[0],str(x[1])) for x in t]))+"\n"
        return descr

    def __call__(self,elem):
        """Apply the current morphism to an element of its domain

        Parameters
        ----------
        elem : string representing an element of self.source

        Returns
        -------
        List of pairs of elements and quantale values mapped by the given
        QMorphism.
        """
        idx_elem = self.source.get_idx_by_name(elem)
        return [(self.target.get_name_by_idx(j),v.x) for j,v in enumerate(self.matrix[:,idx_elem]) if v!=self.qtype.Zero()]

    def __pow__(self,int_power):
        """Raise the morphism to the power int_power
        Overloads the '**' operator of Python

        Parameters
        ----------
        int_power : an integer

        Returns
        -------
        The power self^int_power. Raises an exception if the morphism is not an
        endomorphism.
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
        Raises an exception if the rhs is not a QMorphism, or if the two
        QMorphisms are of different quantale types.
        Returns None if the two morphisms are not composable.
        """

        if not isinstance(morphism,QMorphism):
            raise Exception("RHS is not a valid QMorphism class\n")
        if not self.qtype==morphism.qtype:
            raise Exception("QMorphisms use different quantales")
        if not morphism.target==self.source:
            return None
        new_morphism =  QMorphism(self.name+morphism.name,morphism.source,self.target,qtype=self.qtype)
        new_morphism.set_mapping_matrix((self.matrix.dot(morphism.matrix)))

        return new_morphism

    def __eq__(self,morphism):
        """Checks if the given morphism is equal to 'morphism'
        Overloads the '==' operator of Python

        Parameters
        ----------
        morphism : an instance of QMorphism

        Returns
        -------
        True if 'self' is equal to 'morphism'
        Raises an exception if the rhs is not a QMorphism, or if the two
        QMorphisms are of different quantale types.
        """
        if not isinstance(morphism,QMorphism):
            raise Exception("RHS is not a valid QMorphism class\n")
        if not self.qtype==morphism.qtype:
            raise Exception("QMorphisms use different quantales")
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
        morphism : an instance of QMorphism

        Returns
        -------
        True if 'self' is included in 'morphism'
        Raises an exception if the rhs is not a QMorphism, or if the two
        QMorphisms are of different quantale types, or if the domain and codomain
        differ.
        """
        if not isinstance(morphism,QMorphism):
            raise Exception("RHS is not a valid CatMorphism class\n")
        if not self.qtype==morphism.qtype:
            raise Exception("QMorphisms use different quantales")
        if self is None or morphism is None:
            return False
        if not (self.source == morphism.source) and (self.target == morphism.target):
            raise Exception("Morphisms should have the same domain and codomain")
        return np.all(self.matrix<=morphism.matrix)

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
        Raises an exception if the rhs is not a QMorphism, or if the two
        QMorphisms are of different quantale types, or if the domain and codomain
        differ.
        """

        if not isinstance(morphism,QMorphism):
            raise Exception("RHS is not a valid CatMorphism class\n")
        if not self.qtype==morphism.qtype:
            raise Exception("QMorphisms use different quantales")
        if not (self.source == morphism.source) and (self.target == morphism.target):
            raise Exception("Morphisms should have the same domain and codomain")
        if self is None or morphism is None:
            return False
        return np.all(self.matrix<morphism.matrix)

########################################"""


class CategoryQAction(object):
    def __init__(self,qtype=None,objects=None,generators=None,generate=True):
        """Instantiates a CategoryQAction class with morphisms in a given
           quantale

        Parameters
        ----------
        objects: optional list of CatObject instances representing
                 the objects in the category.

        generators: optional list of QMorphism instances
                 representing the generators of the category.

        generator: optional boolean indicating whether the category
                   should be generated upon instantiation.

        Returns
        -------
        None
        Raises an exception if the quantale type (class) is not specified.
        """
        if qtype is None:
            raise Exception("Type of quantale should be specified")
        self.qtype=qtype
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
            - y is the corresponding instance of QMorphism
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
            - y is the corresponding instance of QMorphism
        """
        return list(sorted(self.generators.items()))

    def set_generators(self,list_morphisms):
        """Set generators to the category action. This erases
        all previous morphisms and generators.

        Parameters
        ----------
        list_morphisms: a list of QMorphism instances representing the
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
            if not isinstance(m,QMorphism):
                raise Exception("Generator is not a valid QMorphism class\n")
            if not m.source.name in cat_obj_names:
                raise Exception("Domain or codomain of a generator is not present in the category")
            if not m.target.name in cat_obj_names:
                raise Exception("Domain or codomain of a generator is not present in the category")
            self.generators[m.name] = m

    def _add_morphisms(self,list_morphisms):
        """Add morphisms to the category action.

        Parameters
        ----------
        list_morphisms: a list of QMorphism instances representing the
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
            identity_morphism = QMorphism("id_"+name,catobject,catobject,qtype=self.qtype)
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
        A list of pairs representing the images of elem by name_f and their
        quantale values.
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
                if element_2 in [x[0] for x in f(element_1)]:
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
