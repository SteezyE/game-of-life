import numpy as np

A = np.random.randint(2,size=(50,50),dtype=int)
np.savetxt('example3.txt',A.astype(int),fmt='%i',delimiter=',')
