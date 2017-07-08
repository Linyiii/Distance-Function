import numpy as np
import random
import glob
import time

#path to the sample file
path='/Users/apple/Desktop/DistanceFunction/samples/*.txt'
#number of iterations of the distance function
num_of_iter=1000

def check_contra(matrix,row,col):
    '''helper function to decide whether contradiction exits in previous column on the same row'''
    no_contra=True
    for check_col in range(0,col):
        if matrix[row,check_col]==0:
            no_contra=True and no_contra
        else:
            no_contra=False
            break
    return no_contra


def find_col_with_more_one(matrix,col,num_of_row):
    '''helper function to return a list of previous columns that have more than one 1's'''
    col_list=[]
    for col in range(0,col):
        counter=0
        for row in range(0,num_of_row):
            if matrix[row,col]==1:
                counter=counter+1
            if counter==2:
                col_list.append(col)
                break
    return col_list

def find_row_to_change(matrix,col,num_of_row):
    '''helper function to return a list of availabel rows in the given col to swap with'''
    row_list=[]
    for row in range(0,num_of_row):
        if matrix[row,col]==1:
            row_list.append(row)
    assert len(row_list)>=2
    return row_list

def do_partition(m,n):
    """
    Input two integers m and n, assume m<n
    Provides a random partition function f:N->M in the form of a n*m matrix"""

    partition=np.zeros((n,m))
    for row in range(0,n):
        col=random.randint(0,m-1)
        partition[row,col]=1

    for col in range(0,m):
        findone=False
        for row in range(0,n):#check whether each column has one 1, ok to have more than one 1 in each column
            if partition[row,col]==1:
                findone=True
                break
            else:
                assert findone==False
                if row==n-1 and col>0:#if last row still have no 1
                    no_contra_row_list=[]
                    for checkrow in range(0,n):
                        if check_contra(partition,checkrow,col):
                            no_contra_row_list.append(checkrow)
                    if no_contra_row_list != []:#if there are rows without contra
                        rowchange2=no_contra_row_list[random.randint(0,len(no_contra_row_list)-1)]#select random row
                        for colchange2 in range(0,m):
                            if colchange2==col:
                                partition[rowchange2,colchange2]=1
                            else:
                                partition[rowchange2,colchange2]=0
                    else:#all rows have contra
                        col_list_to_select=find_col_with_more_one(partition,col,n)
                        colchange2=col_list_to_select[random.randint(0,len(col_list_to_select)-1)]#select random col that has more than one 1
                        row_list_to_select=find_row_to_change(partition,colchange2,n)
                        rowchange2=row_list_to_select[random.randint(0,len(row_list_to_select)-1)]#select random row that is 1
                        partition[rowchange2,colchange2]=0
                        partition[rowchange2,col]=1
                elif row==n-1 and col==0:
                    rowchange3=random.randint(0,n-1)
                    partition[rowchange3,col]=1
                    for colchange3 in range(1,m):
                        partition[rowchange3,colchange3]=0
    return partition

def list_of_z(i,partition,num_of_row):
    '''helper function that gives list of row indices which map to i by the partition funciton'''
    list_z=[]
    for row in range(0,num_of_row):
        if partition[row,i]==1:
            list_z.append(row)
    assert len(list_z)>0
    return list_z

def random_list(x):
    '''create a list of length x with random integers in range(0,10)'''
    result=[]
    counter=0
    for i in range (x):
        a=random.randint(1,9)
        result.append(a)
    return result

def composite_graph(G1,G2,partition):
    '''G1 n*n, G2 m*m, partition n*m, m<=n, return composite graph as a m*n weight matrix'''
    m=len(G2)
    n=len(G1)
    G3=np.zeros((m,n))
    for j in range(m):
        for k in range(m):
            y=G2[j,k]
            list_z=list_of_z(k,partition,n)
            list_of_val=random_list(len(list_z))
            sum_val=sum(list_of_val)
            for i in range(0,len(list_z)):
                G3[j][list_z[i]]= (list_of_val[i]/sum_val)*y
    return G3
               
def two_norm(matrix1,x,matrix2,y,n):
    '''helper function to compute 2-norm of xth and yth row of matrix 1 and matrix 2'''
    result=0
    for i in range (n):
        result=result+(matrix1[x,i]-matrix2[y,i])**(2)
    return result**(0.5)

def find_row(partition_func, i):
    '''helper function to find phi(i), phi represented by the partition function'''
    for col in range(0,partition_func.shape[1]):
        if partition_func[i,col]==1:
            return col

def distance_equal(G1,G2,partition_func):
    partition_copy=partition_func
    z=np.dot(G2,partition_func.transpose())
    n=len(partition_func)
    result=0
    for i in range(n):
        row2=find_row(partition_func,i)
        result=result+two_norm(G1,i,z,row2,n)
    return result/n
    
 
def distance_once(G1,G3,partition_func):
    '''Given two graphs G1 an G2 represented as weight matrix, return a real value distance. Use 2-norm in this case'''
    n=len(partition_func)
    result=0
    for i in range(n):
        row2=find_row(partition_func,i)
        result=result+two_norm(G1,i,G3,row2,n)
    return result/n

def distance(matrix1,matrix2):
    result=float("inf")
    if len(matrix1)==len(matrix2):#two graphs of the same size
        size=len(matrix1)
        for i in range(num_of_iter):
            partition_func=do_partition(size,size)
            result=min(result,distance_equal(matrix1,matrix2,partition_func))
        return result
    else:
        if len(matrix1)> len(matrix2):
            G1=matrix1
            G2=matrix2
            n=len(matrix1)
            m=len(matrix2)
        else:
            G1=matrix2
            G2=matrix1
            n=len(matrix2)
            m=len(matrix1)
        for i in range(num_of_iter):
            partition_func=do_partition(m,n)
            G3=composite_graph(G1,G2,partition_func)
            result=min(result,distance_once(G1,G3,partition_func))
        return result

starttime=time.time()
f_names= glob.glob(path)
graph_list=[]

#assume sample files are in right order
for f in f_names:
    graph_list.append(np.loadtxt(f))

output=open('result.txt','a')
output.write('\n')
for i in range(0,len(graph_list),2):
    size1=len(graph_list[i])
    size2=len(graph_list[i+1])
    result=distance(graph_list[i],graph_list[i+1])
    output.write(str((i/2)+1)+'. '+str(result)+'\n'+'matrices sizes are: '+str(size1)+', '+str(size2)+'\n')
    
elapsedtime=time.time()-starttime
output.write('\n'+'Running time is:'+str(elapsedtime)+'\n')
output.write('Number of iterations is: '+str(num_of_iter)+'\n'+'\n')

output.close()
    


