import unittest

from typediter.exceptions import _TypedIterError, InvalidTypeRestrictionError
from typediter.utils import (
    is_typediter_instance, 
    is_typediter_subclass,
    get_converter_func,
    get_typesafe_tuple_converter_func,
    get_typesafe_frozenset_converter_func,
)

from tests.helpers import TestSamples, assertions


class UtilityTests( unittest.TestCase ):
    """ Tests utility functions

    Tested Utilities
    ----------------
    - (function) is_typediter_instance
    - (function) is_typediter_subclass
    - (function) filter_items
    - (function) get_converter_func
    - (function) get_typesafe_tuple_converter_func
    - (function) get_typesafe_frozenset_converter_func
    """

    def __init__( self, *args, **kwargs ):
        """ Setting up common ressources for tests """
        self.samples = TestSamples( self )
        self.classes = self.samples.typed_iterable_classes( preset='ITERABLE' )
        super().__init__( *args, **kwargs )

    def test_is_typediter_instance_util( self ):
        """ Tests the 'is_typediter_instance' function 
        
        - it should return a bool indicating if an object is an instance
        of a typed iterable class
        """
        # with typed iterable instances (returning True)
        assertions.typechecking_utility(
            test_case = self,
            util_function = is_typediter_instance,
            operation_values = self.samples.typed_iterables_preset(
                preset = 'ITERABLE',
                items_type = str,
                init_value_variant = 'OPERATION'
            ),
            expected_result = True
        )
        
        # with values that should return False
        assertions.typechecking_utility( # -- built-in iterables
            test_case = self,
            util_function = is_typediter_instance,
            operation_values = self.samples.builtin_iterables_preset(
                preset = 'ITERABLE',
                items_type = str,
                init_value_variant = 'OPERATION'
            ),
            expected_result = False
        )

        assertions.typechecking_utility(  # -- non iterable values
            test_case = self,
            util_function = is_typediter_instance,
            operation_values = self.samples.non_iterables(),
            expected_result = False
        )

        assertions.typechecking_utility( # -- typed iterable classes
            test_case = self,
            util_function = is_typediter_instance,
            operation_values = self.samples.typed_iterable_classes( 
                preset = 'ITERABLE' 
            ),
            expected_result = False
        )
    
    def test_is_typediter_subclass_util( self ):
        """ Tests the 'is_typediter_subclass' function 
        
        - it should return a bool indicating if an object is 
        a typed iterable class
        """
        # with typed iterable classes (returning True)
        assertions.typechecking_utility(
            test_case = self,
            util_function = is_typediter_subclass,
            operation_values = self.samples.typed_iterable_classes( 
                preset = 'ITERABLE' 
            ),
            expected_result = True
        )
        
        # with values that should return False
        assertions.typechecking_utility( # -- built-in iterable classes
            test_case = self,
            util_function = is_typediter_subclass,
            operation_values = self.samples.builtin_classes( preset = 'ITERABLE' ),
            expected_result = False
        )

        assertions.typechecking_utility( # -- typed iterable instances
            test_case = self,
            util_function = is_typediter_subclass,
            operation_values = self.samples.typed_iterables_preset(
                preset = 'ITERABLE',
                items_type = str,
                init_value_variant = 'OPERATION'
            ),
            expected_result = False
        )

    def test_filter_items( self ):
        """ Tests the 'filter_items' function 
        
        - it should filter the items of an iterable to keep only
        those inheriting from a given type
        """
        assertions.filter_items_utility(
            test_case = self,
            operation_values = self.samples.all_iterables_variations(
                preset = 'ITERABLE'
            )
        )

    def test_get_converter_func( self ):
        """ Tests the 'get_converter_func' function
        
        - it should succeed to convert an iterable with compatible items
        - it should return an instance of the class it was built from
        - it should fail to convert an iterable with incompatible items
        - it should fail to convert an iterable if the i_type is invalid
        """

        # -- valid call
        assertions.typed_iterable_converter_utility_succeeds(
            test_case = self,
            classes = self.classes,
            converter_func_getter = get_converter_func,
            operation_values = self.samples.typed_and_builtin_iterables_preset(
                preset = 'ITERABLE',
                items_type = str,
                init_value_variant = 'OPERATION',       
            )
        )

        # -- invalid items
        assertions.typed_iterable_converter_utility_fails(
            test_case = self,
            classes = self.classes,
            converter_func_getter = get_converter_func,
            expected_exception = _TypedIterError,
            operation_values = self.samples.all_int_and_mixed_iterables_variations(
                preset = 'ITERABLE',
            )
        )

        # -- invalid i_type

        # not a type
        assertions.typed_iterable_converter_utility_fails(
            test_case = self,
            classes = self.classes,
            converter_func_getter = get_converter_func,
            expected_exception = InvalidTypeRestrictionError,
            operation_values = self.samples.non_iterables(), # because invalid i_type should fail first,
            i_type = '- NOT A TYPE -',
        )

        # not hashable type (for set/frozenset based)
        assertions.typed_iterable_converter_utility_fails(
            test_case = self,
            classes = self.samples.typed_iterable_classes( preset='SET' ),
            converter_func_getter = get_converter_func,
            expected_exception = InvalidTypeRestrictionError,
            operation_values = self.samples.non_iterables(), # because invalid i_type should fail first
            i_type = list,
        )

    def test_get_typesafe_tuple_converter_func( self ):
        """ Tests the 'get_typesafe_tuple_converter_func' function 
        
        - it should succeed to convert an iterable with compatible items
        - it should return an instance of the built-in tuple
        - it should fail to convert an iterable with incompatible items
        - it should fail to convert an iterable if the i_type is invalid
        """

        # -- valid call
        assertions.frozen_builtin_converter_utility_succeeds(
            test_case = self,
            converter_func_getter = get_typesafe_tuple_converter_func,
            operation_values = self.samples.typed_and_builtin_iterables_preset(
                preset = 'ITERABLE',
                items_type = str,
                init_value_variant = 'OPERATION',       
            ),
            expected_result_type = tuple,
        )

        # -- invalid items
        assertions.frozen_builtin_converter_utility_fails(
            test_case = self,
            converter_func_getter = get_typesafe_tuple_converter_func,
            expected_exception = _TypedIterError,
            operation_values = self.samples.all_int_and_mixed_iterables_variations(
                preset = 'ITERABLE',
            ),
            expected_result_type = tuple,
        )

        # -- invalid i_type
        assertions.frozen_builtin_converter_utility_fails(
            test_case = self,
            converter_func_getter = get_typesafe_tuple_converter_func,
            expected_exception = InvalidTypeRestrictionError,
            operation_values = [
                (1, 2, 3),
            ],
            expected_result_type = tuple,
            i_type = '- NOT A TYPE -',
        )

    def test_get_typesafe_frozenset_converter_func( self ):
        """ Tests the 'get_typesafe_frozenset_converter_func' function 
        
        - it should succeed to convert an iterable with compatible items
        - it should return an instance of the built-in frozenset
        - it should fail to convert an iterable with incompatible items
        - it should fail to convert an iterable if the i_type is invalid
        """
        # -- valid call
        assertions.frozen_builtin_converter_utility_succeeds(
            test_case = self,
            converter_func_getter = get_typesafe_frozenset_converter_func,
            operation_values = self.samples.typed_and_builtin_iterables_preset(
                preset = 'ITERABLE',
                items_type = str,
                init_value_variant = 'OPERATION',       
            ),
            expected_result_type = frozenset,
        )

        # -- invalid items
        assertions.frozen_builtin_converter_utility_fails(
            test_case = self,
            converter_func_getter = get_typesafe_frozenset_converter_func,
            expected_exception = _TypedIterError,
            operation_values = self.samples.all_int_and_mixed_iterables_variations(
                preset = 'ITERABLE',
            ),
            expected_result_type = frozenset,
        )

        # -- invalid i_type
        
        # not a type
        assertions.frozen_builtin_converter_utility_fails(
            test_case = self,
            converter_func_getter = get_typesafe_frozenset_converter_func,
            expected_exception = InvalidTypeRestrictionError,
            operation_values = [
                (1, 2, 3),
            ],
            expected_result_type = frozenset,
            i_type = '- NOT A TYPE -',
        )

        # not hashable type (because converting to frozenset)
        assertions.frozen_builtin_converter_utility_fails(
            test_case = self,
            converter_func_getter = get_typesafe_frozenset_converter_func,
            expected_exception = InvalidTypeRestrictionError,
            operation_values = [
                (1, 2, 3),
            ],
            expected_result_type = frozenset,
            i_type = list,
        )
