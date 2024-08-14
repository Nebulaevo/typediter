import unittest
from typing import Iterable

from typediter.exceptions import _TypedIterError
from typediter import  (
    TypedSet, TypedSet_lt,
    TypedFrozenset, TypedFrozenset_lt, 
)

from tests.helpers import TestSamples, assertions

class CommonSetTests( unittest.TestCase ):
    """ Tests all common operations between typed sets and frozensets

    (i) this includes all overridden methods for the typed frozensets

    Tested Classes
    --------------
    - TypedSet_lt
    - TypedSet
    - TypedFrozenset_lt
    - TypedFrozenset

    Tested
    ------
    - (method) difference
    - (method) intersection
    - (method) symmetric_difference
    - (method) union
    - (dunnder) sub
    - (dunnder) and
    - (dunnder) or
    - (dunnder) xor
    """
    
    def __init__( self, *args, **kwargs ):
        """ Setting up common ressources for tests """   
        self.samples = TestSamples( self )
        super().__init__( *args, **kwargs )

    # -------------------- Tested operations --------------------
    
    @staticmethod
    def difference( instance:set|frozenset, value ):
        return instance.difference(value)
    
    @staticmethod
    def difference_multiple_args( instance:set|frozenset, value: Iterable ):
        return instance.difference(*value)

    @staticmethod
    def intersection( instance:set|frozenset, value ):
        return instance.intersection(value)
    
    @staticmethod
    def intersection_multiple_args( instance:set|frozenset, value: Iterable ):
        return instance.intersection(*value)
    
    @staticmethod
    def symmetric_difference( instance:set|frozenset, value ):
        return instance.symmetric_difference(value)
    
    @staticmethod
    def union( instance:set|frozenset, value ):
        return instance.union(value)
    
    @staticmethod
    def union_multiple_args( instance:set|frozenset, value: Iterable ):
        return instance.union(*value)
    

    @staticmethod
    def sub_operation( instance:set|frozenset, value ):
        return instance - value

    @staticmethod
    def and_operation( instance:set|frozenset, value ):
        return instance & value
    
    @staticmethod
    def or_operation( instance:set|frozenset, value ):
        return instance | value
    
    @staticmethod
    def xor_operation( instance:set|frozenset, value ):
        return instance ^ value
    
    # -----------------------------------------------
    # -------------------- TESTS --------------------
    # -----------------------------------------------

    # -----------------------------------------------
    # Test methods

    def test_set_frozenset_difference_method( self ):
        """ Tests set / frozenset 'difference' method
        
        (i) all base instances the tests are run on are 'str' typed

        Light version
        -------------
        (i) operation doesn't modify base instance,
        so should be handled by the built-in
        
        - should work with any iterable (no matter the items type)
        - operation should return a built-in equivalent
        
        Complete version
        ----------------
        (i) operation can't introduce incompatible items in the result,
        so operation value shoudln't be type-checked

        - should work with any iterable (no matter the items type)
        - operation should return a new instance of the typed iterable class
        """
        # -- Light typed iterable 
        assertions.operation_succeeds(
            test_case = self,
            classes = (TypedSet_lt, TypedFrozenset_lt),
            test_function = self.difference,
            star_args_test_function_variant = self.difference_multiple_args,
            operation_values = self.samples.all_iterables_variations(
                preset = 'ITERABLE'
            ),
            expected_result_type = 'Builtin',
        )

        # -- Complete typed iterable
        # remark: difference can't introduce wrong type items,
        # so it shouldn't be type-checked
        assertions.operation_succeeds(
            test_case = self,
            classes = (TypedSet, TypedFrozenset),
            test_function = self.difference,
            star_args_test_function_variant = self.difference_multiple_args,
            operation_values = self.samples.all_iterables_variations(
                preset = 'ITERABLE'
            ),
            expected_result_type = 'SelfClass',
        )
    
    def test_set_frozenset_intersection_method( self ):
        """ Tests set / frozenset 'intersection' method
        
        (i) all base instances the tests are run on are 'str' typed

        Light version
        -------------
        (i) operation doesn't modify base instance,
        so should be handled by the built-in
        
        - should work with any iterable (no matter the items type)
        - operation should return a built-in equivalent
        
        Complete version
        ----------------
        (i) operation can't introduce incompatible items in the result,
        so operation value shoudln't be type-checked

        - should work with any iterable (no matter the items type)
        - operation should return a new instance of the typed iterable class
        """

        # -- Light typed iterable 
        assertions.operation_succeeds(
            test_case = self,
            classes = (TypedSet_lt, TypedFrozenset_lt),
            test_function = self.intersection,
            star_args_test_function_variant = self.intersection_multiple_args,
            operation_values = self.samples.all_iterables_variations(
                preset = 'ITERABLE'
            ),
            expected_result_type = 'Builtin',
        )

        # -- Complete typed iterable
        # remark: intersection can't introduce wrong type items,
        # so it shouldn't be type-checked
        assertions.operation_succeeds(
            test_case = self,
            classes = (TypedSet, TypedFrozenset),
            test_function = self.intersection,
            star_args_test_function_variant = self.intersection_multiple_args,
            operation_values = self.samples.all_iterables_variations(
                preset = 'ITERABLE'
            ),
            expected_result_type = 'SelfClass',
        )

    def test_set_frozenset_symmetric_difference_method( self ):
        """ Tests set / frozenset 'symmetric_difference' method
        
        (i) all base instances the tests are run on are 'str' typed

        Light version
        -------------
        (i) operation doesn't modify base instance,
        so should be handled by the built-in
        
        - should work with any iterable (no matter the items type)
        - operation should return a built-in equivalent
        
        Complete version
        ----------------
        - should work only with compatible iterables
        - should fail with incompatible iterable
        - operation should return a new instance of the typed iterable class
        """

        # -- Light typed iterable 
        assertions.operation_succeeds(
            test_case = self,
            classes = (TypedSet_lt, TypedFrozenset_lt),
            test_function = self.symmetric_difference,
            operation_values = self.samples.all_iterables_variations(
                preset = 'ITERABLE'
            ),
            expected_result_type = 'Builtin',
        )

        # -- Complete typed iterable
        assertions.operation_succeeds(
            test_case = self,
            classes = (TypedSet, TypedFrozenset),
            test_function = self.symmetric_difference,
            operation_values = self.samples.typed_and_builtin_iterables_preset(
                preset = 'ITERABLE',
                items_type = str,
                init_value_variant = 'OPERATION'
            ),
            expected_result_type = 'SelfClass',
        )

        assertions.operation_fails(
            test_case = self,
            classes = (TypedSet, TypedFrozenset),
            test_function = self.symmetric_difference,
            operation_values = self.samples.all_int_and_mixed_iterables_variations(
                preset = 'ITERABLE'
            ),
            expected_exception = _TypedIterError,
        )
    
    def test_set_frozenset_union_method( self ):
        """ Tests set / frozenset 'union' method
        
        (i) all base instances the tests are run on are 'str' typed

        Light version
        -------------
        (i) operation doesn't modify base instance,
        so should be handled by the built-in
        
        - should work with any iterable (no matter the items type)
        - operation should return a built-in equivalent
        
        Complete version
        ----------------
        - should work only with compatible iterables
        - should fail with incompatible iterable
        - operation should return a new instance of the typed iterable class
        """
        # -- Light typed iterable 
        assertions.operation_succeeds(
            test_case = self,
            classes = (TypedSet_lt, TypedFrozenset_lt),
            test_function = self.union,
            star_args_test_function_variant = self.union_multiple_args,
            operation_values = self.samples.all_iterables_variations(
                preset = 'ITERABLE'
            ),
            expected_result_type = 'Builtin',
        )

        # -- Complete typed iterable
        assertions.operation_succeeds(
            test_case = self,
            classes = (TypedSet, TypedFrozenset),
            test_function = self.union,
            star_args_test_function_variant = self.union_multiple_args,
            operation_values = self.samples.typed_and_builtin_iterables_preset(
                preset = 'ITERABLE',
                items_type = str,
                init_value_variant = 'OPERATION',
            ),
            expected_result_type = 'SelfClass',
        )

        assertions.operation_fails(
            test_case = self,
            classes = (TypedSet, TypedFrozenset),
            test_function = self.union,
            star_args_test_function_variant = self.union_multiple_args,
            operation_values = self.samples.all_int_and_mixed_iterables_variations(
                preset = 'ITERABLE'
            ),
            expected_exception = _TypedIterError,
        )

    # -----------------------------------------------
    # Test dunders

    def test_set_frozenset_operation_sub( self ):
        """ Tests set / frozenset 'sub' dunder method
        
        (i) all base instances the tests are run on are 'str' typed

        Light version
        -------------
        (i) operation doesn't modify base instance,
        so should be handled by the built-in
        
        - should work with any set/frozenset (no matter the items type)
        - operation should return a built-in equivalent
        
        Complete version
        ----------------
        (i) operation can't introduce incompatible items in the result,
        so operation value shoudln't be type-checked

        - should work with any set/frozenset (no matter the items type)
        - operation should return a new instance of the typed iterable class
        """
        # -- Light typed iterable 
        assertions.operation_succeeds(
            test_case = self,
            classes = (TypedSet_lt, TypedFrozenset_lt),
            test_function = self.sub_operation,
            operation_values = self.samples.all_iterables_variations(
                preset = 'SET'
            ),
            expected_result_type = 'Builtin',
        )

        # -- Complete typed iterable
        # remark: substraction can't introduce wrong type items,
        # so it shouldn't be type-checked
        assertions.operation_succeeds(
            test_case = self,
            classes = (TypedSet, TypedFrozenset),
            test_function = self.sub_operation,
            operation_values = self.samples.all_iterables_variations(
                preset = 'SET'
            ),
            expected_result_type = 'SelfClass',
        )
    
    def test_set_frozenset_operation_and( self ):
        """ Tests set / frozenset 'and' dunder method
        
        (i) all base instances the tests are run on are 'str' typed

        Light version
        -------------
        (i) operation doesn't modify base instance,
        so should be handled by the built-in
        
        - should work with any set/frozenset (no matter the items type)
        - operation should return a built-in equivalent
        
        Complete version
        ----------------
        (i) operation can't introduce incompatible items in the result,
        so operation value shoudln't be type-checked

        - should work with any set/frozenset (no matter the items type)
        - operation should return a new instance of the typed iterable class
        """
        # -- Light typed iterable 
        assertions.operation_succeeds(
            test_case = self,
            classes = (TypedSet_lt, TypedFrozenset_lt),
            test_function = self.and_operation,
            operation_values = self.samples.all_iterables_variations(
                preset = 'SET'
            ),
            expected_result_type = 'Builtin',
        )

        # -- Complete typed iterable
        # remark: and operation can't introduce wrong type items,
        # so it shouldn't be type-checked
        assertions.operation_succeeds(
            test_case = self,
            classes = (TypedSet, TypedFrozenset),
            test_function = self.and_operation,
            operation_values = self.samples.all_iterables_variations(
                preset = 'SET'
            ),
            expected_result_type = 'SelfClass',
        )
    
    def test_set_frozenset_operation_or( self ):
        """ Tests set / frozenset 'or' dunder method
        
        (i) all base instances the tests are run on are 'str' typed

        Light version
        -------------
        (i) operation doesn't modify base instance,
        so should be handled by the built-in
        
        - should work with any set/frozenset (no matter the items type)
        - operation should return a built-in equivalent
        
        Complete version
        ----------------
        - should work only with compatible set/frozenset
        - should fail with incompatible set/frozenset
        - operation should return a new instance of the typed iterable class
        """
        # -- Light typed iterable 
        assertions.operation_succeeds(
            test_case = self,
            classes = (TypedSet_lt, TypedFrozenset_lt),
            test_function = self.or_operation,
            operation_values = self.samples.all_iterables_variations(
                preset = 'SET'
            ),
            expected_result_type = 'Builtin',
        )

        # -- Complete typed iterable
        assertions.operation_succeeds(
            test_case = self,
            classes = (TypedSet, TypedFrozenset),
            test_function = self.or_operation,
            operation_values = self.samples.typed_and_builtin_iterables_preset(
                preset = 'SET',
                items_type = str,
                init_value_variant = 'OPERATION',
            ),
            expected_result_type = 'SelfClass',
        )

        assertions.operation_fails(
            test_case = self,
            classes = (TypedSet, TypedFrozenset),
            test_function = self.or_operation,
            operation_values = self.samples.all_int_and_mixed_iterables_variations(
                preset = 'SET'
            ),
            expected_exception = _TypedIterError,
        )
    
    def test_set_frozenset_operation_xor( self ):
        """ Tests set / frozenset 'xor' dunder method
        
        (i) all base instances the tests are run on are 'str' typed

        Light version
        -------------
        (i) operation doesn't modify base instance,
        so should be handled by the built-in
        
        - should work with any set/frozenset (no matter the items type)
        - operation should return a built-in equivalent
        
        Complete version
        ----------------
        - should work only with compatible set/frozenset
        - should fail with incompatible set/frozenset
        - operation should return a new instance of the typed iterable class
        """
        # -- Light typed iterable 
        assertions.operation_succeeds(
            test_case = self,
            classes = (TypedSet_lt, TypedFrozenset_lt),
            test_function = self.xor_operation,
            operation_values = self.samples.all_iterables_variations(
                preset = 'SET'
            ),
            expected_result_type = 'Builtin',
        )

        # -- Complete typed iterable
        assertions.operation_succeeds(
            test_case = self,
            classes = (TypedSet, TypedFrozenset),
            test_function = self.xor_operation,
            operation_values = self.samples.typed_and_builtin_iterables_preset(
                preset = 'SET',
                items_type = str,
                init_value_variant = 'OPERATION',
            ),
            expected_result_type = 'SelfClass',
        )

        assertions.operation_fails(
            test_case = self,
            classes = (TypedSet, TypedFrozenset),
            test_function = self.xor_operation,
            operation_values = self.samples.all_int_and_mixed_iterables_variations(
                preset = 'SET'
            ),
            expected_exception = _TypedIterError,
        )
