from typing import Any, Type, Optional

from . import _data_formaters as formaters


def valid_utility_operation_failed(
        operation_name: str,
        operation_value: Any,
        err: Exception,
) -> str:
    """ Returns a formatted failure message for a failure of a valid call to a utility

    Parameters
    ----------
    - **operation_name**
        the name of the utility function that failed
        ( usually the name of the function handling that operation )

    - **operation_value**
        the sample value the operation was performed with
    
    - **err**
        the exception raised
    """

    title = f"Utility operation '{operation_name}' raised unexpected exception"
    op_value_repr = formaters.value_with_type( operation_value )
    exception_repr = formaters.value_with_type( err )
    
    return (
        "\n***\n"
        f"{formaters.red_title(title)}\n"
        f"{formaters.titled_data( 'operation value', op_value_repr )}\n"
        f"{formaters.titled_data( 'exception raised', exception_repr )}"
        "\n***\n"
    )

def valid_utility_operation_unexpected_result(
        operation_name: str,
        operation_value: Any,
        result: Any,
        expected_result: Any,
) -> str:
    """ Returns a formatted failure message for an unexpected result of a valid call to a utility 

    Parameters
    ----------
    - **operation_name**
        the name of the utility function that failed
        (usually the name of the function handling that operation)
    
    - **operation_value**
        the sample value the operation was performed with

    - **result**
        value returned by the utility function

    - **expected_result**
        expected result for the operation
    """
    
    title = f"Utility operation '{operation_name}' returned unexpected result"
    op_value_repr = formaters.value_with_type( operation_value )
    result_repr = formaters.value_with_type( result )
    expected_result_repr = formaters.value_with_type( expected_result )

    return (
        "\n***\n"
        f"{formaters.red_title(title)}\n"
        f"{formaters.titled_data( 'operation value', op_value_repr )}\n"
        f"{formaters.titled_data( 'result', result_repr )}\n"
        f"{formaters.titled_data( 'expected result', expected_result_repr )}"
        "\n***\n"
    )

def invalid_utility_operation_handling_failed(
        operation_name: str,
        operation_value: Any,
        err: Optional[Exception],
        expected_exception: Type[Exception],
):
    """ Returns a formatted failure message for a failure to handle an invalid utility call
    
    Parameters
    ----------
    - **operation_name**
        the name of the utility function that failed
        ( usually the name of the function handling that operation )
    
    - **operation_value**
        the sample value the operation was performed with

    - **err**
        the exception raised
        (None if have not failed)

    - **expected_exception**
        the expected exception class
    """

    title = f"Invalid use of utility operation '{operation_name}'"
    if err is None:
        title += " should have failed"
    else:
        title += " failed with unexpected exception"

    op_value_repr = formaters.value_with_type( operation_value )
    exception_repr = formaters.value_with_type( err )
    expected_exception_repr = formaters.type_name( expected_exception )

    return (
        "\n***\n"
        f"{formaters.red_title(title)}\n"
        f"{formaters.titled_data( 'operation value', op_value_repr )}\n"
        f"{formaters.titled_data( 'exception raised', exception_repr )}\n"
        f"{formaters.titled_data( 'expected exception', expected_exception_repr )}"
        "\n***\n"
    )

# Converters

def valid_converter_utility_operation_failed(
        operation_name: str,
        operation_value: Any,
        converting_to: type,
        i_type: type,
        err: Exception,
) -> str:
    """ Returns a formatted failure message for a failure of a valid call to a converter getter utility

    Parameters
    ----------
    - **operation_name**
        the name of the utility function that failed
        ( usually the name of the function handling that operation )

    - **operation_value**
        the sample value the operation was performed with
    
    - **converting_to**
        the type of items that should have been returned by the converter
    
    - **i_type**
        the type restriction applied to the converter

    - **err**
        the exception raised
    """

    title = f"Utility operation '{operation_name}' raised unexpected exception"
    op_value_repr = formaters.value_with_type( operation_value )
    converting_to_repr = formaters.type_name( converting_to )
    i_type_repr = formaters.type_name( i_type )
    exception_repr = formaters.value_with_type( err )
    
    return (
        "\n***\n"
        f"{formaters.red_title(title)}\n"
        f"{formaters.titled_data( 'operation value', op_value_repr )}\n"
        f"{formaters.titled_data( 'conveting to', converting_to_repr )}\n"
        f"{formaters.titled_data( 'with i_type', i_type_repr )}\n"
        f"{formaters.titled_data( 'exception raised', exception_repr )}"
        "\n***\n"
    )

