from typing import Any, Type, Optional

from typediter.types import TypedIterable_T

from . import _data_formaters as formaters

def valid_init_failed(
        cls: Type[TypedIterable_T],
        i_type: type,
        init_value: Any,
        err: Exception,
        is_sample: bool = False # allows to add context for sample generation failures
) -> str:
    """ Returns a formatted failure message for valid initialisation failure

    Parameters
    ----------
    - **cls**
        the typed iterable class the instance was built from
    
    - **i_type**
        the type restriction applied 
        ( str for all tested instances, except some test samples )
    
    - **init_value**
        the value given to initialise the instance

    - **err**
        the exception raised
    
    - **is_sample**
        whether or not the failure occured in the test samples generation
        ( if yes then it prevented the actual test to run )
    """

    title = "Initialisation raised unexpected exception"
    if is_sample:
        title = f"Sample generation failed, cannot run test\n{title}"

    class_repr = formaters.typediter_class( cls, i_type )
    if init_value is None:
        # for the 'valid' init tests
        # if init_value is None we don't pass any init_value
        # (we don't actually use None, though we do for the 'invalid' tests)
        init_value_repr = '- Nothing -'
    else:
        init_value_repr = formaters.value_with_type( init_value )
    exception_repr = formaters.value_with_type( err )
    
    return (
        "\n***\n"
        f"{formaters.red_title(title)}\n"
        f"{formaters.titled_data( 'class', class_repr )}\n"
        f"{formaters.titled_data( 'intialisation value', init_value_repr )}\n"
        f"{formaters.titled_data( 'exception raised', exception_repr )}"
        "\n***\n"
    )

def valid_init_unexpected_result(
        cls: Type[TypedIterable_T],
        i_type: type,
        init_value: Any,
        result: Any,
        builtin_ref: Any
) -> str:
    """ Returns a formatted failure message for an unexpected initialisation result

    (i) means the value it has after beging initialised is 
    different from the built-in equivalent

    Parameters
    ----------
    - **cls**
        the typed iterable class the instance was built from
    
    - **i_type**
        the type restriction applied 
        ( str for all tested instances, except some test samples )
    
    - **init_value**
        the value given to initialise the instance

    - **result**
        the resulting instance that has been initialised
    
    - **builtin_ref**
        the instance of the built-in equivalent that has been initialised with the same value
    """
    
    title = "Initialisation returned unexpected result"
    class_repr = formaters.typediter_class( cls, i_type )
    if init_value is None:
        # for the 'valid' init tests
        # if init_value is None we don't pass any init_value
        # (we don't actually use None, though we do for the 'invalid' tests)
        init_value_repr = '- Nothing -'
    else:
        init_value_repr = formaters.value_with_type( init_value )
    result_repr = formaters.value_with_type( result )
    builtin_ref_repr = formaters.value_with_type( builtin_ref )
    
    return (
        "\n***\n"
        f"{formaters.red_title(title)}\n"
        f"{formaters.titled_data( 'class', class_repr )}\n"
        f"{formaters.titled_data( 'intialisation value', init_value_repr )}\n"
        f"{formaters.titled_data( 'result', result_repr )}\n"
        f"{formaters.titled_data( 'built-in reference', builtin_ref_repr )}"
        "\n***\n"
    )

def invalid_init_handling_failed(
        cls: Type[TypedIterable_T],
        i_type: type | Any,
        init_value: Any,
        err: Optional[Exception],
        expected_exception: Type[Exception]
) -> str:
    """ Returns a formatted failure message for a failure to handle invalid initialisation

    (i) Means the instance was given incompatible data, 
    and either is have not failed but should have,
    or have failed with an unexpected exception.

    Parameters
    ----------
    - **cls**
        the typed iterable class the instance was built from
    
    - **i_type**
        the type restriction applied 
        ( str for all tested instances, except some test samples )
        ( can be a non-type value to test invalid i_type init )
    
    - **init_value**
        the value given to initialise the instance

    - **err**
        the exception raised
        (None if have not failed)
    
    - **expected_exception**
        the expected exception class
    """
    
    title = "Invalid initialisation"
    if err is None:
        title += " should have failed"
    else:
        title += " failed with unexpected exception"
        
    class_repr = formaters.typediter_class( cls, i_type )
    i_type_is_valid = formaters.i_type_validity( i_type )
    init_value_repr = formaters.value_with_type( init_value )
    exception_repr = formaters.value_with_type( err )
    expected_exception_repr = formaters.type_name( expected_exception )

    return (
        "\n***\n"
        f"{formaters.red_title(title)}\n"
        f"{formaters.titled_data( 'class', class_repr )}\n"
        f"{formaters.titled_data( 'i_type validity', i_type_is_valid )}\n"
        f"{formaters.titled_data( 'intialisation value', init_value_repr )}\n"
        f"{formaters.titled_data( 'exception raised', exception_repr )}\n"
        f"{formaters.titled_data( 'expected exception', expected_exception_repr )}"
        "\n***\n"
    )