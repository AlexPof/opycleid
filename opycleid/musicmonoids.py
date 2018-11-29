# -*- coding: utf-8 -*-

################################################
###### Copyright (c) 2016, Alexandre Popoff
###

import numpy as np
from .categoryaction import CatObject,CatMorphism,MonoidAction

class Noll_Monoid(MonoidAction):
    """Defines the Noll monoid acting on the set of the twelve pitch classes.
    The Noll monoid is generated by the two transformations
        - f(x)=3x+7
        - g(x)=8x+4

    """
    def __init__(self):
        super(Noll_Monoid,self).__init__()
        X = CatObject(".",["C","Cs","D","Eb","E","F","Fs","G","Gs","A","Bb","B"])
        self.set_objects([X])

        F = CatMorphism("f",X,X)
        M_F = np.zeros((12,12),dtype=bool)
        for i in range(12):
            M_F[(3*i+7)%12,i] = True
        F.set_mapping_matrix(M_F)

        G = CatMorphism("g",X,X)
        M_G = np.zeros((12,12),dtype=bool)
        for i in range(12):
            M_G[(8*i+4)%12,i] = True
        G.set_mapping_matrix(M_G)

        self.add_generators([F,G])
        self.generate_category()


class TI_Group_PC(MonoidAction):
    """Defines the TI group acting on the set of the twelve pitch classes.
    """
    def __init__(self):
        super(TI_Group_PC,self).__init__()

        X = CatObject(".",["C","Cs","D","Eb","E","F","Fs","G","Gs","A","Bb","B"])
        self.set_objects([X])

        T = CatMorphism("T1",X,X)
        M_T = np.zeros((12,12),dtype=bool)
        for i in range(12):
            M_T[(i+1)%12,i]=True
        T.set_mapping_matrix(M_T)

        I = CatMorphism("I0",X,X)
        M_I = np.zeros((12,12),dtype=bool)
        for i in range(12):
            M_I[(-i)%12,i]=True
        I.set_mapping_matrix(M_I)

        self.add_generators([T,I])
        self.add_identities()
        self.add_morphisms([T,I])
        for i in range(2,12):
            x = self.operations['id_.']
            for j in range(i):
                x = T*x
            x.set_name("T"+str(i))
            self.add_morphisms([x])
        for i in range(1,12):
            x = self.operations['id_.']
            for j in range(i):
                x = T*x
            y = x*I
            y.set_name("I"+str(i))
            self.add_morphisms([y])


class TI_Group_Triads(MonoidAction):
    """Defines the TI group acting on the set of the 24 major and minor triads.
    """
    def __init__(self):
        super(TI_Group_Triads,self).__init__()

        X = CatObject(".",["C_M","Cs_M","D_M","Eb_M","E_M","F_M","Fs_M","G_M","Gs_M","A_M","Bb_M","B_M",
                           "C_m","Cs_m","D_m","Eb_m","E_m","F_m","Fs_m","G_m","Gs_m","A_m","Bb_m","B_m"])
        self.set_objects([X])

        T = CatMorphism("T1",X,X)
        M_T = np.zeros((24,24),dtype=bool)
        for i in range(12):
            M_T[(i+1)%12,i]=True
            M_T[12+(i+1)%12,i+12]=True
        T.set_mapping_matrix(M_T)

        I = CatMorphism("I0",X,X)
        M_I = np.zeros((24,24),dtype=bool)
        for i in range(12):
            M_I[(5-i)%12 + 12,i]=True
            M_I[(5-i)%12, i+12]=True
        I.set_mapping_matrix(M_I)

        self.add_generators([T,I])
        self.add_identities()
        self.add_morphisms([T,I])
        for i in range(2,12):
            x = self.operations['id_.']
            for j in range(i):
                x = T*x
            x.set_name("T"+str(i))
            self.add_morphisms([x])
        for i in range(1,12):
            x = self.operations['id_.']
            for j in range(i):
                x = T*x
            y = x*I
            y.set_name("I"+str(i))
            self.add_morphisms([y])

