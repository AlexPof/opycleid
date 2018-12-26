# -*- coding: utf-8 -*-

################################################
###### Copyright (c) 2016, Alexandre Popoff
###

import numpy as np
import itertools
import time

class CatObject(object):
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
        return sorted(self.dict_elem2idx.keys())

    def get_cardinality(self):
        return len(self.dict_idx2elem)

    def is_in(self,elem):
        return elem in self.dict_elem2idx

class CatMorphism(object):
    def __init__(self,name,source,target):
        self.name = name
        self.source = source
        self.target = target

    def set_name(self,name):
        if not len(name):
            raise Exception("The specified morphism name is empty")
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
        for elem,images in sorted(mapping.items()):
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

    def copy(self):
        U = CatMorphism(self.name,self.source,self.target)
        U.set_mapping_matrix(self.get_mapping_matrix())

        return U

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
        True if 'self' is included in 'morphism'
        """

        return (self<=morphism) and (not self==morphism)


class CategoryAction(object):
    def __init__(self):
        self.objects={}
        self.generators={}
        self.morphisms={}
        self.equivalences=[]

    def set_objects(self,list_objects):
        self.objects={}
        self.generators={}
        self.morphisms={}
        self.equivalences=[]
        for catobject in list_objects:
            self.objects[catobject.name] = catobject

    def get_objects(self):
        return list(sorted(self.objects.items()))

    def get_morphisms(self):
        return list(sorted(self.morphisms.items()))

    def get_generators(self):
        return list(sorted(self.generators.items()))

    def add_generators(self,list_morphisms):
        for catmorphism in list_morphisms:
            self.generators[catmorphism.name] = catmorphism

    def add_morphisms(self,list_morphisms):
        for catmorphism in list_morphisms:
            self.morphisms[catmorphism.name] = catmorphism

    def add_identities(self):
        for name,catobject in sorted(self.objects.items()):
            identity_morphism = CatMorphism("id_"+name,catobject,catobject)
            identity_morphism.set_to_identity()
            self.add_morphisms([identity_morphism])

    def generate_category(self):
        self.morphisms = self.generators.copy()
        self.add_identities()
        new_liste = self.generators.copy()
        added_liste = self.generators.copy()
        while(len(added_liste)>0):
            added_liste = {}
            for name_x,morphism_x in sorted(new_liste.items()):
                for name_g,morphism_g in self.get_generators():
                    try:
                        c=0
                        new_morphism = morphism_g*morphism_x
                        for name_y,morphism_y in self.get_morphisms():
                            if new_morphism==morphism_y:
                                c=1
                                self.equivalences.append([new_morphism.name,morphism_y.name])
                        if c==0:
                            added_liste[new_morphism.name] = new_morphism
                            self.morphisms[new_morphism.name] = new_morphism
                    except:
                        pass
            new_liste = added_liste

    def mult(self,name_g,name_f):
        new_morphism = self.morphisms[name_g]*self.morphisms[name_f]
        return [name_x for name_x,x in self.get_morphisms() if x==new_morphism][0]

    def apply_operation(self,name_f,elem):
        return self.morphisms[name_f]>>elem

    def get_operation(self,elem1,elem2):
        res = []
        for name_f,f in self.get_morphisms():
            try:
                if elem2 in f>>elem1:
                    res.append(name_f)
            except:
                pass
        return res

    def rename_operation(self,name_f,new_name):
        if not name_f in self.morphisms:
            raise Exception("The specified operation cannot be found")
        new_op = self.morphisms[name_f].copy()
        new_op.set_name(new_name)
        del self.morphisms[name_f]
        self.morphisms[new_name] = new_op

    def rewrite_operations(self):
        operation_names = sorted(self.morphisms.keys())
        for op_name in operation_names:
            self.rename_operation(op_name,self.rewrite(op_name))

        equivalences_new=[]
        for x,y in self.equivalences:
            equivalences_new.append([self.rewrite(x),self.rewrite(y)])
        self.equivalences = equivalences_new

    def rewrite(self,the_string):
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
        return str(self.morphisms[name_f])

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
        object_list : a list of XXXX should

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
    def __init__(self,cat_action_1,cat_action_2):
        if not isinstance(cat_action_1,CategoryAction):
           raise Exception("Source is not a valid CategoryAction class\n")
        if not isinstance(cat_action_2,CategoryAction):
            raise Exception("Target is not a valid CategoryAction class\n")
        self.cat_action_1 = cat_action_1
        self.cat_action_2 = cat_action_2
        self.object_mapping = None
        self.morphisms_mapping = None
        self.generators_mapping = None


    def set_fullmapping(object_mapping,morphism_mapping):
        self.object_mapping = object_mapping
        self.morphisms_mapping = morphism_mapping
        self.generators_mapping = {}
        for name_f,f in self.cat_action_1.get_generators():
            self.generators_mapping[name_f] = morphism_mapping[name_f]
        return self.is_valid()

    def set_from_generator_mapping(self,gen_mapping):

        if not gen_mapping.keys()==self.cat_action_1.generators.keys():
            return False

        ## First we need to check if the mapping defines a valid mapping
        ## between objects
        num_objects = len(self.cat_action_1.get_objects())

        object_mapping=[]
        for f,image_f in gen_mapping.items():
            s1 = self.cat_action_1.morphisms[f].source.name
            s2 = self.cat_action_2.morphisms[image_f].source.name
            t1 = self.cat_action_1.morphisms[f].target.name
            t2 = self.cat_action_2.morphisms[image_f].target.name
            object_mapping.append((s1,s2))
            object_mapping.append((t1,t2))
        object_mapping = set(object_mapping)
        if not len(object_mapping)==num_objects:
            return False

        full_mapping = gen_mapping.copy()
        for obj,image_obj in object_mapping:
            full_mapping["id_"+obj] = "id_"+image_obj

        new_liste = self.cat_action_1.generators.copy()
        added_liste = self.cat_action_1.generators.copy()

        ## This is a variant of the category action generation method.
        ## It generates the category and their images by the map of generators.
        ## If it does not give a multi-valued function, we get the corresponding
        ## functor.

        while(len(added_liste)>0):
            added_liste = []
            for name_x in new_liste:
                for name_g,g in self.cat_action_1.get_generators():
                    try:
                        name_product = self.cat_action_1.mult(name_g,name_x)
                        name_imageproduct = self.cat_action_2.mult(full_mapping[name_g],full_mapping[name_x])
                        if not name_product in full_mapping:
                            added_liste.append(name_product)
                            full_mapping[name_product] = name_imageproduct
                        else:
                            ## If the generated element already exists, we check that its existing image corresponds
                            ## to the image which has just been calculated
                            if not full_mapping[name_product] == name_imageproduct:
                                ## We have a multi-valued function so the algorithm stops there
                                return False
                    except:
                        pass
            new_liste = added_liste[:]

        self.generators_mapping = gen_mapping.copy()
        self.object_mapping = dict(object_mapping)
        self.morphisms_mapping = full_mapping.copy()

        ## By construction, this is functorial, so there is no need to check
        ## with the is_valid() method
        return True

    def get_image_object(self,object_name):
        return self.object_mapping[object_name]

    def get_image_morphism(self,morphism_name):
        return self.morphisms_mapping[morphism_name]

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

    def is_automorphism(self):

        if not self.cat_action_1 == self.cat_action_2:
            return False

        ## We first need to check that the object mapping is bijective

        num_objects = len(self.cat_action_1.get_objects())
        if not (len(set(self.object_mapping.keys()))==num_objects and \
               len(set(self.object_mapping.values()))==num_objects):
           return False

        ## Then we need to check if the morphism mapping is bijective

        num_morphisms = len(self.cat_action_1.get_morphisms())

        if not (len(set(self.morphisms_mapping.keys()))==num_morphisms and \
               len(set(self.morphisms_mapping.values()))==num_morphisms):
           return False

        return True

class CategoryActionFunctor(object):
    def __init__(self,cat_action_1,cat_action_2,category_morphism,nat_transform):
        ## Nat transform is a dictionary of CatMorphism, with keys the object
        ## names of cat_action_1

        if not isinstance(cat_action_1,CategoryAction):
           raise Exception("Source is not a valid CategoryAction class\n")
        if not isinstance(cat_action_2,CategoryAction):
            raise Exception("Target is not a valid CategoryAction class\n")
        if not isinstance(category_morphism,CategoryFunctor):
            raise Exception("The category morphism is not a valid CategoryFunctor class\n")
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
