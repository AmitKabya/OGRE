# OGRE - Online Two-Stages Embedding Method For Large Graphs
## Overview
OGRE and its variants are fast online two-stages graph embedding algorithms for large graphs. The accuracy of existing embedding, as defined by auxiliary tests, is maximal for a core of high degree vertices. We propose to embed only this core using existing methods (such as node2vec, HOPE, GF, GCN), and then update online the remaining vertices, based on the position of their already embedded neighbors. The position of each new vertex is a combination of its first and second neighbors’ positions. We present three versions of this heuristic:

1. OGRE - a weighted combination approach which assumes an undirected graph, or the undirected graph underlying a directed graph. The position of a new vertex that is inserted to the embedding is calculated by the average embedding of its first and second order neighbours, with epsilon as a hyperparamter representing the importance of the second order neighbours.
2. DOGRE - a directed regression which assumes a directed graph. The position of a new vertex that is inserted to the embedding is calculated by the average embedding of its first and second order neighbours, where now they have directions - in, out, in-in, in-out, out-in, out-out, and the importance of each of them is determined by the regression weights.
3. WOGRE - a directed weighted regression, very similar to DOGRE. The difference is by the calculation of the parameters, where here we use a little different combination, therefore different regression results. 

## Dependencies:

- python >=3.6.8
- numpy >= 1.18.0
- scikit-learn >= 0.22.1
- heapq 
- node2vec==0.3.2
- networkx==1.11
- scipy >= 1.41
- pytorch==1.7.0
- matplotlib==3.1.3
- pandas >= 1.0.5