def valid_converter_utility_operation_unexpected_result(
        operation_name: str,
        operation_value: Any,
        converting_to: type,
        i_type: type,
        result: Any,
        expected_result: Any,
) -> str:
    """ Returns a formatted failure message for an unexpected result of a valid call to a converter getter utility 

    Parameters
    ----------
    - **operation_name**
        the name of the utility function that failed
        (usually the name of the function handling that operation)
    
    - **operation_value**
        the sample value the operation was performed with

    - **converting_to**
        the type of items that should have been returned by the converter
    
    - **i_type**
        the type restriction applied to the converter

    - **result**
        value returned by the utility function

    - **expected_result**
        expected result for the operation
    """
    
    title = f"Utility operation '{operation_name}' returned unexpected result"
    op_value_repr = formaters.value_with_type( operation_value )
    converting_to_repr = formaters.type_name( converting_to )
    i_type_repr = formaters.type_name( i_type )
    result_repr = formaters.value_with_type( result )
    expected_result_repr = formaters.value_with_type( expected_result )

    return (
        "\n***\n"
        f"{formaters.red_title(title)}\n"
        f"{formaters.titled_data( 'operation value', op_value_repr )}\n"
        f"{formaters.titled_data( 'conveting to', converting_to_repr )}\n"
        f"{formaters.titled_data( 'with i_type', i_type_repr )}\n"
        f"{formaters.titled_data( 'result', result_repr )}\n"
        f"{formaters.titled_data( 'expected result', expected_result_repr )}"
        "\n***\n"
    )

def invalid_converter_utility_operation_handling_failed(
        operation_name: str,
        operation_value: Any,
        converting_to: type,
        i_type: type | Any,
        err: Optional[Exception],
        expected_exception: Type[Exception],
):
    """ Returns a formatted failure message for a failure to handle an invalid converter getter utility call
    
    Parameters
    ----------
    - **operation_name**
        the name of the utility function that failed
        ( usually the name of the function handling that operation )
    
    - **operation_value**
        the sample value the operation was performed with

    - **converting_to**
        the type of items that should have been returned by the converter
    
    - **i_type**
        the type restriction applied to the converter
        ( can be a non-type value to test invalid i_type )

    - **err**
        the exception raised
        (None if have not failed)

    - **expected_exception**
        the expected exception class
    """

    title = f"Invalid use of utility operation '{operation_name}'"
    if err is None:
        title += " should have failed"
    else:
        title += " failed with unexpected exception"

    op_value_repr = formaters.value_with_type( operation_value )
    converting_to_repr = formaters.type_name( converting_to )
    i_type_is_valid = formaters.i_type_validity( i_type )
    exception_repr = formaters.value_with_type( err )
    expected_exception_repr = formaters.type_name( expected_exception )

    return (
        "\n***\n"
        f"{formaters.red_title(title)}\n"
        f"{formaters.titled_data( 'operation value', op_value_repr )}\n"
        f"{formaters.titled_data( 'conveting to', converting_to_repr )}\n"
        f"{formaters.titled_data( 'i_type validity', i_type_is_valid )}\n"
        f"{formaters.titled_data( 'exception raised', exception_repr )}\n"
        f"{formaters.titled_data( 'expected exception', expected_exception_repr )}"
        "\n***\n"
    )