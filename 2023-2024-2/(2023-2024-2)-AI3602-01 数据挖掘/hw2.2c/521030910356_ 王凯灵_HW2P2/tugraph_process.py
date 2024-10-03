from louvain import Louvain
from graph import WeightedDiGraph
from typing import Dict


def read_from_tugraph_db(db) -> WeightedDiGraph:
    """Reads all data from the given db and returns a WeightedDiGraph instance.

    Args:
        db: A TuGraph db handler.

    Returns:
        WeightedDiGraph: A weighted directed graph instance.
    """
    txn = db.CreateReadTxn()
    edge_list = []  # Fill this list with (src, dst, weight) tuples

    # TODO: (Task 2) Read all edges from the db via the transaction txn.
    # Store the edges as (src, dst, weight) tuples in the edge_list.
    # 5-10 lines of code expected.
    #
    # Hints:
    # 1. Use txn.GetVertexIterator() to iterate over all vertices.
    #    For each vertex, get its out-going neighbors by ListDstVids().
    # 2. Refer to TuGraph documentation for details on its Python APIs.
    #    A cheat sheet is available under ./docs/tugraph-py-api.md
    # 3. Initially, the weight should be 1 for all edges.
    
    iterator = txn.GetVertexIterator()
    while iterator.IsValid():
        src = iterator.GetId()
        neighbors = iterator.ListDstVids()[0]
        for dst in neighbors:
            edge_list.append((src, dst, 1))
        iterator.Next()

    # End of TODO

    txn.Commit()
    return WeightedDiGraph(edge_list)


def Process(db, gt_map: Dict[int, int]):
    import os
    import pickle
    if not os.path.exists("res.pkl"):
        graph = read_from_tugraph_db(db)

        lv = Louvain(graph)
        res = lv.louvain()
        with open('res.pkl', 'wb') as f:
            pickle.dump((lv, res), f)
    else:
        with open('res.pkl', 'rb') as f:
            lv, res = pickle.load(f)
    res = lv.merge_communities(res, n_expected_communities=5, gt_map=gt_map)
    return res
