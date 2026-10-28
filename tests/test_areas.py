import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
from datasets import load_areas

def test_areas_shape_and_truth():
    df, adj, truth = load_areas(return_truth=True)
    assert len(df) == 49 and len(adj) == 49 and all(len(v) in (3, 5, 8) for v in adj.values())
    # neighbours share risk: spatial component correlates with the neighbour mean
    nb_mean = np.array([truth["spatial"][adj[i]].mean() for i in range(49)])
    assert np.corrcoef(truth["spatial"], nb_mean)[0, 1] > 0.8
    assert df.has_facility.sum() == 3 and (df.travel_min_to_nearest >= 2).all()
