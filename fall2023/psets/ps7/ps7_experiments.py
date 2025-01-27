import numpy as np
import os
import pickle
import random
from time import time
from ps7_helpers import timeout, color, generate_k_graph, generate_line_of_ring_subgraphs, generate_random_linked_cluster, generate_hard_coloring_graphs
from ps7 import Graph, exhaustive_search_coloring, iset_bfs_3_coloring, sat_3_coloring
random.seed(120)

##################################
#                                #
#          Experiments           #
#                                #
##################################

'''
    Part B: Run some tests to figure out the relative performance of the 3-coloring algorithms!
    We're comparing exhaustive search, ISET + BFS, and Reduction to 3-SAT.
    There are two types of graphs we generate randomnly.
    The third type, hard graphs, are imported under the hard_instances directory
    1. Line of Rings:
        We generate rings and connect them together.
        Parameters to adjust:
            subgraph_line_parameter: number of rings in the line
    2. Randomized Cluster Connections (Semi Independent Sets):
        We create clusters of independent sets. Then, for each pair of nodes
        that are in different clusters, we add an edge between them with probability p.
        Parameters to adjust:
            cluster_graph_p_parameter: probability of joining an edge between two nodes in different clusters
            cluster_graph_cluster_size_parameter: number of nodes per cluster
            cluster_graph_cluster_quantity_parameter: number of clusters
    TIMEOUT_LENGTH: Number of seconds before an algorithm is set to time out.
    When you run the test file, you can see the performance of every combination of parameters
    and whether each algorithm timed out. Use the information from the printouts to answer question 1(b).
'''

# The timeout length in seconds
TIMEOUT_LENGTH = 1

def kbench():
    algs = [
            # ("Exhaustive Coloring", lambda g: exhaustive_search_coloring(g)),
            # ("ISET BFS Coloring", lambda g: iset_bfs_3_coloring(g)), 
            ("SAT Coloring", lambda g: sat_3_coloring(g))
            ]
    print("complete graphs:")
    for k in range(850,900,1):
        g = generate_k_graph(Graph,k)
        print(k, "graph, m =", k*(k-1)/2)
        for (alg_name, alg) in algs:
            timedout = False
            try:
                with timeout(seconds=TIMEOUT_LENGTH):
                    alg(g.clone())
            except TimeoutError:
                timedout = True
            col = color.GREEN if not timedout else color.ORANGE
            if timedout:
                symbol = color.BOLD + col + u'\u23f1' + color.END + color.END
            else:
                symbol = color.BOLD + col + (u'\u2713' ) + color.END + color.END
            print("\t\t" + symbol + "  " + alg_name + ": ", ("Timeout" if timedout else "Finished"))

