import numpy as np

def agregar_cuadrados_cinematicos(X):
    valores = np.asarray(X, dtype=float)
    return np.column_stack([valores, valores**2])