class PRL_Group(MonoidAction):
    """Defines the neo-Riemannian PRL group acting on the set
    of the 24 major and minor triads.
    """
    def __init__(self):
        super(PRL_Group,self).__init__()

        X = CatObject(".",["C_M","Cs_M","D_M","Eb_M","E_M","F_M","Fs_M","G_M","Gs_M","A_M","Bb_M","B_M",
                           "C_m","Cs_m","D_m","Eb_m","E_m","F_m","Fs_m","G_m","Gs_m","A_m","Bb_m","B_m"])
        self.set_objects([X])

        L = CatMorphism("L",X,X)
        M_L = np.zeros((24,24),dtype=bool)
        for i in range(12):
            M_L[(i+4)%12 + 12,i]=True
            M_L[(i+8)%12,12+i]=True
        L.set_mapping_matrix(M_L)

        R = CatMorphism("R",X,X)
        M_R = np.zeros((24,24),dtype=bool)
        for i in range(12):
            M_R[(i+9)%12 + 12,i]=True
            M_R[(i+3)%12,12+i]=True
        R.set_mapping_matrix(M_R)

        P = CatMorphism("P",X,X)
        M_P = np.zeros((24,24),dtype=bool)
        for i in range(12):
            M_P[i%12 + 12,i]=True
            M_P[i%12,12+i]=True
        P.set_mapping_matrix(M_P)

        self.add_generators([P,R,L])
        self.add_identities()
        self.generate_category()

class UTT_Group(MonoidAction):
    """Defines Hook's UTT group acting on the set of the 24 major and minor triads.
    Each element of the group (whose order is equal to 244) is of the form <p,q,s>.
    s is a signature (+ or -):
        - if s is +, the element sends a major triad of root n to n+p,
                    and a minor triad of root n to n+q
        - if s is -, the element sends a major triad of root n to n+q,
                    and a minor triad of root n to n+p
    """
    def __init__(self):
        super(UTT_Group,self).__init__()

        X = CatObject(".",["C_M","Cs_M","D_M","Eb_M","E_M","F_M","Fs_M","G_M","Gs_M","A_M","Bb_M","B_M",
                           "C_m","Cs_m","D_m","Eb_m","E_m","F_m","Fs_m","G_m","Gs_m","A_m","Bb_m","B_m"])
        self.set_objects([X])

        T = CatMorphism("T",X,X)
        M_T = np.zeros((24,24),dtype=bool)
        for i in range(12):
            M_T[(i+1)%12,i]=True
            M_T[i+12,i+12]=True
        T.set_mapping_matrix(M_T)

        I = CatMorphism("I",X,X)
        M_I = np.zeros((24,24),dtype=bool)
        for i in range(12):
            M_I[i + 12,i]=True
            M_I[i, i+12]=True
        I.set_mapping_matrix(M_I)

        self.add_generators([T,I])
        self.generate_category()

        ## Quick rewriting of the operation names to conform to
        ## Hook's terminology for UTTs

        new_operations = []
        for name_f,f in sorted(self.operations.items()):
            op = [0,0,0]
            for j in name_f[::-1]:
                if j=="T":
                    op[op[2]]=op[op[2]]+1
                if j=="I":
                    op[2]=1-op[2]
            new_name = "<"+str(op[0])+","+str(op[1])+","+("+"*(op[2]==0)+"-"*(op[2]==1))+">"
            new_morphism = CatMorphism(new_name,X,X)
            new_morphism.set_mapping_matrix(f.get_mapping_matrix())
            new_operations.append(new_morphism)

        self.set_objects([X]) ## This erases previous morphisms
        self.add_morphisms(new_operations)
        self.generators = {"<1,0,+>":self.operations["<1,0,+>"],"<0,0,->":self.operations["<0,0,->"]}

