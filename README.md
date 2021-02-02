# OGRE - Online Two-Stages Embedding Method For Large Graphs

**Contact**

******@gmail.com

## Overview
OGRE and its variants are fast online two-stages graph embedding algorithms for large graphs. The accuracy of existing embedding, as defined by auxiliary tests, is maximal for a core of high degree vertices. We propose to embed only this core using existing methods (such as node2vec, HOPE, GF, GCN), and then update online the remaining vertices, based on the position of their already embedded neighbors. The position of each new vertex is a combination of its first and second neighbors’ positions. We present three versions of this heuristic:

1. OGRE - a weighted combination approach which assumes an undirected graph, or the undirected graph underlying a directed graph. The position of a new vertex that is inserted to the embedding is calculated by the average embedding of its first and second order neighbours, with epsilon as a hyperparamter representing the importance of the second order neighbours.
2. DOGRE - a directed regression which assumes a directed graph. The position of a new vertex that is inserted to the embedding is calculated by the average embedding of its first and second order neighbours, where now they have directions - in, out, in-in, in-out, out-in, out-out, and the importance of each of them is determined by the regression.
3. WOGRE - a directed weighted regression, very similar to DOGRE. The difference is by the calculation of the parameters, where here we use a little different combination, therefore different regression results. 

## About This Repo
This repo contains source code of our three suggested embedding algorithms for large graphs.

