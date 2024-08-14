import unittest

from typediter import (
    TypedList_lt, TypedList,
    TypedSet_lt, TypedSet,
    TypedFrozenset_lt, TypedFrozenset
)

from tests.helpers import TestSamples, assertions

class CommonCopyTests( unittest.TestCase ):
    """ Tests the 'copy' method for all classes that have that method

    Tested Classes
    --------------
    (every class except tuple based classes)
    - TypedList_lt
    - TypedList
    - TypedSet_lt
    - TypedSet
    - TypedFrozenset_lt
    - TypedFrozenset

    Tested
    ------
    - (method) copy
    """

    def __init__( self, *args, **kwargs ):
        """ Setting up common ressources for tests """   
        self.samples = TestSamples( self )
        super().__init__( *args, **kwargs )

    # -------------------- Tested operations --------------------
    
    @staticmethod
    def copy( instance:list, value ):
        return instance.copy()
    
    # -----------------------------------------------
    # -------------------- TESTS --------------------
    # -----------------------------------------------

    def test_copy_methods( self ):
        """ Testing copy method on all classes that have that method

        (i) for 'light' typed iterables, copy is an exception.
        normally, light version of typed iterable returns built-ins
        for operations that doesn't modify the instance directly.
        But copy is still overridden to return a typed iterable
        because it would be counter intuitive for it to return an
        instance of another class.
        """
        assertions.operation_succeeds(
            test_case = self,
            classes = ( 
                TypedList_lt, TypedList, 
                TypedSet_lt, TypedSet, 
                TypedFrozenset_lt, TypedFrozenset 
            ),
            test_function = self.copy,
            operation_values = ( None, ), # doesn't take args
            expected_result_type = 'SelfClass',
        )
