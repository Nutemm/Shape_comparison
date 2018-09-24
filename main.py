from math import sqrt
import numpy as np
from numpy import *
from scipy.linalg import inv
from numpy import linalg as LA
from Point import *
from Shape import *
from scipy.sparse import csc_matrix
import scipy.sparse.linalg as slingalg
from Face import *
import time
from sklearn.cluster import KMeans

#File used to read the .off or .obj, some parameters, and create new txt result files with the fingerprints
#These fingerprints can then be displayed with display_pca.py, or compared with the ones of other result files in final_score_per_files.py


def kmeans_D2():
    ''' Was used to do kmeans on GPS-D2 '''
    l_d2 = []

    
    list_files = ["camel-collapse/camel-collapse-01.obj", "camel-gallop/camel-gallop-01.obj", "cat-poses/cat-01.obj", "elephant-gallop/elephant-gallop-01.obj", "elephant-poses/elephant-01.obj", "face-poses/face-01-anger.obj", "head-poses/head-01-anger.obj", "horse-collapse/horse-collapose-01.obj", "horse-gallop/horse-gallop-01.obj", "horse-poses/horse-01.obj", "lion-poses/lion-01.obj"   ]
    list_shapes = []

    for name in list_files:
        t = time.time()
        list_shapes.append(Shape(name))
        list_shapes[-1].compute_D2(k=20, N = 50000, nb_cases = 3, m = 5)
        l_d2.append(list_shapes[-1].histogram)
        list_shapes[-1].clear()
        print("Computed D2-distrib for ", name, "in ", time.time() - t)

    print("Training k-means")
    kmeans = KMeans(init='k-means++', n_clusters=2, n_init=100)
    kmeans.fit(l_d2)
    print("Trained.")

    for i in range(len(list_files)):
        print("File ", list_files[i], "is associated to cluster ", kmeans.predict(l_d2[i].reshape(1, -1)))


def kmeans_Shape_DNA():
    ''' Was used to do kmeans on Shape DNA '''
    l_eig = []

    list_files = [  "camel-poses/camel-01.obj", "camel-poses/camel-02.obj", "camel-poses/camel-03.obj",
                    #"flamingo-poses/flam-04.obj", "flamingo-poses/flam-02.obj", "flamingo-poses/flam-03.obj", #buggy
                    "lion-poses/lion-01.obj","lion-poses/lion-02.obj","lion-poses/lion-03.obj",
                  ]
    list_shapes = []

    for name in list_files:
        t = time.time()
        list_shapes.append(Shape(name))
        list_shapes[-1].compute_shape_dna(10)
        l_eig.append(list_shapes[-1].eigenvalues)
        list_shapes[-1].clear()
        #print(l_eig[-1])
        print("Computed shape DNA for ", name, "in ", time.time()-t)

    print("Training k-means")
    kmeans = KMeans(init='k-means++', n_clusters=2, n_init=100)
    kmeans.fit(l_eig)
    print("Trained.")

    for i in range(len(list_files)):
        print("File ", list_files[i], "is associated to cluster ", kmeans.predict(l_eig[i].reshape(1, -1)))





if __name__ == '__main__':

    # to analyse obj files
    # type_file = 'obj'
    # list_files = ["camel-collapse/camel-collapse-01.obj","camel-collapse/camel-collapse-02.obj","camel-collapse/camel-collapse-03.obj","camel-collapse/camel-collapse-04.obj",
    #               "camel-gallop/camel-gallop-01.obj","camel-gallop/camel-gallop-02.obj","camel-gallop/camel-gallop-03.obj","camel-gallop/camel-gallop-04.obj",
    #               "cat-poses/cat-01.obj","cat-poses/cat-02.obj","cat-poses/cat-03.obj","cat-poses/cat-04.obj",
    #               "elephant-gallop/elephant-gallop-01.obj","elephant-gallop/elephant-gallop-02.obj","elephant-gallop/elephant-gallop-03.obj","elephant-gallop/elephant-gallop-04.obj",
    #               "elephant-poses/elephant-01.obj","elephant-poses/elephant-02.obj","elephant-poses/elephant-03.obj","elephant-poses/elephant-04.obj",
    #               "face-poses/face-01-anger.obj","face-poses/face-02-cry.obj","face-poses/face-03-fury.obj","face-poses/face-04-grin.obj",
    #               "head-poses/head-01-anger.obj","head-poses/head-02-cry.obj","head-poses/head-03-fury.obj","head-poses/head-04-grin.obj",
    #               "horse-collapse/horse-collapose-01.obj","horse-collapse/horse-collapose-02.obj","horse-collapse/horse-collapose-03.obj","horse-collapse/horse-collapose-04.obj",
    #               "horse-gallop/horse-gallop-01.obj","horse-gallop/horse-gallop-02.obj","horse-gallop/horse-gallop-03.obj","horse-gallop/horse-gallop-04.obj",
    #               "horse-poses/horse-01.obj","horse-poses/horse-02.obj","horse-poses/horse-03.obj","horse-poses/horse-04.obj",
    #               "lion-poses/lion-01.obj","lion-poses/lion-02.obj","lion-poses/lion-03.obj","lion-poses/lion-04.obj"]

    #to analyse off files
    type_file = 'off'
    list_files = []
    for i in range(1,101): #you can change the range to compute more or less files. However, the number of analysed files has to be divisible by 20  
        list_files.append("off/"+str(i)+".off")


    list_shapes = [] #contains the Shape objects of all the analysed files
    l_eig = [] #contains the eigenvalues corresponding to each shape
    l_d2 = [] #contains the D2 histogram corresponding to each shape (= GPS method)

    np.set_printoptions(threshold=np.nan)

    #Choose the parameters
    k=40
    N=50000
    nb_cases=20
    m=5

    with open("result "+type_file+" k="+str(k)+" N="+str(N)+" nb_cases="+str(nb_cases)+" m="+str(m)+".txt","w") as output_file:

        output_file.write("k="+str(k)+" N="+str(N)+" nb_cases="+str(nb_cases)+" m="+str(m)+"\n")

        for name in list_files:

            t = time.time()
            list_shapes.append(Shape(name))

            list_shapes[-1].compute_D2(k, N, nb_cases, m) #this method also computes the shape_dna

            l_eig.append(list_shapes[-1].eigenvalues)
            l_d2.append(list_shapes[-1].histogram)


            print("Computed  ", name, "in ", time.time()-t)
            output_file.write(name+"\n")
            output_file.write("eigenvalues begin  \n")
            output_file.write(np.array2string(list_shapes[-1].eigenvalues, precision=8, separator=',') + "\n")
            output_file.write("eigenvalues end  \n")

            output_file.write("histogram begins  \n")
            output_file.write(np.array2string(list_shapes[-1].histogram, precision=8, separator=',') + "\n")
            output_file.write("histogram ends  \n\n")

            list_shapes[-1].clear() #for RAM saving purposes






