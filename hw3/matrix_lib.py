from __future__ import annotations
from typing import Any, Tuple, Dict
import numpy as np
from numpy.lib.mixins import NDArrayOperatorsMixin


class Matrix:
    _matmul_cache: Dict[Tuple[int,int], np.ndarray] = {}
    _hash_mod = 17

    def __init__(self, data: Any):
        arr = np.array(data)
        if arr.ndim != 2:
            raise ValueError("Matrix must be 2-dimensional")
        self._data = arr.astype(int)

    @property
    def shape(self) -> Tuple[int,int]:
        return self._data.shape
    
    def __str__(self) -> str:
        rows = ["[" + ", ".join(str(int(x)) for x in row) + "]" for row in self._data]
        return "[" + ",\n ".join(rows) + "]"
    
    def to_file(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(self))

    def __add__(self, other: Matrix) -> Matrix:
        if not isinstance(other, Matrix):
            return NotImplemented
        if self.shape != other.shape:
            raise ValueError(f"Addition: shapes must match, got {self.shape} and {other.shape}")
        return Matrix(self._data + other._data)

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other: Matrix) -> Matrix:
        if not isinstance(other, Matrix):
            return NotImplemented
        if self.shape != other.shape:
            raise ValueError(f"Elementwise multiply: shapes must match, got {self.shape} and {other.shape}")
        return Matrix(self._data * other._data)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __matmul__(self, other: Matrix) -> Matrix:
        if not isinstance(other, Matrix):
            return NotImplemented
        if self.shape[1] != other.shape[0]:
            raise ValueError(f"Matmul: inner dimensions must be equal, got {self.shape} and {other.shape}")
        key = (hash(self), hash(other))
        cached = Matrix._matmul_cache.get(key)
        if cached is not None:
            return Matrix(cached.copy())
        res = self._data @ other._data
        Matrix._matmul_cache[key] = res.copy()
        return Matrix(res)

    def __hash__(self) -> int:
        # (sum of all elemets) % _hash_mod
        s = int(self._data.sum())
        return s % self._hash_mod

    @classmethod
    def clear_cache(cls):
        cls._matmul_cache.clear()

    @classmethod
    def cache_contents(cls):
        return list(cls._matmul_cache.keys())

    @classmethod
    def from_numpy(cls, arr: np.ndarray) -> "Matrix":
        return cls(arr.copy())


class MatrixND(NDArrayOperatorsMixin):
    __array_priority__ = 1000

    def __init__(self, data: Any):
        arr = np.array(data)
        if arr.ndim != 2:
            raise ValueError("MatrixND must be 2-dimensional")
        self._data = arr
        
    @property
    def data(self) -> np.ndarray:
        return self._data

    @data.setter
    def data(self, value: Any) -> None:
        arr = np.array(value)
        if arr.ndim != 2:
            raise ValueError("MatrixND must be 2-dimensional")
        self._data = arr

    @property
    def shape(self) -> Tuple[int, int]:
        return self._data.shape

    def __str__(self) -> str:
        rows = ["[" + ", ".join(str(int(x)) for x in row) + "]" for row in self._data]
        return "[" + ",\n ".join(rows) + "]"

    def to_file(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(self))

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        arrays = [x._data if isinstance(x, MatrixND) else x for x in inputs]
        result = getattr(ufunc, method)(*arrays, **kwargs)

        if isinstance(result, tuple):
            out = []
            for r in result:
                if isinstance(r, np.ndarray) and r.ndim == 2:
                    out.append(type(self)(r))
                else:
                    out.append(r)
            return tuple(out)

        if isinstance(result, np.ndarray):
            if result.ndim == 2:
                return type(self)(result)
            return result

        return result

    @classmethod
    def from_numpy(cls, arr: np.ndarray) -> "MatrixND":
        return cls(arr.copy())