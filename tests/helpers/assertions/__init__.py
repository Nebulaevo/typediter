""" Module providing assertion helper functions for typed iterable tests

each function is performing a certain operation and a number of assertions
to check if the operation has behaved as expected

Exported Functions
------------------
- **initialisation_succeeds**
    testing initialisation of typed iterable instances 
    with compatible values and a valid i_type

- **initialisation_fails**
    testing initialisation of typed iterable instances 
    with incompatible items or invalid i_type

- **typed_iterable_converter_utility_succeeds**
    testing 'get_converter_func' util,
    with compatible values

- **typed_iterable_converter_utility_fails**
    testing 'get_converter_func' util,
    with incompatible values

- **frozen_builtin_converter_utility_succeeds**
    testing 'get_typesafe_tuple_converter_func' 
    and 'get_typesafe_frozenset_converter_func' utils,
    with compatible values

- **frozen_builtin_converter_utility_fails**
    testing 'get_typesafe_tuple_converter_func' 
    and 'get_typesafe_frozenset_converter_func' utils,
    with incompatible values

- **filter_items_utility**
    testing the 'filter_items' function

- **typechecking_utility**
    testing 'is_typediter_instance' 
    and 'is_typediter_subclass' type-checking utils

- **operation_succeeds**
    testing operation on typed iterable instances
    with compatible operation values

- **operation_fails**
    testing operation on typed iterable instances
    with incompatible operation values
"""


from .initialisation_asserts import (
    initialisation_succeeds,
    initialisation_fails
)

from .iterability_asserts import instances_are_iterable

from .utility_asserts import (
    typed_iterable_converter_utility_succeeds,
    typed_iterable_converter_utility_fails,
    frozen_builtin_converter_utility_succeeds,
    frozen_builtin_converter_utility_fails,
    filter_items_utility,
    typechecking_utility
)

from .operation_asserts import (
    operation_succeeds,
    operation_fails
)

__all__ = [
    "initialisation_succeeds", 
    "initialisation_fails",
    
    "instances_are_iterable",

    "typed_iterable_converter_utility_succeeds",
    "typed_iterable_converter_utility_fails",

    "frozen_builtin_converter_utility_succeeds",
    "frozen_builtin_converter_utility_fails",

    "filter_items_utility",
    "typechecking_utility",

    "operation_succeeds",
    "operation_fails",
]