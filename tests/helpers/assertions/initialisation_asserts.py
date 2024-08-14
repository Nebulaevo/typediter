import unittest
from typing import Any, Iterable, Type

from typediter.exceptions import _TypedIterError
from typediter.types import TypedIterable_T

from tests.helpers import msg
from . import _helpers

# ---------- Initialisation ----------

def initialisation_succeeds( 
        test_case: unittest.TestCase,
        classes: Iterable[ Type[TypedIterable_T] ],
        init_values: list 
):
    """ Asserts that all given classes can be initialised with all given init_values

    to ensure that the result is correct we compare the initialised version 
    with the result in the built-in equivalent

    Parameters
    ----------
    - **test_case**
        the TestCase class from which the function is called

    - **classes**
        iterable containing the typed iterable classes to run the test on

    - **init_values**
        test sample list generated from a TestSamples instance that will be used to initialise the instances
    """

    for typed_iterable_cls in classes:
        
        with test_case.subTest( typed_iterable_cls=typed_iterable_cls ):
            builtin_reference_cls = _helpers.get_builtin_equivalent(
                typed_iterable_cls
            )

            for index, init_value in enumerate(init_values):            
                # ----- SET UP

                # to simplify handling 'generator' samples
                # (see 'extract_test_values' docstring)
                init_value, value_A, value_B = _helpers.extract_test_values( 
                    init_values, index 
                )

                if init_value is None:
                    builtin_reference = builtin_reference_cls()
                else:
                    builtin_reference = builtin_reference_cls(value_A)
                
                # ----- TEST
                try:
                    if init_value is None:
                        instance = typed_iterable_cls( i_type=str )
                    else:
                        instance = typed_iterable_cls( value_B, i_type=str )
                except Exception as err:
                    test_case.fail(
                        msg.valid_init_failed(
                            cls = typed_iterable_cls,
                            i_type = str,
                            init_value = init_value,
                            err = err,
                        )
                    )
                
                # ----- ASSERTIONS
                test_case.assertEqual( instance, builtin_reference,
                    msg.valid_init_unexpected_result(
                        cls = typed_iterable_cls,
                        i_type = str,
                        init_value = init_value,
                        result = instance,
                        builtin_ref = builtin_reference
                    )
                )

def initialisation_fails( 
        test_case: unittest.TestCase,
        classes: Iterable[ Type[TypedIterable_T] ],
        init_values: list,
        i_type: type | Any = str,
        expected_exception: Type[Exception] = _TypedIterError,
):
    """ Asserts that all given classes initialisation fails with _TypedIterError for all given init_values / type restriction

    Parameters
    ----------
    - **test_case**
        the TestCase class from which the function is called

    - **classes**
        iterable containing the typed iterable classes to run the test on

    - **init_values**
        test sample list generated from a TestSamples instance that will be used to initialise the instances

    - **i_type**
        the type restriction that will be given to initialise the instance,
        (so that we can check the instance fails with invalid i_type)
    
    - **expected_exception**
        the exception that should be raised in that scenario
    """
    
    for typed_iterable_cls in classes:

        with test_case.subTest( typed_iterable_cls=typed_iterable_cls ):

            for index, init_value in enumerate(init_values): 
                # ----- SET UP

                # to simplify handling 'generator' samples
                # (see 'extract_test_values' docstring)
                init_value, value_A, _ = _helpers.extract_test_values( 
                    init_values, index 
                )

                raised_exception = None

                # ----- TEST 
                try:
                    typed_iterable_cls( value_A, i_type=i_type )
                except Exception as err:
                    raised_exception = err

                # ----- ASSERTIONS
                test_case.assertIsInstance( 
                    raised_exception, expected_exception,
                    msg.invalid_init_handling_failed(
                        cls = typed_iterable_cls,
                        i_type = i_type,
                        init_value = init_value,
                        err = raised_exception,
                        expected_exception = expected_exception
                    )
                )