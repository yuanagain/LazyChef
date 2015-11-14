import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import breadth_first_order

'''
dense_graph = np.array([[0, 1, 1],
				 		[1, 0, 0],
				 		[1, 0, 0]])
'''
#Connectivity matrix dimension
n = (11,11)
dense_graph = np.zeros(n)
dense_graph[0][1] = 1
dense_graph[0][2] = 1
dense_graph[0][3] = 1
dense_graph[1][4] = 1
dense_graph[1][5] = 1
dense_graph[1][6] = 1
dense_graph[2][7] = 1
dense_graph[3][8] = 1
dense_graph[6][9] = 1
dense_graph[6][10] = 1

sparse_graph = csr_matrix(dense_graph)
BForder = breadth_first_order(sparse_graph,0,return_predecessors=False)
for i in BForder:
	print(i)