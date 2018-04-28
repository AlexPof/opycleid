################################################
###### Copyright (c) 2016, Alexandre Popoff
###

from opycleid.musicmonoids import PRL_Group
from opycleid.knetanalysis import KNet

my_group = PRL_Group()

#Create a path K-Net for the famous Beethoven example
my_knet = KNet(my_group)
my_knet.set_vertices(["C_M","A_m","F_M","D_m","Bb_M","G_m","Eb_M","C_m","Gs_M","F_m","Cs_M","Bb_m"])
my_knet.path_knet_from_vertices()
print str(my_knet)
