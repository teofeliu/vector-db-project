# hnsw_index/utils.py
import numpy as np

def random_level(M: int, num_nodes: int) -> int:
    return min(int(-np.log(np.random.uniform()) * M), 
               int(np.log2(num_nodes + 1)))