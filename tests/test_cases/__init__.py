""" Module declaring unittest TestCases for testing typediter

Exported Classes
----------------
- **BaseTest**
    all other tests are dependent on the behaviour tested in that class,
    other tests shouldn't be executed if this one fails.
    - testing instance initialisation in different condition
    - testing generated instances iterability

- **UtilityTests**
    testing utility functions:
        - typediter.utils.is_typediter_instance
        - typediter.utils.is_typediter_subclass
        - typediter.utils.filter_items
        - typediter.utils.get_converter_func
        - typediter.utils.get_typesafe_tuple_converter_func
        - typediter.utils.get_typesafe_frozenset_converter_func
    
- **CommonCopyTests**
    common test for all typed iterable classes that have a 'copy' method
    (all except for those based on tuple)

- **CommonSetTests**
    testing all common overridden operations between set and frozent based typed iterables
    (does all the tests needed for the frozenset based typed iterables)

- **CommonListTupleTests**
    testing all common overridden operations between list and tuple based typed iterables
    (does all the tests needed for tuple based typed iterables)

- **TypedListTests**
    testing list overridden operations
    (excluding those already tested in common testcases)

- **TypedSetTests**
    testing set overridden operations 
    (excluding those already tested in common testcases)
"""

from .base import BaseTest
from .utility import UtilityTests

from .common_copy import CommonCopyTests
from .common_tuple_list import CommonListTupleTests
from .common_set import CommonSetTests

from .list import TypedListTests
from .set import TypedSetsTests

__all__ = [
    "BaseTest", 
    "UtilityTests",
    "CommonCopyTests", "CommonListTupleTests", "CommonSetTests",
    "TypedListTests", "TypedSetsTests"
]