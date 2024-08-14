import unittest
from typing import Any, Type, Iterable, Callable

from typediter import TypedTuple_lt
from typediter.utils import filter_items
from typediter.types import TypedIterable_T

from tests.helpers import msg
from . import _helpers


def filter_items_utility(
        test_case: unittest.TestCase,
        operation_values: list,
):
    """ Asserts that the filter_items utility function filters iterables correctly

    to check it we try to initialise a TypedTuple_lt instance with the result
    and if it doesn't fail we considered it worked
    
    Parameters
    ----------
    - **test_case**
        the TestCase class from which the function is called

    - **operation_values**
        test sample list generated from a TestSamples instance 
        that will be filtered by the utility function
    """

    with test_case.subTest():
        for index, operation_value in enumerate( operation_values ):
            # ----- SET UP

            # to simplify handling 'generator' samples
            # (see 'extract_test_values' docstring)
            operation_value, value_A, _ = _helpers.extract_test_values( 
                operation_values, index 
            )

            # ----- TEST
            try:
                str_items = filter_items( value_A, i_type=str )
                str_instance = TypedTuple_lt(
                    str_items,
                    i_type = str
                )
                # just to not show the value as 'unused'
                str_instance 

            except Exception as err:
                test_case.fail(
                    msg.valid_utility_operation_failed(
                        operation_name = 'filter_items',
                        operation_value = operation_value,
                        err = err,
                    )
                )

def typechecking_utility(
        test_case: unittest.TestCase,
        util_function: Callable,
        operation_values: list,
        expected_result: Any,
):
    """ Asserts that the 'util_function' returns the expected result
    
    Parameters
    ----------
    - **test_case**
        the TestCase class from which the function is called

    - **util_function**
        utility function tested, 
        taking one arg, and returning one value 

    - **operation_values**
        test sample list generated from a TestSamples instance 
        that will be given to the utility function

    - **expected_result**
        common expected result for all given operation values
    """
    
    with test_case.subTest():

        for index, operation_value in enumerate( operation_values ):
            # ----- SET UP

            # to simplify handling 'generator' samples
            # (see 'extract_test_values' docstring)
            operation_value, value_A, _ = _helpers.extract_test_values( 
                operation_values, index 
            )

            # ----- TEST
            try:
                result = util_function( value_A )
            except Exception as err:
                test_case.fail(
                    msg.valid_utility_operation_failed(
                        operation_name = util_function.__name__,
                        operation_value = operation_value,
                        err = err,
                    )
                )

            # ----- ASSERTIONS
            is_valid = (
                (result == expected_result)
                and ( type(result) is type(expected_result) )
            )

            test_case.assertTrue(
                is_valid,
                msg.valid_utility_operation_unexpected_result(
                    operation_name = util_function.__name__,
                    operation_value = operation_value,
                    result = result,
                    expected_result = expected_result
                )
            )


# Converter utilities tests

def typed_iterable_converter_utility_succeeds(
        test_case: unittest.TestCase,
        classes:  Iterable[ Type[TypedIterable_T] ],
        converter_func_getter: Callable,
        operation_values: list,
):
    """ Asserts that utils returning a function converting iterable to typed iterable works with those values,

    to check if the converter succeded we compare the returned value 
    to an instance of the expected output manually created 
    
    Parameters
    ----------
    - **test_case**
        the TestCase class from which the function is called

    - **classes**
        iterable containing the typed iterable classes to run the test on
    
    - **converter_func_getter**
        utility function tested, 
        takes a typediterable class and a type, returns a converter function

    - **operation_values**
        test sample list generated from a TestSamples instance 
        that will be given as second arg to the test_function
    """
    with test_case.subTest():
        for typed_iterable_cls in classes:

            for index, operation_value in enumerate( operation_values ):
                # ----- SET UP

                # to simplify handling 'generator' samples
                # (see 'extract_test_values' docstring)
                operation_value, value_A, value_B = _helpers.extract_test_values( 
                    operation_values, index 
                )

                expected_result = typed_iterable_cls( value_A, i_type=str )

                # ----- TEST
                try:
                    converter = converter_func_getter( typed_iterable_cls, i_type=str )
                    result = converter( value_B )
                except Exception as err:
                    test_case.fail(
                        msg.valid_converter_utility_operation_failed(
                            operation_name = converter_func_getter.__name__,
                            operation_value = operation_value,
                            converting_to = typed_iterable_cls,
                            i_type = str,
                            err = err,
                        )
                    )
                
                # ----- ASSERTIONS
                # check for type strict equality 
                # to avoid confusing built-in and typed instances
                is_valid = (
                    ( result == expected_result ) and
                    ( type(result) is type(expected_result) )
                )

                test_case.assertTrue( is_valid,
                    msg.valid_converter_utility_operation_unexpected_result(
                        operation_name = converter_func_getter.__name__,
                        operation_value = operation_value,
                        converting_to = typed_iterable_cls,
                        i_type = str,
                        result = result,
                        expected_result = expected_result,
                    )
                )