class Left_Z3Q8_Group(MonoidAction):
    """Defines a simply transitive generalized neo-Riemannian group acting
        on the left on the set of the 24 major and minor triads.
        The group is an extension of Z_12 by Z_2 with a non-trivial cocycle.
    """
    def __init__(self):
        super(Left_Z3Q8_Group,self).__init__()

        X = CatObject(".",["C_M","Cs_M","D_M","Eb_M","E_M","F_M","Fs_M","G_M","Gs_M","A_M","Bb_M","B_M",
                           "C_m","Cs_m","D_m","Eb_m","E_m","F_m","Fs_m","G_m","Gs_m","A_m","Bb_m","B_m"])
        self.set_objects([X])

        T = CatMorphism("T1",X,X)
        M_T = np.zeros((24,24),dtype=bool)
        for i in range(12):
            M_T[(i+1)%12,i]=True
            M_T[12+(i+1)%12,i+12]=True
        T.set_mapping_matrix(M_T)

        J = CatMorphism("J0",X,X)
        M_J = np.zeros((24,24),dtype=bool)
        for i in range(12):
            M_J[(-i)%12 + 12,i]=True
            M_J[(-i+6)%12, i+12]=True
        J.set_mapping_matrix(M_J)

        self.add_generators([T,J])
        self.add_identities()
        self.add_morphisms([T,J])
        for i in range(2,12):
            x = self.operations['id_.']
            for j in range(i):
                x = x*T
            x.set_name("T"+str(i))
            self.add_morphisms([x])
        for i in range(1,12):
            x = self.operations['id_.']
            for j in range(i):
                x = x*T
            y=x*J
            y.set_name("J"+str(i))
            self.add_morphisms([y])

class Right_Z3Q8_Group(MonoidAction):
    """Defines a simply transitive generalized neo-Riemannian group acting
        on the right on the set of the 24 major and minor triads.
        The group is an extension of Z_12 by Z_2 with a non-trivial cocycle.
    """
    def __init__(self):
        super(Right_Z3Q8_Group,self).__init__()

        X = CatObject(".",["C_M","Cs_M","D_M","Eb_M","E_M","F_M","Fs_M","G_M","Gs_M","A_M","Bb_M","B_M",
                           "C_m","Cs_m","D_m","Eb_m","E_m","F_m","Fs_m","G_m","Gs_m","A_m","Bb_m","B_m"])
        self.set_objects([X])

        T = CatMorphism("T1",X,X)
        M_T = np.zeros((24,24),dtype=bool)
        for i in range(12):
            M_T[(i+1)%12,i]=True
            M_T[12+(i-1)%12,i+12]=True
        T.set_mapping_matrix(M_T)

        J = CatMorphism("J0",X,X)
        M_J = np.zeros((24,24),dtype=bool)
        for i in range(12):
            M_J[i + 12,i]=True
            M_J[(i+6)%12, i+12]=True
        J.set_mapping_matrix(M_J)

        self.add_generators([T,J])
        self.add_identities()
        self.add_morphisms([T,J])
        for i in range(2,12):
            x = self.operations['id_.']
            for j in range(i):
                x = x*T
            x.set_name("T"+str(i))
            self.add_morphisms([x])
        for i in range(1,12):
            x = self.operations['id_.']
            for j in range(i):
                x = x*T
            y=x*J
            y.set_name("J"+str(i))
            self.add_morphisms([y])


class UPL_Monoid(MonoidAction):
    """Defines a monoid acting on the set of the 28 major, minor,
        and augmented triads by relations.
        It is generated by three operations:
        - P and L are the relational equivalent of the neo-Riemannian
            P and L operations.
        - U is the relation such that we have xUy whenever x (or y)
            is an augmented triad, and the other chord has
            two tones in common with x (or y)
    """
    def __init__(self):
        super(UPL_Monoid,self).__init__()

        X = CatObject(".",["C_M","Cs_M","D_M","Eb_M","E_M","F_M","Fs_M","G_M","Gs_M","A_M","Bb_M","B_M",
                           "C_m","Cs_m","D_m","Eb_m","E_m","F_m","Fs_m","G_m","Gs_m","A_m","Bb_m","B_m",
                           "C_aug","F_aug","D_aug","G_aug"])
        self.set_objects([X])

        P = CatMorphism("P",X,X)
        M_P = np.zeros((28,28),dtype=bool)
        for i in range(12):
            M_P[i+12,i]=True
            M_P[i,i+12]=True
        for i in range(24,28):
            M_P[i,i]=True
        P.set_mapping_matrix(M_P)

        L = CatMorphism("L",X,X)
        M_L = np.zeros((28,28),dtype=bool)
        for i in range(12):
            M_L[(i+4)%12+12,i]=True
            M_L[(i+8)%12,12+i]=True
        for i in range(24,28):
            M_L[i,i]=True
        L.set_mapping_matrix(M_L)

        U = CatMorphism("U",X,X)
        M_U = np.zeros((28,28),dtype=bool)
        for i in range(12):
            M_U[24+(i%4),i]=True
            M_U[i,24+(i%4)]=True

            M_U[24+((i+3)%4),12+i]=True
            M_U[12+i,24+((i+3)%4)]=True
        U.set_mapping_matrix(M_U)

        self.add_generators([P,L,U])
        self.generate_category()


