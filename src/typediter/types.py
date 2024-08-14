""" Defines utility types, for type hinting

Utility Types
-------------
- **TypedIterable_T**
    a typed iterable instance, light or complete, based on list, tuple, set, or frozenset

- **FrozenTypedIterable_T**
    a typed iterable instance, light or complete, based on tuple or frozenset

- **MutableTypedIterable_T**
    a typed iterable instance, light or complete, based on list or set
"""

from typing import TypeVar, Union

from typediter.classes.light import (
    TypedList_lt,
    TypedTuple_lt,
    TypedSet_lt,
    TypedFrozenset_lt
)
from typediter.classes.complete import (
    TypedList,
    TypedTuple,
    TypedSet,
    TypedFrozenset
)

T = TypeVar('T')

MutableTypedIterable_T = Union[
    TypedList_lt[T], 
    TypedList[T], 
    TypedSet_lt[T], 
    TypedSet[T]
]

FrozenTypedIterable_T = Union[
    TypedTuple_lt[T],
    TypedTuple[T],
    TypedFrozenset_lt[T],
    TypedFrozenset[T]
]

TypedIterable_T = Union[
    MutableTypedIterable_T[T],
    FrozenTypedIterable_T[T]
]

