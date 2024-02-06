# GridCal
# Copyright (C) 2015 - 2024 Santiago Peñate Vera
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from typing import Union, Dict, Tuple, List
import numpy as np
import numba as nb
from GridCalEngine.basic_structures import Numeric, NumericVec, IntVec
from GridCalEngine.Core.Devices.sparse_array import SparseArray


@nb.njit()
def compress_array_numba(value, base):
    """

    :param value:
    :param base:
    :return:
    """
    data = list()
    indptr = list()
    for i, x in enumerate(value):
        if x != base:
            data.append(x)
            indptr.append(i)
    return data, indptr


@nb.njit()
def compress_array_numba_map(value, base) -> Dict[int, Numeric]:
    """

    :param value:
    :param base:
    :return:
    """
    data = dict()
    for i, x in enumerate(value):
        if x != base:
            data[i] = x
    return data


def check_if_sparse(arr: Union[NumericVec], sparsity: float = 0.8) -> Tuple[bool, Union[float, int]]:
    """
    Check if the array is sparse
    :param arr: vector
    :param sparsity: proportion of non-repeated elements
    :return: is sparse, most frequent value
    """
    # truncate the sparsity value
    if sparsity > 0.99:
        sparsity = 0.9

    # compute the minimum number of values to evaluate
    min_elements = int(float(len(arr)) * (1.0 - sparsity))
    if min_elements < 1:
        min_elements = 1

    # if less than min_elements elements, it cannot be sparse
    if len(arr) < min_elements:
        return False, 0

    # declare the map to keep the frequency counter
    cnt: Dict[Numeric, int] = dict()

    for i, val in enumerate(arr):

        # add entry / increase entry (in the C++ map this works)
        dval = cnt.get(val, 0)
        cnt[val] = dval + 1

        # do not check all the vector if the histogram size is telling us that it is not sparse
        if len(cnt) > min_elements:
            return False, 0.0

    if len(cnt) > min_elements:
        # is not sparse
        return False, 0.0
    else:
        # variables to compare and keep the most frequent
        max_val = 0  # value with the most frequency
        max_freq: int = 0  # frequency of max_val

        # determine the most frequent
        for value, count in cnt.items():
            if count > max_freq:
                max_val = value
                max_freq = count

        # it is sparse
        return True, max_val


class Profile:
    """
    Profile
    """

    def __init__(self, default_value, arr: Union[None, NumericVec] = None, sparsity: int = 0.8):

        self._is_sparse: bool = False

        self._sparse_array: Union[SparseArray, None] = None

        self._dense_array: Union[NumericVec, None] = None

        self._sparsity_threshold: float = sparsity

        self._dtype = type(default_value)  # float by default

        self._initialized: bool = False

        self.default_value = default_value

        if arr is not None:
            self.set(arr=arr)

    def info(self):
        """
        Return dictionary with information about the profile object and its content
        :return:
        """
        return {
            "me": hex(id(self)),
            "initialized": self._initialized,
            "is_sparse": self._is_sparse,
            "sparsity_threshold": self._sparsity_threshold,
            "dense_array": {"me": hex(id(self._dense_array)),
                            "size": len(self._dense_array)} if self._dense_array is not None else "None",
            "sparse_array": self._sparse_array.info() if self._sparse_array is not None else "None",
        }

    def get_sparse_map(self) -> Dict[int, Numeric]:
        """
        Return the dictionary hosting the sparse data if this profile is sparse
        :return: Dict[int, Numeric]
        """
        if self._sparse_array is not None:
            return self._sparse_array.get_map()

    @property
    def dtype(self) -> type:
        """
        Get the declared type
        :return: type
        """
        return self._dtype

    @property
    def is_sparse(self) -> bool:
        """
        is the profile sparse?
        :return: bool
        """
        return self._is_sparse

    @property
    def is_initialized(self) -> bool:
        """
        is the profile initialized?
        :return: bool
        """
        return self._initialized

    def create_sparse(self, size: int, default_value: Numeric):
        """
        Build sparse from definition
        :param size: size
        :param default_value: default value
        """
        self._is_sparse = True
        self._sparse_array = SparseArray()
        self._sparse_array.create(size=size, default_value=default_value)
        self._initialized = True

    def create_dense(self, size: int, default_value: Numeric):
        """
        Create a dense profile
        :param size: size
        :param default_value: default value
        """
        self._is_sparse = False
        self._dense_array = np.full(size, default_value)
        self._sparse_array = None
        self._initialized = True

    def set(self, arr: NumericVec):
        """
        Set array value
        :param arr:
        :return:
        """
        if len(arr) > 0:
            u, counts = np.unique(arr, return_counts=True)
            f = len(u) / len(arr)  # sparsity factor
            if f < self._sparsity_threshold:
                ind = np.argmax(counts)
                base = u[ind]  # this is the most frequent value
                if isinstance(base, np.bool_):
                    base = bool(base)

                self._is_sparse = True
                self._sparse_array = SparseArray()

                if len(u) > 1:
                    if isinstance(arr, np.ndarray):
                        data_map = compress_array_numba_map(arr, base)
                    else:
                        raise Exception('Unknown profile type' + str(type(arr)))
                else:
                    data_map = dict()

                self._sparse_array.create(size=len(arr),
                                          default_value=base,
                                          data=data_map)
                self._dtype = type(base)
            else:
                self._is_sparse = False
                self._dense_array = arr
                self._dtype = arr.dtype
        else:
            self._is_sparse = False
            self._dense_array = arr
            self._dtype = arr.dtype

        self._initialized = True

    def __getitem__(self, key: int):
        """
        Get item
        :param key: index position
        :return: value at "key"
        """
        if isinstance(key, int):

            if self._is_sparse:
                return self._sparse_array[key]
            else:
                return self._dense_array[key]
        else:
            raise TypeError("Key must be an integer")

    def __setitem__(self, key: int, value):
        """
        Set item
        :param key: item index
        :param value: value to set
        """
        if isinstance(key, int):

            if self._is_sparse:
                assert key < self._sparse_array.size()
                self._sparse_array[key] = value
            else:
                assert key < len(self._dense_array)
                self._dense_array[key] = value

        else:
            raise TypeError("Key must be an integer")

    def convert_sparse_to_dense(self) -> None:
        """
        Convert this profile to sparse
        :return: Nothing
        """
        if self._is_sparse:
            self._dense_array = self._sparse_array.toarray()
            self._sparse_array = None
            self._is_sparse = False

    def resize(self, n: int):
        """
        Resize the profile
        :param n: new size
        """
        if isinstance(n, int):
            if self._initialized:
                if self._is_sparse:
                    self._sparse_array.resize(n)
                else:
                    self._dense_array.resize(n)
            else:
                self._initialized = True
                self.create_sparse(n, self.default_value)
        else:
            raise TypeError("The size must be an integer")

    def resample(self, indices: IntVec):
        """
        Resample this profile in-place
        :param indices: new indices
        """
        if self._is_sparse:
            self._sparse_array.resample(indices=indices)
        else:
            self._dense_array = self._dense_array[indices]

    def size(self) -> int:
        """
        Get the size
        :return: integer
        """
        if self._initialized:
            return self._sparse_array.size() if self._is_sparse else len(self._dense_array)
        else:
            return 0

    def toarray(self) -> NumericVec:
        """
        Get dense numpy array representation
        :return: NumericVec
        """
        if self._is_sparse:
            return self._sparse_array.toarray()
        else:
            return self._dense_array

    def tolist(self) -> List[Union[int, float]]:
        """
        Get dense list representation
        :return: List[Union[int, float]]
        """
        return self.toarray().tolist()