## Notes:
`datasets` directory consists of several small datasets. You can find the larger ones in [This Google Drive link](https://drive.google.com/drive/folders/1zycmmDES39zVlbVCYs88JTJ1Wm5FbfLz), taken from [GraphSaint public github repository](https://github.com/GraphSAINT/GraphSAINT) and from [NRL Benchmark public github repository](https://github.com/PriyeshV/NRL_Benchmark)
(go to `link prediction` or `node classification` directories, there you will find links to datasets in .mat format). Once you have your datasets, place them in the `datasets` direcotiry.

Notice you will have to adjust them to our files format (will be further explained) or provide a data loader function in order to produce the networkx graph. For .mat files, see how Youtube and Flickr datasets are loaded. You can add the appropriate condition to the function "load_data" in `evaluation_tasks` -> `eval_utils.py`. Note that when having .mat file, it has both the edges and labels. To see an example for a use go to "load_data" in `evaluation_tasks` -> `eval_utils.py` and to `evaluation_tasks` -> `calculate_static_embeddings.py`.

### What files should you have in order to embed your graph?
- In order to calculate the embedding, you first must have an edge list file:
If the graph is unweighted it consists of 2 columns: source, target (with no title, source and target share an edge).<br>
Example for unweighted graph: <br>
1 2 <br>
2 3 <br>
1 4 <br>
1 3 <br>
If the graph is weighted, it consists of 3 columns: source target weight.<br> 
Example for weighted graph: <br>
1 2 3 <br>
1 3 0.3 <br>
1 4 4.5 <br>
2 4 0.98 <br>
You can see examples for this format in `datasets` directory.

Note that in the end one must have a networkx graph, so you can change the data loader function as you want (adjusting to your file format), but remember a networkx graph is required in the end.

Another format is `.mat`, as explained above. For example you can see `datasets\Flickr.mat` and see how it is loaded in `evaluation_tasks`->`eval_utils.py`->`load_data`.
- If you want to perform vertex classification task or GCN initial embedding is used, you must provide labels file: <br>
A txt file which consists of 2 columns: node, label (no title). Notice all nodes must have labels! <br>
Example: <br>
1 0 <br>
2 0 <br>
3 1 <br>
4 2 <br>
You can see examples for this format in `labels` directory.

If your file is in `.mat` format, you do not need labels file (because it already has labels).
- If you want to perform link prediction task, you must provide non edges file: <br>
A csv file which consists of two columns: node1, node2 ; where there is no edge between them (again no title). <br>
In order to produce such file, you can use `calculate_non_edges()` function, using `from OGRE import calculate_non_edges`.
If such file does not exist, it will be created automaticly by running the function `link prediction()` on your `CalculateStaticEmbeddings` object.

## How to run?

1. First install the packages using pip.

```commandline
pip install OGRE-embed
```

2. Import OGRE and create a `CalculateStaticEmbeddings` object.
```python
from OGRE import CalculateStaticEmbeddings
# CalculateStaticEmbeddings is the main class of the package.
# Use it to embed your graph. Then you can perform link prediction or vertex classification tasks.

# create an instance of the class
embedding = CalculateStaticEmbeddings(name="example_dataset", dataset_path=".", 
                                      initial_size=[100, 1000], dim=128, is_weighted=False,
                                      choose="degree", s_a=True, epsilon=0.1,
                                      regu_val=0.1, weighted_reg=False)
```

#### CalculateStaticEmbeddings Parameters:
- **name**: Name of dataset (as the name of the edge list txt file) (string)
- **dataset_path**: Path to the dataset (string)
- **initial_size**: List of initial core sizes. (list of int)
- **dim**: Embedding dimension (int). Default is 128.
- **is_weighted**: True if the graph is weighted, else False (bool). Default is False.
- **choose**: "degrees" if the vertices of the initial core are the ones with the highest degree
(as done in our experiments), else "k_core" if the vertices of the initial core are
the ones with highest k-core score (string). Default is "degrees".
- **s_a**: True if you also want to calculate state-of-the-art embeddings (node2vec/GF/HOPE/GCN), 
else False. Default is True.

Params for OGRE:
- **epsilon**: Weight to the second order neighbours embedding. Default is 0.1.<br>
For more details you can go to the implementation - `our_embedding_methods -> OGRE.py` (float).

Params for DOGRE/WOGRE:
- **regu_val**: Regularization value for regression, only for DOGRE/WOGRE. Default is 0.<br>
For more details you can go to the implementation- `our_embedding_methods -> D_W_OGRE.py` (float).
- **weighted_reg**: True for weighted regression, else False. Default is False.

3. Calculate the embedding.
```python
embedding.calculate_static_embeddings(method=["OGRE"], initial_methods=["node2vec"])
```
#### Output:
First, If the directories `embeddings_degrees`/`embedding_k_core` do not exist,
they will be created depends on the input of `choose`(parameter of CalculateStaticEmbeddings).
If the directory `embeddings_state_of_the_art` does not exist, it will be created as well.<br>

Our embeddings will be saved in the directory `embeddings_degrees`/`embedding_k_core` under the name:<br> 
`{name_of_dataset} + {state_of_the_art} + {our_embedding} + {initial_core_size} + {epsilon}.npy`<br> 
and state-of-the-art embeddings are saved in the directory `embeddings_state_of_the_art` under the name:<br>
`{name_of_dataset} + {state_of_the_art}.npy`<br>

#### calculate_static_embeddings Parameters:
 - methods: List of our suggested embedding methods (OGRE/DOGRE/WOGRE) with whom you want to embed the given graph. Default is `["OGRE"]`.
 - initial_methods : List of state-of-the-art embedding methods (node2vec/GF/HOPE/GCN) with whom the initial core will be embed. Default is `["node2vec"]`.

4. Evaluate run time.

Evaluate running times of each method according to the initial core size
If one wishes to evaluate the run time, one can use the function `run_time()` on the `CalculateStaticEmbeddings` object.<br>
The function will create a csv file with the run time and save it in the directory `files_degrees`/`files_k_core`<br>
(depends on `choose` parameter value) under the name:<br>
`{name_of_dataset} times_1.csv`<br>
If `plot=True` a plot of the run time will be saved in the directory `plots` (directory is created if it does not exist) under the name:<br>
`{dataset_name} {initial_method} running time vs initial.png`<br>

```python
embedding.run_time(plot=True)
```

**NOTE**: If you want to evaluate the run time, you must run the function `calculate_static_embeddings()` first.

5. Perform link prediction task.

If one wishes to perform link prediction task, one can use the function `link_prediction()` on the `CalculateStaticEmbeddings` object.<br>
The function will create a csv file with the link prediction and save it in the directory `files_degrees`/`files_k_core`<br>
(depends on `choose` parameter value) under the name:<br>
`{name_of_dataset} Link Prediction.csv`<br>
Plots of the link prediction will be saved in the directory `plots` (directory is created if it does not exist) under the name:<br>
`{dataset_name} Link Prediction {...}.png`<br>

```python
embedding.link_prediction(plot=True)
```

##### link_prediction Parameters:
- **number_true_false**:
- **rounds**:
- **test_ratio**:
- **number_choose**:
- **path_non_edges**: Path to the non edges file without the file name itself. Default is `"."`.
- **non_edges_percentage**: Percentage of non edges to take.<br>
(non-edge might be too big for all nodes, choose the biggest portion your device
    can handle with). Default is 1.
- **plot**: True if you want to plot the link prediction, else False. Default is False.

**NOTE**: If you want to calculate link prediction, you must run the function `calculate_static_embeddings()` first.

6. Perform node classification tasks.

If one wishes to perform node classification task, one can use the function `node_classification()` on the `CalculateStaticEmbeddings` object.<br>
The function will create a csv file with the node classification and save it in the directory `files_degrees`/`files_k_core`
(depends on `choose` parameter value) 

[//]: # (under the name:<br>)

[//]: # (`{name_of_dataset} Link Prediction.csv`<br>)
Plots of the link prediction will be saved in the directory `plots` (directory is created if it does not exist) 
under the name:<br>
`{dataset_name} Link Prediction {...}.png`<br>

```python
embedding.node_classification(plot=True)
```

##### node_classification Parameters:
- **label_files**:
- **multi_label**: True if you want to perform a multi-label node classification task, else False. Default is False.
- **rounds**:
- **test_ratio**:
- **plot**: True if you want to plot the link prediction, else False. Default is False.

**NOTE**: If you want to calculate node classification, you must run the function `calculate_static_embeddings()` first.
