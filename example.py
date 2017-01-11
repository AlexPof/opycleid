################################################
###### Copyright (c) 2016, Alexandre Popoff 
###

from opycleid.musicmonoids import PRL_Group
from opycleid.knetanalysis import KNet

my_group = PRL_Group()

#Create a path K-Net for the famous Beethoven example
my_knet = KNet(my_group)
my_knet.add_vertices(["C","a","F","d","Bb","g","Eb","c","Gs","f","Cs","bb"])
my_knet.path_knet_from_vertices()
my_knet.print_knet()
