from typing import Any, Type, Optional

from typediter.types import TypedIterable_T

from . import _data_formaters as formaters

# local helpers

def _format_operation_value( 
        operation_value: Any,
        is_multiple_operation_values: bool = False, 
) -> str | list[str]:
    """ Private helper handling formatting the operation value (single sample / list of samples)

    This utility returns an individual representation of a sample or a list of representation of samples 
    depending on 'is_multiple_operation_values'

    (i) Because some operations are *args operations, sometimes the value is a list of samples
    instead of being a single sample.
    and we want to make each individual sample clear in the failure message.
    (to handle this gracefully, 'formaters.titled_data' accepts lists of strings as well as string)

    Parameters
    ----------
    - **operation_value**
        the sample, or list of samples we want to display in a failure message
    
    - **is_multiple_operation_values**
        bool indicating if the operation value is a sample or a list of samples
        (some individual samples can be lists, or other iterables)
    """
    if is_multiple_operation_values:
        return [ formaters.value_with_type( value ) for value in operation_value ]
    else:
        return formaters.value_with_type( operation_value )

# message generation

def valid_operation_failed(
        operation_name: str,
        inst: TypedIterable_T,
        operation_value: Any,
        err: Exception,
        is_multiple_operation_values: bool = False,
) -> str:
    """ Returns a formatted failure message for valid operation failure

    Parameters
    ----------
    - **operation_name**
        the name of the operation that failed
        ( usually the name of the function handling that operation )
    
    - **inst**
        the typed iterable instance the operation was performed on
    
    - **operation_value**
        the value the operation was performed with
        ( usually a sample, but can be a list of samples if testing a *args operation )
    
    - **err**
        the exception raised

    - **is_multiple_operation_values**
        boolean indicating if the operation was tested with a list of samples
        ( if the operation was called with *args )
    """

    title = f"'{operation_name}' operation raised unexpected exception"
    inst_repr = formaters.typediter_instance( inst )
    operation_value_repr = _format_operation_value( operation_value, is_multiple_operation_values )
    exception_repr = formaters.value_with_type( err )

    return (
        "\n***\n"
        f"{formaters.red_title(title)}\n"
        f"{formaters.titled_data( 'instance', inst_repr )}\n"
        f"{formaters.titled_data( 'operation value', operation_value_repr )}\n"
        f"{formaters.titled_data( 'exception raised', exception_repr )}"
        "\n***\n"
    )

def valid_operation_unexpected_result(
        operation_name: str,
        cls: Type[TypedIterable_T],
        i_type: type,
        operation_value: Any,
        expects_self_result: bool,
        result_is_self: bool,
        expected_result_type: type,
        result: Any,
        builtin_ref_result: Any,
        is_multiple_operation_values: bool = False,
) -> str:
    """ Returns a formatted failure message for an unexpected operation result

    (i) means the value returned by the test function was different than the same
    operation done on a built-in reference

    Parameters
    ----------
    - **operation_name**
        the name of the operation that failed
        ( usually the name of the function handling that operation )
    
    - **cls**
        the typed iterable class that is currently tested

    - **i_type**
        the type restriction applied 
        ( str for all tested instances )

    - **operation_value**
        the value the operation was performed with
        ( usually a sample, but can be a list of samples if testing a *args operation )

    - **expects_self_result**
        bool indicating whether we expected the value returned by the 
        test function to return the same instance as the instance the 
        operation was performed on.
    
    - **result_is_self**
        bool indicating whether the result is the same instance as
        as the instance the operation was performed on.
    
    - **expected_result_type**
        expected type for the test function return value

    - **result**
        value returned by the test function
    
    - **builtin_ref_result**
        value returned by the test function when called with a built-in reference
        and the same value
    
    - **is_multiple_operation_values**
        boolean indicating if the operation was tested with a list of samples
        ( if the operation was called with *args )
    """
    
    title = f"'{operation_name}' operation returned unexpected result"

    class_repr = formaters.typediter_class( cls, i_type )
    operation_value_repr = _format_operation_value( operation_value, is_multiple_operation_values )
    expects_self_result_repr = formaters.value_with_type( expects_self_result )
    result_is_self_repr = formaters.value_with_type( result_is_self )
    result_repr = formaters.value_with_type( result )
    expected_result_type_repr = formaters.type_name( expected_result_type )
    builtin_ref_result_repr = formaters.value_with_type( builtin_ref_result )

    return (
        "\n***\n"
        f"{formaters.red_title(title)}\n"
        f"{formaters.titled_data( 'class', class_repr )}\n"
        f"{formaters.titled_data( 'operation value', operation_value_repr )}\n"
        f"{formaters.titled_data( 'result', result_repr )}\n"
        f"{formaters.titled_data( 'result should be same instance', expects_self_result_repr )}\n"
        f"{formaters.titled_data( 'result is same instance', result_is_self_repr )}\n"
        f"{formaters.titled_data( 'expected result type', expected_result_type_repr )}\n"
        f"{formaters.titled_data( 'built-in reference result', builtin_ref_result_repr )}"
        "\n***\n"
    )

