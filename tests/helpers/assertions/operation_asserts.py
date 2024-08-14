import unittest
from typing import Any, Type, Literal, Optional, Callable, Iterable

from typediter.types import TypedIterable_T
from typediter.classes import _FrozenTypedIter, _MutableTypedIter

from tests.helpers import msg, TestSamples
from . import _helpers

ExpectedResultPreset_T = Literal['Self', 'SelfClass', 'Builtin']
TestFunc_T = Callable[ [Iterable, Any], Any ]
StarArgsTestFunc_T = Callable[ [Iterable, list], Any ]

def operation_succeeds( 
        test_case: unittest.TestCase,
        classes: Iterable[ Type[TypedIterable_T] ],
        test_function: TestFunc_T,
        operation_values: list,
        expected_result_type: type | ExpectedResultPreset_T,
        star_args_test_function_variant: Optional[ StarArgsTestFunc_T ] = None,
):
    """ Asserts that a given operation succeeds with all those values

    (i) test instances generated are 'str' typed iterables

    we run the test_function with each individual values, 
    and if specified, we run the 'star_args_test_function_variant' 
    one time giving it all the values in a *args.
    to compare, we execute the same operation with the built-in and compare results.

    Parameters
    ----------
    - **test_case**
        the TestCase instance from which the function is called

    - **classes**
        iterable containing the typed iterable classes we have to test

    - **test_function**
        function performing the operation,
        takes an iterable instance (typed or built-in equivalent), 
        and an operation value

    - **star_args_test_function_variant** (optional)
        variation on the test_function using *args as operation value
        to test operations that allow multiple args.
        takes an iterable instance (typed or built-in equivalent),
        and the whole operation_values list.
        ( performs one operation with all the values as test )

    - **operation_values**
        test sample list generated from a TestSamples instance. 
        that will be given as second arg to the test_function
    
    - **expected_result_type**
        type or preset name, indicating the type of the value 
        that should be retrieved from the test_function
            - type:
                the expected result type

            - "Self":
                Test functions result have to be the same instance that the one 
                we gave to the test function

            - "SelfClass":
                Test functions result have to be an instance of the tested 
                typed iterable class
            
            - "Builtin":
                Test function result have to be an instance of 
                the built-in equivalent to the the tested typed iterable 
                class
    """
    local_samples = TestSamples( test_case )

    for typed_iterable_cls in classes:

        with test_case.subTest( typed_iterable_cls=typed_iterable_cls ):
            
            _one_value_operations_succeeds(
                test_case = test_case,
                typed_iterable_cls = typed_iterable_cls,
                test_function = test_function,
                operation_values = operation_values,
                expected_result_type = expected_result_type,
                local_samples = local_samples
            )

            if star_args_test_function_variant:
                _star_args_operation_succeeds(
                    test_case = test_case,
                    typed_iterable_cls = typed_iterable_cls,
                    star_args_test_function_variant = star_args_test_function_variant,
                    operation_values = operation_values,
                    expected_result_type = expected_result_type,
                    local_samples = local_samples
                )

# ---------- operation succeeds helpers ---------- 

