---
title: 'Opycleid: A Python package for transformational music theory'
tags:
  - Python
  - music-theory
  - category-theory
  - chords
authors:
  - name: Alexandre Popoff
    orcid: 0000-0002-3767-0361
    affiliation: 1
affiliations:
  - name: Independent Researcher
    index: 1
date: 16 September 2018
bibliography: paper.bib
---

# Summary

Transformational music theory (TMT) is a branch of mathematical music theory
which usesmodern mathematical structures (such as groups, monoids and
categories) to study and characterize musical objects (such as tones, chords,
durations, rhythms) and their relations. More precisely, transformational music
theory has progressively shifted the music-theoretical and analytical process
from an “object-oriented” point of view to one where the transformations between
musical elements are emphasized. The field originated in the work of David Lewin
[@Lewin:1987] [@Lewin:1982] who pioneered the use of groups and group actions
[@Fiore:2011], and has later been extended to monoids [@Noll:2005], and category
theory [@Mazzola:2006] [@Popoff:2015] [@Popoff:2016]. It has proved useful in
analysis, from late romantic music [@Gollin:2010] [@Cohn:2012] to recent film
music [@Lehman:2018]. The algebraic and combinatorial nature of musical
transformation make them prone to easy computer implementations. However,
general frameworks for creating and applying musical transformations
(for example using category theory) are scarce if not non-existent, and are
instead focused on specific and restrained areas (for example, neo-Riemannian
operations).

# Statement of need

``Opycleid`` is a Python package for transformational music theory, allowing the
definition and application of musical transformations in the broadest way possible.
The API for ``Opycleid`` was designed in order to take a very general approach
to TMT by considering category actions in **Rel**, i.e. faithful functors
from a small category to the 2-category **Rel** of finite sets and
relations between them. At the same time, ``Opycleid`` provides ready-to-use
classes for the common groups and monoids encountered in TMT
(such as the *T/I* group or the *PRL* group usually found in neo-Riemannian theory),
allowing the analysis of chords with just a few Python lines of code.

``Opycleid`` was designed to be used by both researchers and by students in
music theory (see for example
<https://www.mathsstudents.leeds.ac.uk/fileadmin/user_upload/Current_Maths_UG_Students/2017_Dr_R_Sturman.pdf>).
The source code for ``Opycleid`` has been archived to Zenodo with the linked DOI:
(TO BE COMPLETED)

# References
