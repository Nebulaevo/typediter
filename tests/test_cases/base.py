import unittest

from typediter.exceptions import (
    InvalidTypeRestrictionError, 
    TypeRestrictionError, 
    IterableExpectedError
)

from tests.helpers import TestSamples, assertions

class BaseTest( unittest.TestCase ):
    """ Base tests for all typed iterable instances

    Tested Classes
    --------------
    - TypedList_lt
    - TypedList
    - TypedTuple_lt
    - TypedTuple
    - TypedSet_lt
    - TypedSet
    - TypedFrozenset_lt
    - TypedFrozenset

    Tested
    ------
    - initialisation
    - iterability of instances
    """

    def __init__( self, *args, **kwargs ):
        """ Setting up common ressources for tests """
        self.samples = TestSamples( self )
        self.classes = self.samples.typed_iterable_classes( preset='ITERABLE' )
        super().__init__( *args, **kwargs )

    def test_initialisation( self ):
        """ Tests instance initialisation of typed iterable
        - without any init value
        - with empty init value
        - with compatible iterable
        - with incomptible iterable
        - with an invalid type restriction (i_type)

        (i) all base instances the tests are run on are 'str' typed
        (except for the invalid type restriction)
        """

        # -- Empty initialisation
        assertions.initialisation_succeeds( 
            test_case = self, 
            classes = self.classes,
            init_values = [ None, ] # 'None' handled in a special case
        )

        assertions.initialisation_succeeds( 
            test_case = self, 
            classes = self.classes,
            init_values = self.samples.typed_and_builtin_iterables_preset(
                preset = 'ITERABLE',
                items_type = str,
                init_value_variant = 'EMPTY'
            )
        )

        # -- Normal initialisation
        assertions.initialisation_succeeds( 
            test_case = self, 
            classes = self.classes,
            init_values = self.samples.typed_and_builtin_iterables_preset(
                preset = 'ITERABLE',
                items_type = str,
                init_value_variant = 'OPERATION'
            )
        )

        # -- with incompatible iterables
        assertions.initialisation_fails(
            test_case = self, 
            classes = self.classes,
            init_values = self.samples.all_int_and_mixed_iterables_variations(
                preset = 'ITERABLE'
            ),
            expected_exception = TypeRestrictionError
        )

        # -- with non-iterable values
        assertions.initialisation_fails(
            test_case = self, 
            classes = self.classes,
            init_values = self.samples.non_iterables(),
            expected_exception = IterableExpectedError
        )

        # -- with invalid type restrictions
        # (invalid i_type should fail before anything else)

        # not a type
        assertions.initialisation_fails(
            test_case = self, 
            classes = self.classes,
            init_values = self.samples.non_iterables(), # because invalid i_type should fail first
            i_type = '- NOT A TYPE -',
            expected_exception = InvalidTypeRestrictionError,
        )

        # not hashable type (for set/frozenset based)
        assertions.initialisation_fails(
            test_case = self, 
            classes = self.samples.typed_iterable_classes( preset='SET' ),
            init_values = self.samples.non_iterables(), # because invalid i_type should fail first
            i_type = list,
            expected_exception = InvalidTypeRestrictionError,
        )
    
    def test_iterability( self ):
        """ Tests iterability of typed iterable instances

        (i) tested because it had been a problem 
        when trying to have base classes (_FrozenTypedIter, _MutableTypedIter) inherit from Iterable
        """
        assertions.instances_are_iterable(
            test_case = self,
            classes = self.classes
        )
