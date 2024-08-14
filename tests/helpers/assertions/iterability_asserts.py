import unittest
from typing import Type, Iterable

from typediter.types import TypedIterable_T

from tests.helpers import msg, TestSamples
from . import _helpers


def instances_are_iterable(
        test_case: unittest.TestCase,
        classes: Iterable[ Type[TypedIterable_T] ]
):
    """ Asserts that all given classes produce iterable instances

    (i) have been a problem at one point, 
    when the base classes (_FrozenTypedIter, _MutableTypedIter) were directly inheriting from Iterable, 
    so we check for sanity.

    we check if trying to iterate over the instance doesn't raise any errors,
    and the number of iteration is the same as the built-in equivalent initialised with the same value

    Parameters
    ----------
    - **test_case**
        the TestCase class from which the function is called

    - **classes**
        iterable containing the typed iterable classes to run the test on
    """
    local_samples = TestSamples( test_case )

    for typed_iterable_cls in classes:

        with test_case.subTest( typed_iterable_cls=typed_iterable_cls ):
            builtin_reference_cls = _helpers.get_builtin_equivalent(
                typed_iterable_cls
            )

            # ----- SET UP
            builtin_ref, *_ = local_samples.builtin_iterables(
                classes = ( builtin_reference_cls, ),
                items_type = str,
                init_value_variant = 'BASE'
            )

            typed_iterable, *_ = local_samples.typed_iterables(
                classes = ( typed_iterable_cls, ),
                items_type = str,
                init_value_variant = 'BASE'
            )

            # to make mypy happy
            assert isinstance( builtin_ref, (list, tuple, set, frozenset) )

            expected_iterations = len( builtin_ref )
            loops = 0

            # ----- TEST
            try:
                for _ in typed_iterable:
                    loops += 1
            except Exception as err:
                test_case.fail(
                    msg.iterating_over_instance_failed(
                        err = err,
                        inst = typed_iterable
                    )
                )
            
            # ----- ASSERTIONS
            test_case.assertEqual(
                loops, expected_iterations,
                msg.unexpected_number_of_iterations(
                    inst = typed_iterable,
                    builtin_ref = builtin_ref,
                    loops_done = loops,
                    expected_iterations = expected_iterations
                )
            )