class S_Monoid(MonoidAction):
    """Defines a monoid acting on the set of the 28 major, minor,
        and augmented triads by relations.
        It is generated by the S=P_1,0 relation, i.e. we have x(P_1,0)y
        whenever the chord x differ from y by the movement
        of a single note by a semitone.
    """
    def __init__(self):
        super(S_Monoid,self).__init__()

        X = CatObject(".",["C_M","Cs_M","D_M","Eb_M","E_M","F_M","Fs_M","G_M","Gs_M","A_M","Bb_M","B_M",
                           "C_m","Cs_m","D_m","Eb_m","E_m","F_m","Fs_m","G_m","Gs_m","A_m","Bb_m","B_m",
                           "C_aug","F_aug","D_aug","G_aug"])
        self.set_objects([X])

        S = CatMorphism("S",X,X)
        M_S = np.zeros((28,28),dtype=bool)
        for i in range(12):
            M_S[24+(i%4),i]=True
            M_S[i,24+(i%4)]=True

            M_S[24+((i+3)%4),12+i]=True
            M_S[12+i,24+((i+3)%4)]=True

            M_S[12+i,i]=True
            M_S[i,12+i]=True

            M_S[12+(i+4)%12,i]=True
            M_S[i,12+(i+4)%12]=True
        S.set_mapping_matrix(M_S)

        self.add_generators([S])
        self.generate_category()



class T_Monoid(MonoidAction):
    """Defines a monoid acting on the set of the 28 major, minor,
        and augmented triads by relations.
        It is generated by the T=P_2,0 relation, i.e. we have x(P_2,0)y
        whenever the chord x differ from y by the movement
        of two notes by a semitone each.
    """
    def __init__(self):
        super(T_Monoid,self).__init__()

        X = CatObject(".",["C_M","Cs_M","D_M","Eb_M","E_M","F_M","Fs_M","G_M","Gs_M","A_M","Bb_M","B_M",
                           "C_m","Cs_m","D_m","Eb_m","E_m","F_m","Fs_m","G_m","Gs_m","A_m","Bb_m","B_m",
                           "C_aug","F_aug","D_aug","G_aug"])
        self.set_objects([X])

        T = CatMorphism("T",X,X)
        M_T = np.zeros((28,28),dtype=bool)
        for i in range(12):
            M_T[(i+4)%12,i]=True
            M_T[i,(i+4)%12]=True

            M_T[(i+8)%12,i]=True
            M_T[i,(i+8)%12]=True

            M_T[12+(i+1)%12,i]=True
            M_T[i,12+(i+1)%12]=True

            M_T[12+(i+5)%12,i]=True
            M_T[i,12+(i+5)%12]=True

            M_T[24+((i+3)%4),i]=True
            M_T[i,24+((i+3)%4)]=True

        for i in range(12):
            M_T[24+(i%4),12+i]=True
            M_T[12+i,24+(i%4)]=True

            M_T[12+(i+4)%12,12+i]=True
            M_T[12+i,12+(i+4)%12]=True

            M_T[12+(i+8)%12,12+i]=True
            M_T[12+i,12+(i+8)%12]=True
        T.set_mapping_matrix(M_T)

        self.add_generators([T])
        self.generate_category()


class K_Monoid(MonoidAction):
    """Defines a monoid acting on the set of the 28 major, minor,
        and augmented triads by relations.
        It is generated by the K=P_2,1 relation, i.e. we have x(P_2,1)y
        whenever the chord x differ from y by the movement of two notes
        by a semitone each, and the remaining note by a tone.
    """
    def __init__(self):
        super(K_Monoid,self).__init__()

        X = CatObject(".",["C_M","Cs_M","D_M","Eb_M","E_M","F_M","Fs_M","G_M","Gs_M","A_M","Bb_M","B_M",
                           "C_m","Cs_m","D_m","Eb_m","E_m","F_m","Fs_m","G_m","Gs_m","A_m","Bb_m","B_m",
                           "C_aug","F_aug","D_aug","G_aug"])
        self.set_objects([X])

        K = CatMorphism("K",X,X)
        M_K = np.zeros((28,28),dtype=bool)
        for i in range(12):
            M_K[12+(i+3)%12,i]=True
            M_K[i,12+(i+3)%12]=True

            M_K[12+(i+11)%12,i]=True
            M_K[i,12+(i+11)%12]=True

            M_K[24+((i+1)%4),i]=True
            M_K[i,24+((i+1)%4)]=True

            M_K[24+((i+2)%4),12+i]=True
            M_K[12+i,24+((i+2)%4)]=True
        K.set_mapping_matrix(M_K)

        self.add_generators([K])
        self.generate_category()


