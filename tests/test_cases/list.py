import unittest

from typediter.exceptions import _TypedIterError, IterableExpectedError
from typediter import TypedList, TypedList_lt 

from tests.helpers import TestSamples, assertions

class TypedListTests( unittest.TestCase ):
    """ Tests typed lists overridden methods and dunders

    (i) except for methods that are already tested
    in the 'CommonListTupleTests' test case.

    Tested Classes
    --------------
    - TypedList_lt
    - TypedList

    Tested
    ------
    - (method) insert
    - (method) append
    - (method) extend
    - (dunnder) setitem
    - (dunnder) iadd
    """

    def __init__( self, *args, **kwargs ):
        """ Setting up common ressources for tests """  
        self.samples = TestSamples( self )
        super().__init__( *args, **kwargs )

    # -------------------- Tested operations --------------------

    @staticmethod
    def insert( instance:list, value ):
        instance.insert(1, value)
        return instance

    @staticmethod
    def append( instance:list, value ):
        instance.append(value)
        return instance

    @staticmethod
    def extend( instance:list, value ):
        instance.extend( value )
        return instance
    

    @staticmethod
    def setitem_operation_with_index( instance:list, value ):
        instance[0] = value
        return instance
    
    @staticmethod
    def setitem_operation_with_slice( instance:list, value ):
        instance[0:2] = value
        return instance

    @staticmethod
    def iadd_operation( instance:list, value ):
        instance += value
        return instance

    # -----------------------------------------------
    # -------------------- TESTS --------------------
    # -----------------------------------------------

    # -----------------------------------------------
    # Test methods

    def test_list_insert_method( self ):
        """ Tests list 'insert' method
        
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
            classes = (TypedList_lt, TypedList),
            test_function = self.insert,
            operation_values = self.samples.items( str_items=True ),
            expected_result_type = 'Self',
        )

        assertions.operation_fails(
            test_case = self,
            classes = (TypedList_lt, TypedList),
            test_function = self.insert,
            operation_values = self.samples.items( str_items=False ),
            expected_exception = _TypedIterError
        )

    def test_list_append_method( self ):
        """ Tests list 'append' method
        
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
            classes = (TypedList_lt, TypedList),
            test_function = self.append,
            operation_values = self.samples.items( str_items=True ),
            expected_result_type = 'Self',
        )

        assertions.operation_fails(
            test_case = self,
            classes = (TypedList_lt, TypedList),
            test_function = self.append,
            operation_values = self.samples.items( str_items=False ),
            expected_exception = _TypedIterError
        )

    def test_list_extend_method( self ):
        """ Tests list 'extend' method
        
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
            classes = (TypedList_lt, TypedList),
            test_function = self.extend,
            operation_values = self.samples.typed_and_builtin_iterables_preset(
                preset = 'ITERABLE',
                items_type = str,
                init_value_variant = 'OPERATION',
            ),
            expected_result_type = 'Self',
        )

        assertions.operation_fails(
            test_case = self,
            classes = (TypedList_lt, TypedList),
            test_function = self.extend,
            operation_values = self.samples.all_int_and_mixed_iterables_variations(
                preset = 'ITERABLE',
            ),
            expected_exception = _TypedIterError
        )

    # -----------------------------------------------
    # Test dunders

    def test_list_operation_setitem_with_index( self ):
        """ Tests list 'setitem' dunder method: (index, item) overload

        'setitem' dunder declares 2 overloads:
        - __setitem__( index, item ) -> None
        - __setitem__( slice, iterable ) -> None
        
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
            classes = (TypedList_lt, TypedList),
            test_function = self.setitem_operation_with_index,
            operation_values = self.samples.items( str_items=True ),
            expected_result_type = 'Self',
        )

        assertions.operation_fails(
            test_case = self,
            classes = (TypedList_lt, TypedList),
            test_function = self.setitem_operation_with_index,
            operation_values = self.samples.items( str_items=False ),
            expected_exception = _TypedIterError
        )

    def test_list_operation_setitem_with_slice( self ):
        """ Tests list 'setitem' dunder method: (slice, iterable) overload

        'setitem' dunder declares 2 overloads:
        - __setitem__( index, item )
        - __setitem__( slice, iterable )
        
        (i) all base instances the tests are run on are 'str' typed
        
        Light and Complete versions
        ---------------------------
        (i) operation directly modifying original instance,
        so operation value should be type-checked for both
        light and complete versions
        
        - should work only with compatible iterables
        - should fail with incompatible iterables
        - test function should return the original instance
        - should fail with 'IterableExpectedError' if given a slice and a non-iterable value.
            The other way around, 
            giving an iterable value to an index key is technically valid,
            if it's a list containing iterable items
        """
        assertions.operation_succeeds(
            test_case = self,
            classes = (TypedList_lt, TypedList),
            test_function = self.setitem_operation_with_slice,
            operation_values = self.samples.typed_and_builtin_iterables_preset(
                preset = 'ITERABLE',
                items_type = str,
                init_value_variant = 'OPERATION',
            ),
            expected_result_type = 'Self',
        )

        assertions.operation_fails(
            test_case = self,
            classes = (TypedList_lt, TypedList),
            test_function = self.setitem_operation_with_slice,
            operation_values = self.samples.all_int_and_mixed_iterables_variations(
                preset = 'ITERABLE',
            ),
            expected_exception = _TypedIterError
        )

        # check with invalid overload
        # -> Non iterable given to slice 'setitem' should raise a IterableExpectedError
        assertions.operation_fails(
            test_case = self,
            classes = (TypedList_lt, TypedList),
            test_function = self.setitem_operation_with_slice,
            operation_values = self.samples.items( str_items=False ), # because str is iterable so valid
            expected_exception = IterableExpectedError
        )

    def test_list_operation_iadd( self ):
        """ Tests list 'iadd' dunder method
        
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
            classes = (TypedList_lt, TypedList),
            test_function = self.iadd_operation,
            operation_values = self.samples.typed_and_builtin_iterables_preset(
                preset = 'ITERABLE',
                items_type = str,
                init_value_variant = 'OPERATION',
            ),
            expected_result_type = 'Self',
        )

        assertions.operation_fails(
            test_case = self,
            classes = (TypedList_lt, TypedList),
            test_function = self.iadd_operation,
            operation_values = self.samples.all_int_and_mixed_iterables_variations( 
                preset = 'ITERABLE',
            ),
            expected_exception = _TypedIterError
        )