def _one_value_operations_succeeds(
        test_case: unittest.TestCase,
        typed_iterable_cls: Type[TypedIterable_T],
        test_function: TestFunc_T,
        operation_values: list,
        expected_result_type: type | ExpectedResultPreset_T,
        local_samples: TestSamples
):
    """ Private helper for 'operation_succeeds' func, running 'test_function'.

    runs 'test_function' with each indiviudal operation value, and checking the 
    result against the same operation made on a built-in equivalent 
    and checking the result type.

    Parameters
    ----------
    - **test_case**
        the TestCase instance from which the function is called
    
    - **typed_iterable_cls**
        the typed iterable class currently tested
    
    - **test_function**
        function performing the operation,
        takes an iterable instance (typed or built-in equivalent), 
        and an operation value
    
    - **operation_values**
        test sample list generated from a TestSamples instance 
        that will be given as second arg to the test_function
    
    - **expected_result_type**
        type or preset name, indicating the type of the value 
        that should be retrieved from the test_function
            - type:
                the expected result type

            - "Self":
                Test functions result have to be the same instance that the one 
                we gave to the test function

            - "SelfClass":
                Test functions result have to be an instance of the tested 
                typed iterable class
            
            - "Builtin":
                Test function result have to be an instance of the built-in equivalent
                to the the tested typed iterable class
    
    - **local_samples**
        TestSamples instance
    """
    expected_type: type

    # getting the corresponding built-in equivalent
    builtin_reference_cls = _helpers.get_builtin_equivalent( typed_iterable_cls )
    
    # getting expected result type 
    # and whether the result should be the same instance as the base instance
    expected_type, expects_self_result = _get_expected_result_specifications(
        expected_result_type = expected_result_type,
        typed_iterable_cls = typed_iterable_cls,
        builtin_reference_cls = builtin_reference_cls
    )

    for index, operation_value in enumerate(operation_values):
        # ---- SETUP
        
        # to simplify handling 'generator' samples
        # (see 'extract_test_values' docstring)
        operation_value, value_A, value_B = _helpers.extract_test_values(
            operation_values, index
        )

        builtin_reference, *_ = local_samples.builtin_iterables(
            classes = ( builtin_reference_cls, ),
            items_type = str,
            init_value_variant = 'BASE'
        )

        typed_iterable, *_ = local_samples.typed_iterables(
            classes = ( typed_iterable_cls, ),
            items_type = str,
            init_value_variant = 'BASE'
        )

        reference_result = test_function( builtin_reference, value_A )

        # ---- TEST
                
        try:
            result = test_function( typed_iterable, value_B )
        except Exception as err:
            test_case.fail( 
                msg.valid_operation_failed(
                    operation_name = test_function.__name__,
                    inst = typed_iterable,
                    operation_value = operation_value,
                    err = err
                )
            )
        
        # ---- ASSERTIONS
        _assert_result_is_valid(
            test_case = test_case,
            typed_iterable_cls = typed_iterable_cls,
            operation_name = test_function.__name__,
            operation_value = operation_value,
            expected_type = expected_type,
            expects_self_result = expects_self_result,
            original_instance = typed_iterable,
            result = result,
            reference_result = reference_result
        )

def _star_args_operation_succeeds(
        test_case: unittest.TestCase,
        typed_iterable_cls:  Type[TypedIterable_T],
        star_args_test_function_variant: StarArgsTestFunc_T,
        operation_values: list,
        expected_result_type: type | ExpectedResultPreset_T,
        local_samples: TestSamples
):
    """ Private helper for 'operation_succeeds' func, running 'star_args_test_function_variant'.

    runs 'star_args_test_function_variant' one time, giving it all the operation values, and checking the 
    result against the same operation made on a built-in equivalent 
    and checking the result type.
    
    Parameters
    ----------
    - **test_case**
        the TestCase instance from which the function is called
    
    - **typed_iterable_cls**
        the typed iterable class currently tested
    
    - **star_args_test_function_variant**
        function performing the operation,
        takes an iterable instance (typed or built-in equivalent), 
        and a list of operation values
    
    - **operation_values**
        test sample list generated from a TestSamples instance 
        that will be given as second arg to the test_function
    
    - **expected_result_type**
        type or preset name, indicating the type of the value 
        that should be retrieved from the test_function
            - type:
                the expected result type

            - "Self":
                Test functions result have to be the same instance that the one 
                we gave to the test function

            - "SelfClass":
                Test functions result have to be an instance of the tested 
                typed iterable class
            
            - "Builtin":
                Test function result have to be an instance of the built-in equivalent
                to the the tested typed iterable class
    
    - **local_samples**
        TestSamples instance
    """
    
    expected_type: type

    # getting the corresponding built-in equivalent
    builtin_reference_cls = _helpers.get_builtin_equivalent( typed_iterable_cls )
    
    # setting expected operation result type
    # expected_result_type is a preset name, or directly a type
    expected_type, expects_self_result = _get_expected_result_specifications(
        expected_result_type = expected_result_type,
        typed_iterable_cls = typed_iterable_cls,
        builtin_reference_cls = builtin_reference_cls
    )

    # SETUP 

    # to simplify handling 'generator' samples
    # (see 'extract_star_args_test_values' docstring)
    operation_values, values_A, values_B = _helpers.extract_star_args_test_values( operation_values )
    
    builtin_reference, *_ = local_samples.builtin_iterables(
        classes = ( builtin_reference_cls, ),
        items_type = str,
        init_value_variant = 'BASE'
    )

    typed_iterable, *_ = local_samples.typed_iterables(
        classes = ( typed_iterable_cls, ),
        items_type = str,
        init_value_variant = 'BASE'
    )

    reference_result = star_args_test_function_variant( builtin_reference, values_A )

    # ---- TEST
                
    try:
        result = star_args_test_function_variant( typed_iterable, values_B )
    except Exception as err:
        test_case.fail( 
            msg.valid_operation_failed(
                operation_name = star_args_test_function_variant.__name__,
                inst = typed_iterable,
                operation_value = operation_values,
                err = err,
                is_multiple_operation_values = True
            )
        )

    # ---- ASSERTIONS
    _assert_result_is_valid(
        test_case = test_case,
        typed_iterable_cls = typed_iterable_cls,
        operation_name = star_args_test_function_variant.__name__,
        operation_value = operation_values,
        expected_type = expected_type,
        expects_self_result = expects_self_result,
        original_instance = typed_iterable,
        result = result,
        reference_result = reference_result,
        is_multiple_operation_values = True
    )