def operation_inserted_incompatible_item(
        operation_name: str,
        cls: Type[TypedIterable_T],
        i_type: type,
        operation_value: Any,
        invalid_item: Any,
        is_multiple_operation_values: bool = False,
) -> str:
    """ Returns a formatted failure message for an incompatible item found after an operation
    
    (i) an operation has inserted an incompatible item in the typed iterable
    and that no other failures occured

    Parameters
    ----------
    - **operation_name**
        the name of the operation that failed
        ( usually the name of the function handling that operation )
    
    - **cls**
        the typed iterable class that is currently tested

    - **i_type**
        the type restriction applied 
        ( str for all tested instances )

    - **operation_value**
        the value the operation was performed with
        ( usually a sample, but can be a list of samples if testing a *args operation )
    
    - **invalid_item**
        the invalid item found
    
    - **is_multiple_operation_values**
        boolean indicating if the operation was tested with a list of samples
        ( if the operation was called with *args )
    """
    
    title = f"'{operation_name}' operation inserted incompatible item in typed iterable without failing"
    class_repr = formaters.typediter_class( cls, i_type )
    operation_value_repr = _format_operation_value( operation_value, is_multiple_operation_values )
    invalid_item_repr = formaters.value_with_type( invalid_item )

    return (
        "\n***\n"
        f"{formaters.red_title(title)}\n"
        f"{formaters.titled_data( 'class', class_repr )}\n"
        f"{formaters.titled_data( 'operation value', operation_value_repr )}\n"
        f"{formaters.titled_data( 'incompatible item found', invalid_item_repr )}\n"
        "\n***\n"
    )

def invalid_operation_handling_failed(
        operation_name: str,
        cls: Type[TypedIterable_T],
        i_type: type,
        operation_value: Any,
        err: Optional[Exception],
        expected_exception: Type[Exception],
        is_multiple_operation_values: bool = False,
) -> str:
    """ Returns a formatted failure message for a failure to handle invalid operation

    (i) Means the operation was given data incompatible with the instance, 
    and either it have not failed but should have,
    or have failed with an unexpected exception.
    
    Parameters
    ----------
    - **operation_name**
        the name of the operation that failed
        ( usually the name of the function handling that operation )
    
    - **cls**
        the typed iterable class that is currently tested

    - **i_type**
        the type restriction applied 
        ( str for all tested instances )

    - **operation_value**
        the value the operation was performed with
        ( usually a sample, but can be a list of samples if testing a *args operation )
    
    - **err**
        the exception raised
        (None if have not failed)
    
    - **expected_exception**
        the expected exception class
    
    - **is_multiple_operation_values**
        boolean indicating if the operation was tested with a list of samples
        ( if the operation was called with *args )
    """
    
    title = f"Invalid '{operation_name}' operation"
    if err is None:
        title += " should have failed"
    else:
        title += " failed with unexpected exception"
    
    class_repr = formaters.typediter_class( cls, i_type )
    operation_value_repr = _format_operation_value( operation_value, is_multiple_operation_values )
    exception_repr = formaters.value_with_type( err )
    expected_exception_repr = formaters.type_name( expected_exception )

    return (
        "\n***\n"
        f"{formaters.red_title(title)}\n"
        f"{formaters.titled_data( 'class', class_repr )}\n"
        f"{formaters.titled_data( 'operation value', operation_value_repr )}\n"
        f"{formaters.titled_data( 'exception raised', exception_repr )}\n"
        f"{formaters.titled_data( 'expected exception', expected_exception_repr )}"
        "\n***\n"
    )