def benchmark():
    # You may experiment with these parameters if you wish!
    # Each of these ranges is formatted with a minimum, maximum, and step size.
    subgraph_line_parameter_range = (2000, 30000, 100)
    cluster_graph_p_parameter_range = (0.2, 0.95, 0.37)
    cluster_graph_cluster_size_parameter_range = (2, 21, 8)
    cluster_graph_cluster_quantity_parameter_range = (2, 4, 1)

    algs = [
            # ("Exhaustive Coloring", lambda g: exhaustive_search_coloring(g)),
            # ("ISET BFS Coloring", lambda g: iset_bfs_3_coloring(g)), 
            ("SAT Coloring", lambda g: sat_3_coloring(g))
            ]

    print("Line of Rings")
    print()
    for r in [3,4,5]:
        print("Size of ring", r)
        for rings in range(subgraph_line_parameter_range[0], subgraph_line_parameter_range[1], subgraph_line_parameter_range[2]):
            print("\tNumber of rings", rings)
            g = generate_line_of_ring_subgraphs(Graph, rings, r)
            size_text = "\t(n = {}, m = {})".format(g.N, sum([len(v_lst) for v_lst in g.edges]) // 2)
            print(size_text)
            for (alg_name, alg) in algs:
                timedout = False
                try:
                    with timeout(seconds=TIMEOUT_LENGTH):
                        alg(g.clone())
                except TimeoutError:
                    timedout = True
                col = color.GREEN if not timedout else color.ORANGE
                if timedout:
                    symbol = color.BOLD + col + u'\u23f1' + color.END + color.END
                else:
                    symbol = color.BOLD + col + (u'\u2713' ) + color.END + color.END
                print("\t\t" + symbol + "  " + alg_name + ": ", ("Timeout" if timedout else "Finished"))

    print()
    print()
    print("Randomized Cluster Connections (Semi Independent Sets)")
    print()
    for p in np.arange(cluster_graph_p_parameter_range[0], cluster_graph_p_parameter_range[1], cluster_graph_p_parameter_range[2]):
        # print()
        print("Probability of keeping edge", p)
        for q in range(cluster_graph_cluster_quantity_parameter_range[0], cluster_graph_cluster_quantity_parameter_range[1], cluster_graph_cluster_quantity_parameter_range[2]):
            print("\tNumber of clusters", q)
            for s in range(cluster_graph_cluster_size_parameter_range[0], cluster_graph_cluster_size_parameter_range[1], cluster_graph_cluster_size_parameter_range[2]):
                # print()
                print("\t\tSize of cluster", s)
                g = generate_random_linked_cluster(Graph, s, q, p)
                size_text = "\t\t(n = {}, m = {})".format(g.N, sum([len(v_lst) for v_lst in g.edges]) // 2)
                print(size_text)
                for (alg_name, alg) in algs:
                    timedout = False
                    try:
                        with timeout(seconds=TIMEOUT_LENGTH):
                            alg(g.clone())
                    except TimeoutError:
                        timedout = True
                    col = color.GREEN if not timedout else color.ORANGE
                    if timedout:
                        symbol = color.BOLD + col + u'\u23f1' + color.END + color.END
                    else:
                        symbol = color.BOLD + col + (u'\u2713' ) + color.END + color.END
                    print("\t\t\t" + symbol + "  " + alg_name + ": ", ("Timeout" if timedout else "Finished"))

    print()
    print()


def hard_instance_benchmark():
    print("Hard instances")
    print()

    # # Graph generation and Pickle dumping code (keep commented out)
    # print("Constructing a hard instance")
    # g = generate_hard_coloring_graphs(Graph, 1000)
    # with open(f'{g.N}_node_instance.pickle', 'wb') as f:
    #     pickle.dump(g, f)

    # Pickle loading code
    print("Reading a hard instance from Pickle file")
    for filename in sorted(os.listdir('./hard_instances'), key=lambda x: int(x.split('_')[0])):
        with open(f'./hard_instances/{filename}', 'rb') as f:
            g = pickle.load(f)
    
        print("Finished constructing/reading a hard instance with", g.N, "nodes")
        algs = [("Exhaustive Coloring", lambda g: exhaustive_search_coloring(g)),
                ("ISET BFS Coloring", lambda g: iset_bfs_3_coloring(g)), 
                ("SAT Coloring", lambda g: sat_3_coloring(g))]
        for (alg_name, alg) in algs:
            timedout = False
            try:
                with timeout(seconds=TIMEOUT_LENGTH):
                    t1 = time()
                    alg(g.clone())
                    t2 = time()
                    time_taken = t2 - t1
            except TimeoutError:
                timedout = True
            col = color.GREEN if not timedout else color.ORANGE
            if timedout:
                symbol = color.BOLD + col + u'\u23f1' + color.END + color.END
            else:
                symbol = color.BOLD + col + (u'\u2713' ) + color.END + color.END
                is_colorable = "Found 3-coloring" if g.is_graph_coloring_valid() else "No 3-coloring found"
            print("\t\t" + symbol + "  " + alg_name + ": ", ("Timeout" if timedout else f'Finished, Time taken: {time_taken} ({is_colorable})'))
    
# random graph testing
if __name__ == "__main__":
    # kbench()
    benchmark()
    # hard_instance_benchmark()