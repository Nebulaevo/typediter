from typing import Any

from typediter.types import TypedIterable_T

from . import _data_formaters as formaters

def iterating_over_instance_failed(
        err: Exception,
        inst: TypedIterable_T
) -> str:
    """ Returns a formatted failure message for iteration failure
    
    (i) tying to iterate over a typed iterable instance raised and exception

    Parameters
    ----------
    - **err**
        the exception raised

    - **inst**
        the typed iterable instance
    """

    title = "Looping over instance raised unexpected exception"
    inst_repr = formaters.typediter_instance( inst )
    exception_repr = formaters.value_with_type( err )

    return (
        "\n***\n"
        f"{formaters.red_title(title)}\n"
        f"{formaters.titled_data( 'instance', inst_repr )}\n"
        f"{formaters.titled_data( 'exception raised', exception_repr )}"
        "\n***\n"
    )

def unexpected_number_of_iterations(
        inst: TypedIterable_T,
        builtin_ref: Any,
        loops_done: int,
        expected_iterations: int,
) -> str:
    """ Returns a formatted failure message for unexpected number of iteration

    (i) indicating that looping over the instance didn't do the expected number of loops 
    
    Parameters
    ----------
    - **inst**
        the typed iterable instance
    
    - **builtin_ref**
        the instance of the built-in equivalent that has been initialised with the same value
    
    - **loops_done**
        the actual number of loops over the typed iterable instance
    
    - **expected_iterations**
        the number of loops expected
        ( deduced from the length of the builtin_ref )
    """

    title = "Looping over instance did an unexpected number of loops"
    inst_repr = formaters.typediter_instance( inst )
    builtin_ref_repr = formaters.value_with_type( builtin_ref )
    
    return (
        "\n***\n"
        f"{formaters.red_title(title)}\n"
        f"{formaters.titled_data( 'instance', inst_repr )}\n"
        f"{formaters.titled_data( 'built-in reference', builtin_ref_repr )}\n"
        f"{formaters.titled_data( 'loops', str(loops_done) )}\n"
        f"{formaters.titled_data( 'expected loops', str(expected_iterations) )}"
        "\n***\n"
    )