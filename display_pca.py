import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

#NEEDS THE OUTPUT FILE OF THE MAIN.PY SCRIPT

#name of the file to open
filename = "result off k=40 N=50000 nb_cases=20 m=5.txt"
result_file = open(filename,"r")

line = result_file.readline() #jump useless lines
line = result_file.readline()

L=[] # temp var
E=[] # eigenvalues
G=[] # histograms
N=[] # names of shapes

#read result_file
step = 'name'
while line :
    if(step=='name'):
        l=[line[line.find("/")+1:line.find(".")]]
        N.append(line[line.find("/")+1:line.find(".")])
        step='eigen'
        eigen=''
        line=result_file.readline()
        
    elif(step=='eigen'):
        if(line.find(']')!=-1):
            step='hist'
            eigen+=line[:-1]
            
            l.append(eval(eigen))
            E.append(eval(eigen))
            #l.append(np.fromstring(eigen, sep=','))
            hist=''
            line=result_file.readline()
            line=result_file.readline()

        else:
            eigen+=line[:-1]
            
    elif(step=='hist'):
        if(line.find(']')!=-1):
            step='name'
            hist+=line[:-1]
            l.append(eval(hist))
            #l.append(np.fromstring(hist, sep=','))
            L.append(l)
            G.append(eval(hist))
            line=result_file.readline()
            line=result_file.readline()
        else:
            hist+=line[:-1]
    line = result_file.readline()

# 1 for .obj, 2 for .off
dataset_type = 1
if ('off' in filename):
    dataset_type = 2
nb_per_col = 4 if dataset_type == 1 else 20 #nb of images of the same object for each object, depends on the dataset
n_components_pca = 7 #if dataset_type == 1 else 10 #nb of differents objects


#Plot DNA PCA
plt.figure()
X=E
pca = PCA(n_components=n_components_pca)
X_r = pca.fit(X).transform(X)
print(X_r)
for i in range(0,len(X_r),nb_per_col):
    plt.scatter(X_r[i:i+nb_per_col, 0], X_r[i:i+nb_per_col, 1])

plt.title('DNA')
for i, txt in enumerate(N):
    plt.annotate(txt, (X_r[i, 0],X_r[i, 1]))


#Plot GPS PCA
plt.figure()        
X=G
pca = PCA(n_components=n_components_pca)
X_r = pca.fit(X).transform(X)
print(X_r)
for i in range(0,len(X_r),nb_per_col):
    plt.scatter(X_r[i:i+nb_per_col, 0], X_r[i:i+nb_per_col, 1])
    
plt.title('GPS')
for i, txt in enumerate(N):
    plt.annotate(txt, (X_r[i, 0],X_r[i, 1]))
plt.show()