def typed_iterable_converter_utility_fails(
        test_case: unittest.TestCase,
        classes:  Iterable[ Type[TypedIterable_T] ],
        converter_func_getter: Callable,
        expected_exception: Type[Exception],
        operation_values: list,
        i_type: type | Any = str
):
    """ Asserts that utils returning a function converting iterable to typed iterable fails with those values
    
    Parameters
    ----------
    - **test_case**
        the TestCase class from which the function is called

    - **classes**
        iterable containing the typed iterable classes to run the test on
    
    - **converter_func_getter**
        utility function tested, 
        takes a typediterable class and a type, returns a converter function

    - **expected_exception**
        exception class expected to be raised

    - **operation_values**
        test sample list generated from a TestSamples instance 
        that will be given as second arg to the test_function
    
    - **i_type**
        the type restriction applied to the converter
        (so that we can check that the conversion fails with invalid i_type)
    """
    
    with test_case.subTest():
        for typed_iterable_cls in classes:
            
            for index, operation_value in enumerate( operation_values ):
                # ----- SET UP

                # to simplify handling 'generator' samples
                # (see 'extract_test_values' docstring)
                operation_value, value_A, _ = _helpers.extract_test_values( 
                    operation_values, index 
                )
                
                raised_exception = None

                # ----- TEST
                try:
                    converter = converter_func_getter( typed_iterable_cls, i_type=i_type )
                    converter( value_A )
                except Exception as err:
                    raised_exception = err

                # ----- ASSERTIONS
                test_case.assertIsInstance(
                    raised_exception, expected_exception,
                    msg.invalid_converter_utility_operation_handling_failed(
                        operation_name = converter_func_getter.__name__,
                        operation_value = operation_value,
                        converting_to = typed_iterable_cls,
                        i_type = i_type,
                        err = raised_exception,
                        expected_exception = expected_exception,
                    )
                )
        

def frozen_builtin_converter_utility_succeeds(
        test_case: unittest.TestCase,
        converter_func_getter: Callable,
        operation_values: list,
        expected_result_type: Type[ tuple | frozenset ]
):
    """ Asserts that utils returning a function converting iterable to type-safe frozen builtin iterable works with those values,

    to check if the converter succeded we compare the returned value 
    to an instance of the expected output manually created 
    
    Parameters
    ----------
    - **test_case**
        the TestCase class from which the function is called

    - **converter_func_getter**
        utility function tested, 
        takes a type, returns a converter function

    - **operation_values**
        test sample list generated from a TestSamples instance 
        that will be given as second arg to the test_function
    
    - **expected_result_type**
        expected class (tuple or frozenset) of the value returned 
        by the converter function
    """

    with test_case.subTest():
        for index, operation_value in enumerate( operation_values ):
            # ----- SET UP

            # to simplify handling 'generator' samples
            # (see 'extract_test_values' docstring)
            operation_value, value_A, value_B = _helpers.extract_test_values( 
                operation_values, index 
            )

            expected_result = expected_result_type( value_A )

            # ----- TEST
            try:
                converter = converter_func_getter( str )
                result = converter( value_B )
            except Exception as err:
                test_case.fail(
                    msg.valid_converter_utility_operation_failed(
                        operation_name = converter_func_getter.__name__,
                        operation_value = operation_value,
                        converting_to = expected_result_type,
                        i_type = str,
                        err = err,
                    )
                )
            
            # ----- ASSERTIONS
            # check for type strict equality 
            # to avoid confusing built-in and typed instances
            is_valid = (
                ( result == expected_result ) and
                ( type(result) is type(expected_result) )
            )

            test_case.assertTrue( is_valid,
                msg.valid_converter_utility_operation_unexpected_result(
                    operation_name = converter_func_getter.__name__,
                    operation_value = operation_value,
                    converting_to = expected_result_type,
                    i_type = str,
                    result = result,
                    expected_result = expected_result,
                )
            )

def frozen_builtin_converter_utility_fails(
        test_case: unittest.TestCase,
        converter_func_getter: Callable,
        expected_exception: Type[Exception],
        operation_values: list,
        expected_result_type: Type[ tuple | frozenset ],
        i_type: type | Any = str
):
    """ Asserts that utils returning a function converting iterable to type-safe frozen builtin iterable fails with those values
    
    Parameters
    ----------
    - **test_case**
        the TestCase class from which the function is called
    
    - **converter_func_getter**
        utility function tested, 
        takes a type, returns a converter function

    - **expected_exception**
        exception class expected to be raised

    - **operation_values**
        test sample list generated from a TestSamples instance 
        that will be given as second arg to the test_function
    
    - **expected_result_type**
        expected class (tuple or frozenset) of the value returned 
        by the converter function
        (just there for failure logging)

    - **i_type**
        the type restriction applied to the converter
        (so that we can check that the conversion fails with invalid i_type)
    """
    with test_case.subTest():
        for index, operation_value in enumerate( operation_values ):
            # ----- SET UP

            # to simplify handling 'generator' samples
            # (see 'extract_test_values' docstring)
            operation_value, value_A, _ = _helpers.extract_test_values( 
                operation_values, index 
            )
            
            raised_exception = None

            # ----- TEST
            try:
                converter = converter_func_getter( i_type )
                converter( value_A )
            except Exception as err:
                raised_exception = err

            # ----- ASSERTIONS
            test_case.assertIsInstance(
                raised_exception, expected_exception,
                msg.invalid_converter_utility_operation_handling_failed(
                    operation_name = converter_func_getter.__name__,
                    operation_value = operation_value,
                    converting_to = expected_result_type,
                    i_type = i_type,
                    err = raised_exception,
                    expected_exception = expected_exception
                )
            )