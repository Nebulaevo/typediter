""" Module declaring functions generating the failure messages for typed iterable tests

each function returns a formatted message giving all the needed failure informations
depending on the failure type,
there is one message formatting function for every failure type.

Exported functions
------------------
- **valid_init_failed**
    message indicating that an initialisation that should have worked,
    raised an unexpected exception

- **valid_init_unexpected_result**
    message indicating that an initialisation,
    returned an incorrect result

- **invalid_init_handling_failed**
    message indicating that an invalid initialisation that should have failed,
    wasn't handled correcly

- **iterating_over_instance_failed**
    message indicating that iterating over an instance,
    raised an expection

- **unexpected_number_of_iterations**
    message indicating that iterating over an instance,
    didn't do the expected amout of iterations

- **valid_utility_operation_failed**
    message indicating that the use of a utility function in a valid way,
    raised an unexpected exception

- **valid_utility_operation_unexpected_result**
    message indicating that the use of a utility function in a valid way,
    returned an incorrect result

- **invalid_utility_operation_handling_failed**
    message indicating that the use of a utility function in a way that should have failed,
    wasn't handled correcly

- **valid_converter_utility_operation_failed**
    message indicating that the use of a converter getter utility 
    function in a valid way, raised an unexpected exception

- **valid_converter_utility_operation_unexpected_result**
    message indicating that the use of a converter getter utility 
    function in a valid way, returned an incorrect result

- **invalid_converter_utility_operation_handling_failed**
    message indicating that the use of a converter getter utility 
    function in a way that should have failed, wasn't handled correcly

- **valid_operation_failed**
    message indicating that the execution of a valid operation,
    raised an unexpected exception

- **valid_operation_unexpected_result**
    message indicating that the execution of a valid operation,
    returned an incorrect result

- **operation_inserted_incompatible_item**
    message indicating that a typed iterable instance,
    ended up with an incompatible item after an operation

- **invalid_operation_handling_failed**
    message indicating that the execution of an operation in a way that should have failed,
    wasn't handled correctly
"""

from .initialisation import (
    valid_init_failed,
    valid_init_unexpected_result,
    invalid_init_handling_failed
)

from .iterability import (
    iterating_over_instance_failed,
    unexpected_number_of_iterations
)

from .utility_operation import (
    valid_utility_operation_failed,
    valid_utility_operation_unexpected_result,
    invalid_utility_operation_handling_failed,

    valid_converter_utility_operation_failed,
    valid_converter_utility_operation_unexpected_result,
    invalid_converter_utility_operation_handling_failed,
)

from .operation import (
    valid_operation_failed,
    valid_operation_unexpected_result,
    operation_inserted_incompatible_item,
    invalid_operation_handling_failed
)

__all__ = [
    "valid_init_failed", 
    "valid_init_unexpected_result",
    "invalid_init_handling_failed",

    "iterating_over_instance_failed",
    "unexpected_number_of_iterations",

    "valid_utility_operation_failed",
    "valid_utility_operation_unexpected_result",
    "invalid_utility_operation_handling_failed",
    "valid_converter_utility_operation_failed",
    "valid_converter_utility_operation_unexpected_result",
    "invalid_converter_utility_operation_handling_failed",

    "valid_operation_failed",
    "valid_operation_unexpected_result",
    "operation_inserted_incompatible_item",
    "invalid_operation_handling_failed",
]