# -*- coding: utf-8 -*-

################################################
###### Copyright (c) 2016, Alexandre Popoff 
###

import numpy as np

################################################
###### GENERIC CLASS FOR MONOID ACTION
###

class KNet:
	def __init__(self,category):
		if not "MonoidAction" in str(category.__class__.__bases__):
			raise Exception("Not a valid category action\n")
		else:
			self.vertices = {}
			self.edges = {}
			self.category = category

	def add_vertices(self,list_vertices):
		for x in list_vertices:
			if x in self.category.objects.keys():
				self.vertices[len(self.vertices)] = x
			else:
				raise Exception("Element "+str(x)+" is not in the category action\n")

	def add_edges(self,list_edges):
		for id_vertex_A,id_vertex_B,operation in list_edges:
			if not operation in self.category.operations.keys():
				raise Exception(str(operation)+" is not a valid operation in the category\n")
				
			if operation in self.category.get_operation(self.vertices[id_vertex_A],self.vertices[id_vertex_B]):
				self.edges[len(self.edges)] = (id_vertex_A,id_vertex_B,operation)
			else:
				raise Exception(str(operation)+" is not a valid operation for the corresponding vertices\n")
			
	def pathKNet_from_vertices(self):
		if not self.category.SIMPLY_TRANSITIVE:
			raise Exception("The category does not act in a simple transitive way: ambiguous determination of operations")
		else:
			for i in range(len(self.vertices)-1):
				self.add_edges([(i,i+1,self.category.get_operation(self.vertices[i],self.vertices[i+1])[0])])

	def completeKNet_from_vertices(self):
		if not self.category.SIMPLY_TRANSITIVE:
			raise Exception("The category does not act in a simple transitive way: ambiguous determination of operations")
		else:
			for i in range(len(self.vertices)):
				for j in range(i+1,len(self.vertices)):
					self.add_edges([(i,j,self.category.get_operation(self.vertices[i],self.vertices[j])[0])])


	def print_KNet(self):
		for x in self.edges.keys():
			self.print_KNet_edge(x)

	def print_KNet_edge(self,x):
		name_A = self.vertices[self.edges[x][0]]
		name_B = self.vertices[self.edges[x][1]]
		name_op = self.edges[x][2]
		print " "*len(name_A)+name_op+" "*len(name_B)
		print self.vertices[self.edges[x][0]]+"-"*len(name_op)+">"+self.vertices[self.edges[x][1]]
		print ""

			
	def is_valid(self):
	
		## Get the adjacency matrix
		n_obj = len(self.vertices)
		adj_matrix = np.zeros((n_obj,n_obj))
		for x in self.edges.keys():
			adj_matrix[self.edges[x][1],self.edges[x][0]] = True
		
		## Get all top elements
		top_elements = np.where(np.sum(adj_matrix,axis=1)==0)[0]
		
		## Perform propagation of operations along vertices starting from a top element
		for top_idx in top_elements:
			list_prop=[(top_idx,"e",0)]
			flag=1
			while(flag):
				flag=0
				for i,(idx,op,visited) in enumerate(list_prop):
					if not visited:
						# Get all the possible edges out of this vertex, and multiply on the left by the category element
						for edge in self.edges.keys():
							if self.edges[edge][0]==idx:
								list_prop.append((self.edges[edge][1],self.category.mult(self.edges[edge][2],op),0))
								flag=1
						# We have exhausted all the possible paths out of this vertex, so we mark it as visited 
						list_prop[i] = (idx,op,1)
			
			## Check the validity of the paths: the same vertex should have the same category operation
			for idx_1,op_1,v1 in list_prop:
				for idx_2,op_2,v2 in list_prop:
					if idx_1==idx_2 and not(op_1==op_2):
						return False
		
		return True
					
			



