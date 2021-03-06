# Shape_comparison
Scripts and pdf report of the INF555 class at Ecole Polytechnique

This project consisted in the implementation of two research papers : 
- http://reuter.mit.edu/papers/reuter-shapeDNA06.pdf
- http://www.cs.jhu.edu/~misha/Fall07/Papers/Rustamov07.pdf

These two papers aim to create a mapping between 3D shapes and vectors so that close shapes also correspond to close vectors.

Our work consisted in the comparison and the analysis of these two methods.

The two datasets we used can be downloaded here:
- http://people.csail.mit.edu/sumner/research/deftransfer/data.html
- http://segeval.cs.princeton.edu/ (the Meshes only parts)

Once they are added to the project, you can run the python scripts:
- main.py computes the coordinates of shapes and store them in .txt files. Each .txt file contains the coordinates of multiple shapes, obtained with both algorithms with a given set of parameters. You can run main.py with different parameters, and make it analyse more or less shapes. "result off k=40 N=50000 nb_cases=20 m=5.txt" is an example of the output of main.py
- final_score_per_files.py compares the efficiency of the algorithms applied with different parameters. It takes in input the .txt files that come from main.py (and that you want to compare)
- display_pca.py displays the PCA of the points contained in a .txt file obtained through main.py.
Each point corresponds to a shape, and each object is represented in multiple states (i.e. there are different shapes for the same object). The points with the same color correspond to the same objects. If the method works well, points with the same color will be close from each other.

Finally, the report details the observed results. It is only available in French for now.

