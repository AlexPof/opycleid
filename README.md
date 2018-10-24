![PyPi](https://badge.fury.io/py/opycleid.svg)


# opycleid

Opycleid is a Python package for transformational music theory (TMT), a field of
musicology which studies transformations between musical objects
(notes, chords, durations, etc.) from a mathematical point of view.

The website and complete documentation is [available here](https://alexpof.github.io/opycleid/).

## Installation

### Dependencies

Opycleid requires:

- Python (>= 3.4)
- NumPy (>= 1.8.2)

### User installation

The easiest way to install opycleid is using ``pip``:

    $ pip install opycleid

## Development

We welcome new contributors of all experience levels. The preferred way to
contribute to opycleid is to fork the main repository on GitHub,
then submit a “pull request” (PR). Bug reports and discussion on new features
(only) can be posted in the [corresponding GitHub issues](https://github.com/AlexPof/opycleid/issues).
Preferably, the development of new features should be discussed beforehand
on this page.

### Source code

You can check the latest sources with the command:

    >>> git clone https://github.com/AlexPof/opycleid.git

## Testing / Tutorial

The following serves as a quick tutorial and as tests of the basic functionalities
of opycleid.

After installation, transformational music analysis is easily implemented in a
few lines, with the group/monoid of your choice. Opycleid includes the basic
groups encountered in TMT, such as the T/I group acting on pitch classes,
or the T/I and the neo-Riemannian group PRL acting on triads.

    >>> from opycleid.musicmonoids import PRL_Group,TI_Group_Triads,TI_Group_PC

Assume we want to work first with pitch classes. What operations in the T/I group
takes C to A ?

    >>> my_group = TI_Group_PC()
    >>> my_group.get_operation("C","A")
    ['I9', 'T9']

Assume we now work with major and minor triads.
What operations in the T/I group takes C major to B minor ?

    >>> my_group = TI_Group_Triads()
    >>> my_group.get_operation("C_M","B_m")
    ['I6']

What operation do we get in the T/I group if we apply first I6, then T9 ?

    >>> print(my_group.mult("T9","I6"))
    I3   

If we now consider the PRL group instead, what transformation takes B minor to G major ?

    >>> my_group = PRL_Group()
    >>> my_group.get_operation("B_m","G_M")
    ['L']

What chord do we get if we apply that same operation to a D major chord (Answer: F sharp minor) ?

    >>> my_group.apply_operation("L","D_M")
    ['Fs_m']

In its ninth symphony, Beethoven uses a succession of R and L operations to cycle
through almost all 24 major and minor triads. We can model this cycle using opycleid.

    >>> from opycleid.musicmonoids import PRL_Group
    >>> from opycleid.knetanalysis import KNet
    >>> my_group = PRL_Group()
    >>> #Create a path K-Net for the famous Beethoven example
    >>> my_knet = KNet(my_group)
    >>> my_knet.set_vertices(["C_M","A_m","F_M","D_m","Bb_M","G_m","Eb_M","C_m","Gs_M","F_m","Cs_M","Bb_m"])
    >>> my_knet.path_knet_from_vertices()
    >>> print(my_knet)
    K-Net description:
       R   
    C_M->A_m
       L   
    A_m->F_M
       R   
    F_M->D_m
       L    
    D_m->Bb_M
        R   
    Bb_M->G_m
       L    
    G_m->Eb_M
        R   
    Eb_M->C_m
       L    
    C_m->Gs_M
        R   
    Gs_M->F_m
       L    
    F_m->Cs_M
        R    
    Cs_M->Bb_m

## Help and Support

### Documentation

- [HTML documentation (stable release)](https://alexpof.github.io/opycleid/)
- [Complete tutorial](https://alexpof.github.io/opycleid/gettingstarted/)

### Communication

Please use the [GitHub issues page](https://github.com/AlexPof/opycleid/issues).
