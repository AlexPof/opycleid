![PyPi](https://badge.fury.io/py/opycleid.svg)

# opycleid
Opycleid - A Python package for transformational music theory

Please visit http://alpof.wordpress.com/2016/06/20/opycleid-a-python-package-for-transformational-music-theory/
for detailed instructions.

How to use opycleid
==========

Transformational music analysis is easily implemented in a few lines, with the group/monoid of your choice:

    >>> from opycleid.musicmonoids import PRL_Group,TI_Group_Triads,TI_Group_PC

Let's work first with pitch classes... what operations in the T/I group takes C to A ?

    >>> my_group = TI_Group_PC()
    >>> print my_group.get_operation("C","A")
    ['I^9', 'T^9']

Let's now work with major and minor triads... what operations in the T/I group takes C major to B minor ?

    >>> my_group = TI_Group_Triads()
    >>> print my_group.get_operation("C_M","B_m")
    ['I^6']

What would it be if we use the PRL group instead ?

    >>> my_group = PRL_Group()
    >>> print my_group.get_operation("C_M","B_m")
    ['(RL)^10R']

What do we get if we apply that same operation to a D major chord (Answer: C sharp minor) ?

    >>> print my_group.apply_operation("(RL)^10R","D_M")
    ['Cs_m']

What are the operations in the PRL group ?

    >>> print my_group.operations.keys()
    ['(RL)^5R', '(RL)^7R', '(RL)^9', '(RL)^8', '(RL)^7', '(RL)^6', '(RL)^5', '(RL)^4', '(RL)^3', '(RL)^2', '(RL)^1', '(RL)^3R', '(RL)^8R', '(RL)^1R', '(RL)^10R', '(RL)^4R', '(RL)^2R', '(RL)^6R', 'R', 'e', '(RL)^9R', '(RL)^11R', '(RL)^11', '(RL)^10']

What operation do we get in the PRL group if we apply first (RL)^10R, then (RL)^5 ?

    >>> print my_group.mult("(RL)^5","(RL)^10R")
    (RL)^3R    
