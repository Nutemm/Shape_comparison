import numpy as np
import time
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from scipy.spatial.distance import euclidean

#Use the txt files generated by main.py to get fingerprints for different methods. Analyse them by computing a score.
#Compare the txt files. The one with the lowest score corresponds to the best parameters.

def compute_distance_inter_groups(names_f, positions):
    ''' Score explained in the .pdf '''

    dists = []

    if dataset_type == 2:
        for pos in range(0,200,20): #each object has 20 images, and we have the fingerprints of 10 objects
            group_dist = 0
            for i in range(19):
                for j in range(i+1,20):
                    group_dist += euclidean(np.array(positions[pos+i]), np.array(positions[pos+j]))
            dists.append(group_dist)

    elif dataset_type == 1:
        pos = 0
        while pos < len(names_f):
            offset = 0
            indices_same_animal = [] #find indices of the same animal
            while pos+offset < len(names_f) and names_f[pos].split("-")[0] == names_f[offset+pos].split("-")[0]:
                indices_same_animal.append(offset+pos)
                offset += 1

            #computes dist inter group
            group_dist = 0
            for i in range(len(indices_same_animal)-1):
                for j in range(i+1,len(indices_same_animal)):
                    group_dist += euclidean(np.array(positions[indices_same_animal[i]]), np.array(positions[indices_same_animal[j]]))

            dists.append(group_dist)

            pos = pos+offset #analyse another animal

    #Compute total distances between each pair of points
    dist_sum = 0
    for i in range(len(positions)):
        for j in range(i+1, len(positions)):
            dist_sum += euclidean(np.array(positions[i]), np.array(positions[j]))



    #All those dists need to be divided by distance-extra-cluster
    return np.array(dists)/dist_sum


if __name__ == '__main__':


    dataset_type = 2 #1 for first dataset, 2 for the other

    list_files = []
    if dataset_type == 1:
        list_files = ["result obj k=40 N=50000 nb_cases=5 m=1.txt",
                    "result obj k=40 N=50000 nb_cases=10 m=1.txt","result obj k=40 N=50000 nb_cases=20 m=1.txt",
                    "result obj k=40 N=50000 nb_cases=50 m=1.txt",
                    "result-k40-N50000-nb_cases5-m5.txt","result-k40-N50000-nb_cases10-m5.txt",
                    "result obj k=40 N=50000 nb_cases=20 m=5.txt",
                    "result obj k=40 N=50000 nb_cases=50 m=5.txt",
                    "result obj k=40 N=50000 nb_cases=5 m=10.txt", "result-k40-N50000-nb_cases10-m10.txt",
                    "result-k40-N100000-nb_cases20-m20.txt",
                    ]
    else:
        list_files = ["result off k=40 N=50000 nb_cases=10 m=1.txt", "result off k=40 N=50000 nb_cases=20 m=1.txt",
                    "result off k=40 N=50000 nb_cases=50 m=1.txt",
                    "result off k=40 N=50000 nb_cases=10 m=5.txt",
                    #"result off k=40 N=50000 nb_cases=20 m=5.txt",
                    "result-off-k40-N50000-nb_cases5-m10.txt", "result off k=40 N=50000 nb_cases=20 m=10.txt"]

    eigenvalues_f = []
    histograms_f = []
    names_f = []

    #read the files
    for i, file in enumerate(list_files):

        obj = open(file, "r")

        line = obj.readline()
        line = obj.readline()

        L = []  # temp var
        E = []  # eigenvalues
        G = []  # histograms
        N = []  # names of shapes

        step = 'name'
        while line:

            if (step == 'name'):
                l = [line[line.find("/") + 1:line.find(".")]]
                N.append(line[line.find("/") + 1:line.find(".")])
                step = 'eigen'
                eigen = ''
                line = obj.readline()

            elif (step == 'eigen'):
                if (line.find(']') != -1):
                    step = 'hist'
                    eigen += line[:-1]

                    l.append(eval(eigen))
                    E.append(eval(eigen))
                    # l.append(np.fromstring(eigen, sep=','))
                    hist = ''
                    line = obj.readline()
                    line = obj.readline()

                else:
                    eigen += line[:-1]

            elif (step == 'hist'):
                if (line.find(']') != -1):
                    step = 'name'
                    hist += line[:-1]
                    l.append(eval(hist))
                    # l.append(np.fromstring(hist, sep=','))
                    L.append(l)
                    G.append(eval(hist))
                    line = obj.readline()
                    line = obj.readline()
                else:
                    hist += line[:-1]
            line = obj.readline()


        eigenvalues_f = E #because they are always the same
        names_f = N #because they are always the same
        histograms_f.append(G)

    
    #Computes the eigen_values, D2 histograms and the dists
    eigenvalues_f1 = [eigenvalues_f[i][:1] for i in range(len(eigenvalues_f))]
    eigenvalues_f5 = [eigenvalues_f[i][:5] for i in range(len(eigenvalues_f))]
    eigenvalues_f10 = [eigenvalues_f[i][:10] for i in range(len(eigenvalues_f))]
    eigenvalues_f20 = [eigenvalues_f[i][:20] for i in range(len(eigenvalues_f))]

    dists_groups_parameter = [compute_distance_inter_groups(names_f, eigenvalues_f1)] #for eigen_values with k = 1
    dists_groups_parameter.append(compute_distance_inter_groups(names_f, eigenvalues_f5)) #for eigen_values with k = 5
    dists_groups_parameter.append(compute_distance_inter_groups(names_f, eigenvalues_f10)) #for eigen_values with k = 10
    dists_groups_parameter.append(compute_distance_inter_groups(names_f, eigenvalues_f20)) #for eigen_values with k = 20
    dists_groups_parameter.append(compute_distance_inter_groups(names_f, eigenvalues_f)) #for eigen_values with k = 40


    for h in histograms_f:
        dists_groups_parameter.append(compute_distance_inter_groups(names_f, h)) #for GPS

    dists_groups_parameter = np.array(dists_groups_parameter)
    # scale column by column (each column = a group of images) -> this way each group has same importance
    dists_groups_parameter /= np.sum(dists_groups_parameter, axis=0)
    #sum distances for all groups
    ar_dists_groups_parameter = dists_groups_parameter
    dists_groups_parameter = np.sum(dists_groups_parameter, axis=1)

    print("For dataset", dataset_type, ":\n")
    print("Score with Shape-DNA and k = 1 :", dists_groups_parameter[0])
    print(ar_dists_groups_parameter[0], "\n")
    print("Score with Shape-DNA and k = 5 :", dists_groups_parameter[1])
    print(ar_dists_groups_parameter[1], "\n")
    print("Score with Shape-DNA and k = 10 :", dists_groups_parameter[2])
    print(ar_dists_groups_parameter[2], "\n")
    print("Score with Shape-DNA and k = 20 :", dists_groups_parameter[3])
    print(ar_dists_groups_parameter[3], "\n")
    print("Score with Shape-DNA and k = 40 :", dists_groups_parameter[4])
    print(ar_dists_groups_parameter[4], "\n")

    for i in range(5,len(dists_groups_parameter)):
        print("Score with ", list_files[i-5],":", dists_groups_parameter[i])
        print(ar_dists_groups_parameter[i], "\n")