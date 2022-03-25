from xmlrpc.client import Boolean
import numpy as np

def isSubsetArray(A: np.ndarray, B: np.ndarray) -> Boolean:
    # True if nonzero-elements of A are in B at the same pos
    return np.logical_or(A==B, B-A==B).all()
