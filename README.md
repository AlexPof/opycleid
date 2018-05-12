![PyPi](https://badge.fury.io/py/opycleid.svg)

# opycleid
Opycleid - A Python package for transformational music theory

The complete documentation is [available here](https://alexpof.github.io/opycleid/)

How to use opycleid
==========

Transformational music analysis is easily implemented in a few lines, with the group/monoid of your choice:

    >>> from opycleid.musicmonoids import PRL_Group,TI_Group_Triads,TI_Group_PC

Let's work first with pitch classes... what operations in the T/I group takes C to A ?

    >>> my_group = TI_Group_PC()
    >>> my_group.get_operation("C","A")
    ['I9', 'T9']

Let's now work with major and minor triads... what operations in the T/I group takes C major to B minor ?

    >>> my_group = TI_Group_Triads()
    >>> my_group.get_operation("C_M","B_m")
    ['I6']

What would it be if we use the PRL group instead ?

    >>> my_group = PRL_Group()
    >>> my_group.get_operation("C_M","B_m")
    ['LRL']

What do we get if we apply that same operation to a D major chord (Answer: C sharp minor) ?

    >>> my_group.apply_operation("LRL","D_M")
    ['Cs_m']

What are the operations in the PRL group ?

    >>> list(my_group.operations.keys())
    ['RP', 'RPRP', 'LP', 'P', 'PR', 'LRP', 'id_.', 'PLP', 'PRP', 'LPR', 'RLR', 'PRLR', 'LR', 'RPLPR', 'RL', 'RLRP', 'PL', 'RPR', 'LRL', 'LPRP', 'R', 'L', 'PLPR', 'RLP']

What operation do we get in the PRL group if we apply first LRL, then P ?

    >>> print my_group.mult("P","LRL")
    LPRP    