def _get_expected_result_specifications(
    expected_result_type: type | ExpectedResultPreset_T,
    typed_iterable_cls: type,
    builtin_reference_cls: type
) -> tuple[type, bool]:
    """ Private helper for 'operation_succeeds' func, returning type specification for the operation result
    
    Returns the expected result type and whether the result should be the same instance as the base instance
    based on the value of 'expected_result_type'.

    Parameters
    ----------
    - **expected_result_type**
        the expected returned result type, or a preset name:
            - type:
                result should be an instance of that type
            - "Self":
                result should be the same instance as the base instance
            - "SelfClass":
                result should be a new instance of the same class as the base instance
            - "Builtin":
                result should be a new instance of the built-in equivalent to the base instance's class
    
    - **typed_iterable_cls**
        type of the base instance on which the operation is tested

    - **builtin_reference_cls**
        built-in equivalent to the current 'typed_iterable_cls'

    Returns
    -------
    Tuple of 2 values:
        - a type, which has to be an exact match with the result's type
        - a bool, indicating whether the result should be the same instance as the base instance
    """
    expected_type: type

    # what will be the result type ?
    if expected_result_type == 'Self' or expected_result_type == 'SelfClass':
        expected_type = typed_iterable_cls
    elif expected_result_type == 'Builtin':
        expected_type = builtin_reference_cls
    else:
        expected_type = expected_result_type
    
    # are we expecting the same instance ?
    expects_self_result = expected_result_type == 'Self'

    return expected_type, expects_self_result

def _assert_result_is_valid(
        test_case: unittest.TestCase,
        typed_iterable_cls: Type[TypedIterable_T],
        operation_name: str,
        operation_value: Any,
        expected_type: type,
        expects_self_result: bool,
        original_instance: TypedIterable_T,
        result: Any,
        reference_result: Any,
        is_multiple_operation_values: bool = False,

):
    """ Private helper for 'operation_succeeds' func, making the assertions on the result

    checks the operation result against the expected type specifications, and the reference result
    to verify that the operation was executed succefully,
    and then checks resulting typed iterable instances to verify that no incompatible items were inserted. 

    Parameters
    ----------
    - **test_case**
        the TestCase instance from which the function is called

    - **typed_iterable_cls**
        the typed iterable class currently tested

    - **operation_name**
        name of the tested operation
    
    - **operation_value**
        the value the operation was performed with

    - **expected_type**
        the exact type expected for the result

    - **expects_self_result**
        whether we expect the result of the operation to be the same instance as the original instance
    
    - **original_instance**
        the typed iterable instance used as the base for the operation

    - **result**
        result returned by the test function,
        given the original instance and the operation value
    
    - **reference_result**
        result returned by the test function,
        given the built-in equivalent to the original instance, and the operation value

    - **is_multiple_operation_values**
        wether the test_function is 'star_args_test_function_variant'
        ( so was it a *args operation )
        ( message generation handled differently )
    """
    # check for type strict equality 
    # to avoid confusing built-in and typed instances
    is_valid = (
        ( result == reference_result )
        and ( type(result) is expected_type )
    )

    # 2 additionnal cases:
    # - we want the operation to return self
    # - we want the operation to return a new instance
    is_self = result is original_instance
    
    if expects_self_result:
        is_valid = is_valid and is_self
    else:
        is_valid = is_valid and not is_self
    
    # assertion
    test_case.assertTrue( is_valid,
        msg.valid_operation_unexpected_result(
            operation_name = operation_name,
            cls = typed_iterable_cls,
            i_type = str,
            operation_value = operation_value,
            expects_self_result = expects_self_result,
            result_is_self = is_self,
            expected_result_type = expected_type,
            result = result,
            builtin_ref_result = reference_result,
            is_multiple_operation_values = is_multiple_operation_values
        )
    )

    # checking if the operation has introduced a badly typed items
    _assert_no_invalid_items_were_inserted(
        test_case = test_case,
        instance = original_instance,
        operation_name = operation_name,
        operation_value = operation_value,
        is_multiple_operation_values = is_multiple_operation_values
    )
    if isinstance( result, (_FrozenTypedIter, _MutableTypedIter) ) and not is_self:
        # if result is a typed iterable different than the original instance
        _assert_no_invalid_items_were_inserted(
            test_case = test_case,
            instance = result, # type: ignore [arg-type]
            operation_name = operation_name,
            operation_value = operation_value,
            is_multiple_operation_values = is_multiple_operation_values
        )

