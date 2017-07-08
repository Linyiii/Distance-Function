import numpy as np

size_of_matrix= 8
num_of_matrices= 4

def random_matrix_file(size,num):
    for i in range(0,num):
        matrix=np.matrix(np.random.randint(0,2,size=(size,size)))
        name='randominput'+str(i)+'.txt'
        f=open(name,'w')
        for row in range(0,size):
            for col in range(0,size):
                if col!=size-1:
                    f.write(str(matrix[row,col])+' ')
                else:
                    f.write(str(matrix[row,col])+'\n')
        f.close()
            
        
        
random_matrix_file(size_of_matrix,num_of_matrices)
