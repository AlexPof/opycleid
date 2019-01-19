![PyPi](https://badge.fury.io/py/opycleid.svg)
[![DOI](http://joss.theoj.org/papers/10.21105/joss.00981/status.svg)](https://doi.org/10.21105/joss.00981)


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

The easiest way to install Opycleid is using ``pip``:

    $ pip install opycleid

Opycleid can also be installed directly from source:

    $ python setup.py install    

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
    >>> from opycleid.knetanalysis import PKNet
    >>> my_group = PRL_Group()
    >>> my_knet = PKNet(my_group)
    >>> beethoven_chords = ["C_M","A_m","F_M","D_m","Bb_M","G_m","Eb_M","C_m","Gs_M","F_m","Cs_M","Bb_m"]
    >>> for pknet in my_knet.from_progression(beethoven_chords):
    >>>     print(pknet)
    X_0 -- R --> X_1
    [['C_M']] -> [['A_m']]
    X_1 -- L --> X_2
    [['A_m']] -> [['F_M']]
    X_10 -- R --> X_11
    [['Cs_M']] -> [['Bb_m']]
    X_2 -- R --> X_3
    [['F_M']] -> [['D_m']]
    X_3 -- L --> X_4
    [['D_m']] -> [['Bb_M']]
    X_4 -- R --> X_5
    [['Bb_M']] -> [['G_m']]
    X_5 -- L --> X_6
    [['G_m']] -> [['Eb_M']]
    X_6 -- R --> X_7
    [['Eb_M']] -> [['C_m']]
    X_7 -- L --> X_8
    [['C_m']] -> [['Gs_M']]
    X_8 -- R --> X_9
    [['Gs_M']] -> [['F_m']]
    X_9 -- L --> X_10
    [['F_m']] -> [['Cs_M']]


## Help and Support

### Documentation

- [HTML documentation (stable release)](https://alexpof.github.io/opycleid/)
- [Complete tutorial](https://alexpof.github.io/opycleid/gettingstarted/)

### Communication

Please use the [GitHub issues page](https://github.com/AlexPof/opycleid/issues).