def _assert_no_invalid_items_were_inserted(
    test_case: unittest.TestCase,
    instance: TypedIterable_T,
    operation_name: str,
    operation_value: Any,
    is_multiple_operation_values: bool = False,
):
    """ Private helper for 'operation_succeeds' func, asserting that a typed iterable instance has no incompatible items

    Parameters
    ----------
    - **test_case**
        the TestCase instance from which the function is called

    - **instance**
        the typed iterable instance we are checking
    
    - **operation_name**
        name of the tested operation
    
    - **operation_value**
        the value the operation was performed with

    - **is_multiple_operation_values**
        wether the test_function is 'star_args_test_function_variant'
        ( so was it a *args operation )
    """
    i_type = instance.i_type

    for item in instance:
        test_case.assertTrue( isinstance( item, i_type ),
            msg.operation_inserted_incompatible_item(
                operation_name = operation_name,
                cls = type( instance ),
                i_type = str,
                operation_value = operation_value,
                invalid_item = item,
                is_multiple_operation_values = is_multiple_operation_values
            )
        )
    


def operation_fails(
        test_case: unittest.TestCase,
        classes: Iterable[Type],
        test_function: TestFunc_T,
        operation_values: list,
        expected_exception: Type[Exception],
        star_args_test_function_variant: Optional[ StarArgsTestFunc_T ] = None,
):
    """ Asserts that a given operation fails with all those values

    (i) test instances generated are 'str' typed iterables

    we run the test_function with each individual values, 
    and if specified, we run the 'star_args_test_function_variant' 
    one time giving it all the values in a *args
    if one operation doesn't fail for a value, we fail the test

    Parameters
    ----------
    - **test_case**
        the TestCase instance from which the function is called

    - **classes**
        iterable containing the typed iterable classes we have to test

    - **test_function**
        function performing the operation,
        takes an iterable instance (typed or built-in equivalent), 
        and an operation value

    - **star_args_test_function_variant** (optional)
        variation on the test_function using *args as operation value
        to test operations that allow multiple args.
        takes an iterable instance (typed or built-in equivalent),
        and the whole operation_values list.
        ( performs one operation with all the values as test )

    - **operation_values**
        test sample list generated from a TestSamples instance 
        that will be given as second arg to the test_function

    - **expected_exception**
        Exception class that is expected to be raised
        ( if another exception is raised we fail the test )
    """
    
    local_samples = TestSamples( test_case )

    for typed_iterable_cls in classes:

        with test_case.subTest( typed_iterable_cls=typed_iterable_cls ):
            
            _one_value_operations_fails(
                test_case = test_case,
                typed_iterable_cls = typed_iterable_cls,
                test_function = test_function,
                operation_values = operation_values,
                expected_exception = expected_exception,
                local_samples = local_samples,
            )

            if star_args_test_function_variant:
                _star_args_operation_fails(
                    test_case = test_case,
                    typed_iterable_cls = typed_iterable_cls,
                    star_args_test_function_variant = star_args_test_function_variant,
                    operation_values = operation_values,
                    expected_exception = expected_exception,
                    local_samples = local_samples,
                )

