import unittest

from typediter.exceptions import _TypedIterError
from typediter import  (
    TypedList_lt, TypedList,
    TypedTuple_lt, TypedTuple, 
)

from tests.helpers import TestSamples, assertions

class CommonListTupleTests( unittest.TestCase ):
    """ Tests all common operations between typed lists and tuples

    (i) this includes all overridden methods for the typed tuples

    Tested Classes
    --------------
    - TypedList_lt
    - TypedList
    - TypedTuple_lt
    - TypedTuple

    Tested
    ------
    - (dunder) add
    - (dunder) getitem
    - (dunder) mul
    - (dunder) rmul
    """
    
    def __init__( self, *args, **kwargs ):
        """ Setting up common ressources for tests """   
        self.samples = TestSamples( self )
        super().__init__( *args, **kwargs )

    # -------------------- Tested operations --------------------
    
    @staticmethod
    def getitem_operation_with_index( instance:tuple|list, value ):
        return instance[ 1 ]
    
    @staticmethod
    def getitem_operation_with_slice( instance:tuple|list, value ):
        return instance[ 0:2 ]

    @staticmethod
    def add_operation( instance:tuple|list, value ):
        return instance + value

    @staticmethod
    def mul_operation( instance:tuple|list, value ):
        return instance * value
    
    @staticmethod
    def rmul_operation( instance:tuple|list, value ):
        return value * instance
    
    # -----------------------------------------------
    # -------------------- TESTS --------------------
    # -----------------------------------------------

    def test_list_tuple_operation_getitem_with_index( self ):
        """ Tests list / tuple 'getitem' dunder method: (index) overload
        
        for both list and tuple 'getitem' dunder declares 2 overloads:
        - __getitem__( index ) -> item
        - __getitem__( slice ) -> tuple (for tuple) lists (for list)

        (i) all base instances the tests are run on are 'str' typed

        Light and Complete versions
        ---------------------------
        (i) this overload of the operation should still have the 
        same behaviour as the built-in for both light and complete versions

        - operation should return an item (str)
        """
        assertions.operation_succeeds(
            test_case = self,
            classes = ( 
                TypedList_lt, TypedList,
                TypedTuple_lt, TypedTuple 
            ),
            test_function = self.getitem_operation_with_index,
            operation_values = [ None ], # doesn't take args
            expected_result_type = str # item
        )

    def test_list_tuple_operation_getitem_with_slice( self ):
        """ Tests list / tuple 'getitem' dunder method: (slice) overload
        
        for both list and tuple 'getitem' dunder declares 2 overloads:
        - __getitem__( index ) -> item
        - __getitem__( slice ) -> tuple (for tuple) lists (for list)

        (i) all base instances the tests are run on are 'str' typed

        Light version
        -------------
        (i) operation doesn't modify base instance,
        so should be handled by the built-in

        - operation should return a built-in equivalent
        
        Complete version
        ----------------
        - operation should return a new instance of the typed iterable class
        """
        assertions.operation_succeeds(
            test_case = self,
            classes = (TypedList_lt, TypedTuple_lt),
            test_function = self.getitem_operation_with_slice,
            operation_values = [ None ], # doesn't take args
            expected_result_type = 'Builtin'
        )

        assertions.operation_succeeds(
            test_case = self,
            classes = (TypedList, TypedTuple),
            test_function = self.getitem_operation_with_slice,
            operation_values = [ None ], # doesn't take args
            expected_result_type = 'SelfClass'
        )

    def test_list_tuple_operation_add( self ):
        """ Tests list / tuple 'add' dunder method
        
        (i) all base instances the tests are run on are 'str' typed

        Light version
        -------------
        (i) operation doesn't modify base instance,
        so should be handled by the built-in
        
        - should work with any tuple (for tuple) lists (for list) (no matter the items type)
        - operation should return a built-in equivalent
        
        Complete version
        ----------------
        - should work only with compatible tuple (for tuple) lists (for list)
        - should fail with incompatible tuple (for tuple) lists (for list)
        - operation should return a new instance of the typed iterable class
        """
        # -- Light typed iterable
        assertions.operation_succeeds(
            test_case = self,
            classes = ( TypedList_lt, ),
            test_function = self.add_operation,
            operation_values = self.samples.all_iterables_variations(
                preset = 'LIST',
            ),
            expected_result_type = 'Builtin',
        )

        assertions.operation_succeeds(
            test_case = self,
            classes = ( TypedTuple_lt, ),
            test_function = self.add_operation,
            operation_values = self.samples.all_iterables_variations(
                preset = 'TUPLE',
            ),
            expected_result_type = 'Builtin',
        )

        # -- Complete typed iterable
        assertions.operation_succeeds(
            test_case = self,
            classes = ( TypedList, ),
            test_function = self.add_operation,
            operation_values = self.samples.typed_and_builtin_iterables_preset(
                preset = 'LIST',
                items_type = str,
                init_value_variant = 'OPERATION'
            ),
            expected_result_type = 'SelfClass',
        )

        assertions.operation_succeeds(
            test_case = self,
            classes = ( TypedTuple, ),
            test_function = self.add_operation,
            operation_values = self.samples.typed_and_builtin_iterables_preset(
                preset = 'TUPLE',
                items_type = str,
                init_value_variant = 'OPERATION'
            ),
            expected_result_type = 'SelfClass'
        )
        
        assertions.operation_fails(
            test_case = self,
            classes = ( TypedList, ),
            test_function = self.add_operation,
            operation_values = self.samples.all_int_and_mixed_iterables_variations( 
                preset = 'LIST',
            ),
            expected_exception = _TypedIterError
        )

        assertions.operation_fails(
            test_case = self,
            classes = ( TypedTuple, ),
            test_function = self.add_operation,
            operation_values = self.samples.all_int_and_mixed_iterables_variations(
                preset = 'TUPLE',
            ),
            expected_exception = _TypedIterError,
        )
    
    def test_list_tuple_operation_mul( self ):
        """ Tests list / tuple 'mul' dunder method
        
        (i) all base instances the tests are run on are 'str' typed
        
        Light version
        -------------
        (i) operation doesn't modify base instance,
        so should be handled by the built-in
        
        - operation should return a built-in equivalent
        
        Complete version
        ----------------
        - operation should return a new instance of the typed iterable class
        """
        operation_test_values = ( 0, 3, -2 )
        
        # -- Light typed iterable
        assertions.operation_succeeds(
            test_case = self,
            classes = (TypedList_lt, TypedTuple_lt),
            test_function = self.mul_operation,
            operation_values = operation_test_values,
            expected_result_type = 'Builtin',
        )

        # -- Complete typed iterable
        assertions.operation_succeeds(
            test_case = self,
            classes = (TypedList, TypedTuple),
            test_function = self.mul_operation,
            operation_values = operation_test_values,
            expected_result_type = 'SelfClass',
        )

    def test_list_tuple_operation_rmul( self ):
        """ Tests tuple 'rmul' dunder method
        
        (i) all base instances the tests are run on are 'str' typed
        
        Light version
        -------------
        (i) operation doesn't modify base instance,
        so should be handled by the built-in
        
        - operation should return a built-in equivalent
        
        Complete version
        ----------------
        - operation should return a new instance of the typed iterable class
        """
        operation_test_values = ( 0, 3, -2 )
        
        # -- Light typed iterable
        assertions.operation_succeeds(
            test_case = self,
            classes = (TypedList_lt, TypedTuple_lt),
            test_function = self.rmul_operation,
            operation_values = operation_test_values,
            expected_result_type = 'Builtin',
        )

        # -- Complete typed iterable
        assertions.operation_succeeds(
            test_case = self,
            classes = (TypedList, TypedTuple),
            test_function = self.rmul_operation,
            operation_values = operation_test_values,
            expected_result_type = 'SelfClass',
        )