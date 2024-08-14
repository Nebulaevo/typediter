import unittest

from typediter.exceptions import _TypedIterError
from typediter import  TypedSet, TypedSet_lt

from tests.helpers import TestSamples, assertions


class TypedSetsTests( unittest.TestCase ):
    """ Tests typed sets overridden methods and dunders

    (i) except for methods that are already tested
    in the 'CommonSetTests' test case.

    Tested Classes
    --------------
    - TypedSet_lt
    - TypedSet

    Tested
    ------
    - (method) add
    - (method) symmetric_difference_update
    - (method) update
    - (dunnder) ior
    - (dunnder) ixor
    """
    
    def __init__( self, *args, **kwargs ):
        """ Setting up common ressources for tests """
        self.samples = TestSamples( self )
        super().__init__( *args, **kwargs )

    # -------------------- Tested operations --------------------
    
    @staticmethod
    def add( instance:set, value ):
        instance.add(value)
        return instance

    @staticmethod
    def symmetric_difference_update( instance:set, value ):
        instance.symmetric_difference_update(value)
        return instance

    @staticmethod
    def update( instance:set, value ):
        instance.update(value)
        return instance

    @staticmethod
    def update_multiple( instance:set, value ):
        instance.update(*value)
        return instance

    @staticmethod
    def ior_operation( instance:set, value ):
        instance |= value
        return instance
    
    @staticmethod
    def ixor_operation( instance:set, value ):
        instance ^= value
        return instance
    
    # -----------------------------------------------
    # -------------------- TESTS --------------------
    # -----------------------------------------------

    # -----------------------------------------------
    # Test methods

    def test_set_add_method( self ):
        """ Tests set 'add' method
        
        (i) all base instances the tests are run on are 'str' typed

        Light and Complete versions
        ---------------------------
        (i) operation directly modifying original instance,
        so operation value should be type-checked for both
        light and complete versions
        
        - should work only with compatible items
        - should fail with incompatible items
        - test function should return the original instance
        """
        assertions.operation_succeeds(
            test_case = self,
            classes = (TypedSet_lt, TypedSet),
            test_function = self.add,
            operation_values = self.samples.items( str_items=True ),
            expected_result_type = 'Self'
        )

        assertions.operation_fails(
            test_case = self,
            classes = (TypedSet_lt, TypedSet),
            test_function = self.add,
            operation_values = self.samples.items( str_items=False ),
            expected_exception = _TypedIterError
        )
    
    def test_set_symmetric_difference_update_method( self ):
        """ Tests set 'symmetric_difference_update' method
        
        (i) all base instances the tests are run on are 'str' typed

        Light and Complete versions
        ---------------------------
        (i) operation directly modifying original instance,
        so operation value should be type-checked for both
        light and complete versions
        
        - should work only with compatible iterables
        - should fail with incompatible iterables
        - test function should return the original instance
        """
        assertions.operation_succeeds(
            test_case = self,
            classes = (TypedSet_lt, TypedSet),
            test_function = self.symmetric_difference_update,
            operation_values = self.samples.typed_and_builtin_iterables_preset(
                preset = 'ITERABLE',
                items_type = str,
                init_value_variant = 'OPERATION',
            ),
            expected_result_type = 'Self'
        )
        
        assertions.operation_fails(
            test_case = self,
            classes = (TypedSet_lt, TypedSet),
            test_function = self.symmetric_difference_update,
            operation_values = self.samples.all_int_and_mixed_iterables_variations(
                preset = 'ITERABLE',
            ),
            expected_exception = _TypedIterError
        )
    
    def test_set_update_method( self ):
        """ Tests set 'update' method
        
        (i) all base instances the tests are run on are 'str' typed

        Light and Complete versions
        ---------------------------
        (i) operation directly modifying original instance,
        so operation value should be type-checked for both
        light and complete versions
        
        - should work only with compatible iterables
        - should fail with incompatible iterables
        - test function should return the original instance
        """
        assertions.operation_succeeds(
            test_case = self,
            classes = (TypedSet_lt, TypedSet),
            test_function = self.update,
            star_args_test_function_variant = self.update_multiple,
            operation_values = self.samples.typed_and_builtin_iterables_preset(
                preset = 'ITERABLE',
                items_type = str,
                init_value_variant = 'OPERATION',
            ),
            expected_result_type = 'Self'
        )
        
        assertions.operation_fails(
            test_case = self,
            classes = (TypedSet_lt, TypedSet),
            test_function = self.update,
            star_args_test_function_variant = self.update_multiple,
            operation_values = self.samples.all_int_and_mixed_iterables_variations(
                preset = 'ITERABLE',
            ),
            expected_exception = _TypedIterError
        )
    
    # -----------------------------------------------
    # Test dunders

    def test_set_operation_ior( self ):
        """ Tests set 'ior' dunder method
        
        (i) all base instances the tests are run on are 'str' typed

        Light and Complete versions
        ---------------------------
        (i) operation directly modifying original instance,
        so operation value should be type-checked for both
        light and complete versions
        
        - should work only with compatible set/frozenset
        - should fail with incompatible set/frozenset
        - test function should return the original instance
        """
        assertions.operation_succeeds(
            test_case = self,
            classes = (TypedSet_lt, TypedSet),
            test_function = self.ior_operation,
            operation_values = self.samples.typed_and_builtin_iterables_preset(
                preset = 'SET',
                items_type = str,
                init_value_variant = 'OPERATION',
            ),
            expected_result_type = 'Self'
        )
        
        assertions.operation_fails(
            test_case = self,
            classes = (TypedSet_lt, TypedSet),
            test_function = self.ior_operation,
            operation_values = self.samples.all_int_and_mixed_iterables_variations(
                preset = 'SET',
            ),
            expected_exception = _TypedIterError
        )
    
    def test_set_operation_ixor( self ):
        """ Tests set 'ixor' dunder method
        
        (i) all base instances the tests are run on are 'str' typed

        Light and Complete versions
        ---------------------------
        (i) operation directly modifying original instance,
        so operation value should be type-checked for both
        light and complete versions
        
        - should work only with compatible set/frozenset
        - should fail with incompatible set/frozenset
        - test function should return the original instance
        """
        assertions.operation_succeeds(
            test_case = self,
            classes = (TypedSet_lt, TypedSet),
            test_function = self.ixor_operation,
            operation_values = self.samples.typed_and_builtin_iterables_preset(
                preset = 'SET',
                items_type = str,
                init_value_variant = 'OPERATION',
            ),
            expected_result_type = 'Self'
        )
        
        assertions.operation_fails(
            test_case = self,
            classes = (TypedSet_lt, TypedSet),
            test_function = self.ixor_operation,
            operation_values = self.samples.all_int_and_mixed_iterables_variations(
                preset = 'SET',
            ),
            expected_exception = _TypedIterError
        )