# ---------- operation fails helpers ---------- 

def _one_value_operations_fails(
        test_case: unittest.TestCase,
        typed_iterable_cls: Type[TypedIterable_T],
        test_function: TestFunc_T,
        operation_values: list,
        expected_exception: Type[Exception],
        local_samples: TestSamples,
):
    """ Private helper for 'operation_fails' func, running 'test_function'.

    runs 'test_function' with each indiviudal operation value, 
    if an operation doesn't raise the expected exception for a value, we fail the test

    Parameters
    ----------
    - **test_case**
        the TestCase instance from which the function is called
    
    - **typed_iterable_cls**
        the typed iterable class currently tested
    
    - **test_function**
        function performing the operation,
        takes an iterable instance (typed or built-in equivalent), 
        and an operation value
    
    - **operation_values**
        test sample list generated from a TestSamples instance 
        that will be given as second arg to the test_function
    
    - **expected_exception**
        Exception class that is expected to be raised
        ( if another exception is raised we fail the test )
    
    - **local_samples**
        TestSamples instance
    """
    
    for index, operation_value in enumerate(operation_values):
        # ---- SETUP

        # to simplify handling 'generator' samples
        # (see 'extract_test_values' docstring)
        operation_value, value_A, _ = _helpers.extract_test_values(
            operation_values, index
        )

        typed_iterable, *_ = local_samples.typed_iterables(
            classes = ( typed_iterable_cls, ),
            items_type = str,
            init_value_variant = 'BASE'
        )

        raised_exception = None

        # ---- TESTS
        try:
            test_function( typed_iterable, value_A )
        except Exception as err:
            raised_exception = err
        
        # ---- ASSERTIONS
        test_case.assertIsInstance( 
            raised_exception, expected_exception,
            msg.invalid_operation_handling_failed(
                operation_name = test_function.__name__,
                cls = typed_iterable_cls,
                i_type = str,
                operation_value = operation_value,
                err = raised_exception,
                expected_exception = expected_exception
            )
        )

def _star_args_operation_fails(
        test_case: unittest.TestCase,
        typed_iterable_cls: Type[TypedIterable_T],
        star_args_test_function_variant: StarArgsTestFunc_T,
        operation_values: list,
        expected_exception: Type[Exception],
        local_samples: TestSamples,
):
    """ Private helper for 'operation_fails' func, running 'star_args_test_function_variant'.

    runs 'star_args_test_function_variant' one time, giving it all the operation values, 
    if the operation doesn't raise the expected exception, we fail the test

    Parameters
    ----------
    - **test_case**
        the TestCase instance from which the function is called
    
    - **typed_iterable_cls**
        the typed iterable class currently tested
    
    - **star_args_test_function_variant**
        function performing the operation,
        takes an iterable instance (typed or built-in equivalent), 
        and a list of operation values
    
    - **operation_values**
        test sample list generated from a TestSamples instance 
        that will be given as second arg to the test_function
    
    - **expected_exception**
        Exception class that is expected to be raised
        ( if another exception is raised we fail the test )  
    
    - **local_samples**
        TestSamples instance
    """
    # ---- SETUP

    # to simplify handling 'generator' samples
    # (see 'extract_star_args_test_values' docstring)
    operation_values, values_A, _ = _helpers.extract_star_args_test_values( operation_values )

    typed_iterable, *_ = local_samples.typed_iterables(
        classes = ( typed_iterable_cls, ),
        items_type = str,
        init_value_variant = 'BASE'
    )

    raised_exception = None

    # ---- TESTS
    try:
        star_args_test_function_variant( typed_iterable, values_A )
    except Exception as err:
        raised_exception = err
    
    # ---- ASSERTIONS
    test_case.assertIsInstance( 
        raised_exception, expected_exception,
        msg.invalid_operation_handling_failed(
            operation_name = star_args_test_function_variant.__name__,
            cls = typed_iterable_cls,
            i_type = str,
            operation_value = operation_values,
            err = raised_exception,
            expected_exception = expected_exception,
            is_multiple_operation_values = True
        )
    )