class W_Monoid(MonoidAction):
    """Defines a monoid acting on the set of the 28 major, minor,
        and augmented triads by relations.
        It is generated by the K=P_1,2 relation, i.e. we have x(P_2,1)y
        whenever the chord x differ from y by the movement of a single note
        by a semitone, and the remaining notes by a tone each.
    """
    def __init__(self):
        super(W_Monoid,self).__init__()

        X = CatObject(".",["C_M","Cs_M","D_M","Eb_M","E_M","F_M","Fs_M","G_M","Gs_M","A_M","Bb_M","B_M",
                           "C_m","Cs_m","D_m","Eb_m","E_m","F_m","Fs_m","G_m","Gs_m","A_m","Bb_m","B_m",
                           "C_aug","F_aug","D_aug","G_aug"])
        self.set_objects([X])

        W = CatMorphism("W",X,X)
        M_W = np.zeros((28,28),dtype=bool)
        for i in range(12):
            M_W[12+(i+2)%12,i]=True
            M_W[i,12+(i+2)%12]=True

            M_W[12+(i+6)%12,i]=True
            M_W[i,12+(i+6)%12]=True

            M_W[24+((i+2)%4),i]=True
            M_W[i,24+((i+2)%4)]=True

            M_W[24+((i+1)%4),12+i]=True
            M_W[12+i,24+((i+1)%4)]=True
        W.set_mapping_matrix(M_W)

        self.add_generators([W])
        self.generate_category()



class ST_Monoid(MonoidAction):
    """Defines a monoid acting on the set of the 28 major, minor,
        and augmented triads by relations.
        It is generated by the S and T operations presented above.
    """
    def __init__(self):
        super(ST_Monoid,self).__init__()

        X = CatObject(".",["C_M","Cs_M","D_M","Eb_M","E_M","F_M","Fs_M","G_M","Gs_M","A_M","Bb_M","B_M",
                           "C_m","Cs_m","D_m","Eb_m","E_m","F_m","Fs_m","G_m","Gs_m","A_m","Bb_m","B_m",
                           "C_aug","F_aug","D_aug","G_aug"])
        self.set_objects([X])

        S = CatMorphism("S",X,X)
        M_S = np.zeros((28,28),dtype=bool)
        for i in range(12):
            M_S[24+(i%4),i]=True
            M_S[i,24+(i%4)]=True

            M_S[24+((i+3)%4),12+i]=True
            M_S[12+i,24+((i+3)%4)]=True

            M_S[12+i,i]=True
            M_S[i,12+i]=True

            M_S[12+(i+4)%12,i]=True
            M_S[i,12+(i+4)%12]=True
        S.set_mapping_matrix(M_S)

        T = CatMorphism("T",X,X)
        M_T = np.zeros((28,28),dtype=bool)
        for i in range(12):
            M_T[(i+4)%12,i]=True
            M_T[i,(i+4)%12]=True

            M_T[(i+8)%12,i]=True
            M_T[i,(i+8)%12]=True

            M_T[12+(i+1)%12,i]=True
            M_T[i,12+(i+1)%12]=True

            M_T[12+(i+5)%12,i]=True
            M_T[i,12+(i+5)%12]=True

            M_T[24+((i+3)%4),i]=True
            M_T[i,24+((i+3)%4)]=True

        for i in range(12):
            M_T[24+(i%4),12+i]=True
            M_T[12+i,24+(i%4)]=True

            M_T[12+(i+4)%12,12+i]=True
            M_T[12+i,12+(i+4)%12]=True

            M_T[12+(i+8)%12,12+i]=True
            M_T[12+i,12+(i+8)%12]=True
        T.set_mapping_matrix(M_T)

        self.add_generators([S,T])
        self.generate_category()
