# opycleid
Opycleid - A Python package for transformational music theory

Please visit http://alpof.wordpress.com/2016/06/20/opycleid-a-python-package-for-transformational-music-theory/
for detailed instructions.

How to use
==========

Transformational music analysis is easily implemented in a few lines, with the group/monoid of your choice:

    >>> from opycleid.monoids import PRL_Group,TI_Group_Triads,TI_Group_PC
    >>> ## Let's work first with pitch-classes... what operations in the T/I group takes C to A ?
    >>> my_group = TI_Group_PC()
    >>> print my_group.get_operation("C","A")
    ['I^9', 'T^9']
    >>> ## Let's now work first with major and minor triads... what operations in the T/I group takes C major to B minor ?
    >>> my_group = TI_Group_Triads()
    >>> print my_group.get_operation("C","b")
    ['I^6']
    >>> ## What would it be if we use the PRL group instead ?
    >>> my_group = PRL_Group()
    >>> print my_group.get_operation("C","b")
    ['(RL)^10R']
    >>> ## What do we get if we apply that same operation to a D major chord (Answer: C sharp minor) ?
    >>> print my_group.apply_operation("(RL)^10R","D")
    ['cs']
