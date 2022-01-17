# -*- coding: utf-8 -*-
""" HELPER FUNCTIONS MODULE
"""
__author__ = 'kokarev.nv'

from typing import Any, Union, Collection, Sequence
from .constants import (
    PREDEFINED_TRUE_ARRAY, PREDEFINED_FALSE_ARRAY, VALID_ARRAY_TYPES
)


def exec_if_cond(cond: bool, func: Any, *args) -> Any:
    """ Execute a function with any positional args if condition True. 

    Args:
        cond (bool): function execution condition
        func (Any): callable object, exec function

    Returns:
        Any: function execution result
    """
    if cond:
        func(*args)


def raise_if_cond(cond: bool, error_msg: str, exc_class=Exception):
    """ Raise an exception with error message, if condition is true.

    Args:
        cond (bool): exception condition
        error_msg (str): mesage text
        exc_class (Exception, optional): exception class. Defaults to Exception.
    """
    if cond:
        raise exc_class(error_msg)


class Collations:
    """ Boolean cast functions inside.

    """
    @staticmethod
    def try_true(value: Any) -> Any:
        """ Trying to cast a predefined value to boolean True.

        Args:
            value (Any): value to cast

        Returns:
            bool, Any: casted value or started value
        """
        return str(value).lower() in PREDEFINED_TRUE_ARRAY or value

    @staticmethod
    def try_false(value: Any) -> Any:
        """ Trying to cast a predefined value to boolean False.

        Args:
            value (Any): value to cast

        Returns:
            bool, Any: casted value or started value
        """
        return False if str(value).lower() in PREDEFINED_FALSE_ARRAY else value

    @classmethod
    def try_bool(cls, value: Any) -> Any:
        """ Trying to cast a predefined value to boolean.

        Args:
            value (Any): value to cast

        Returns:
            bool, Any: casted value or started value
        """
        if isinstance(value, bool):
            return value

        ans = cls.try_true(value)
        if not isinstance(ans, bool):
            ans = cls.try_false(value)

        return ans


class Collections:
    """ Collection handling functions inside.

    """
    @staticmethod
    def coalesce(*args):
        """ Unpackage the first elem that casts to True. If all elems cast to False, then return the last elem.

        Returns:
            any type: first elem that casts to true or last elem
        """
        return next((el for el in args if el), args[-1])

    @staticmethod
    def distinct(*args) -> list:
        """ Get only unique subelements that can be non-hashable types. Strongly typed matches only!

        Returns:
            list: unique elements
        """
        return [
            el for idx, el in enumerate(args) if (
                el not in args[:idx] or 
                type(el) != type(args[args[:idx].index(el)])
            )
        ]

    @classmethod
    def get_diff_list(
        cls, 
        alfa: Union[Collection, Sequence], 
        beta: Union[Collection, Sequence], 
        distinct: bool=False
    ) -> list:     
        """ Subtract beta from alfa and return a difference list.

        Args:
            alfa (Union[Collection, Sequence]): first object with elements
            beta (Union[Collection, Sequence]): second object with elements
            distinct (bool, optional): get diffs as unique elems. Defaults to False.

        Returns:
            list: diff elements
        """
        res = [item for item in alfa if item not in beta]
        if distinct:
            res = cls.distinct(*res)
        return res
    
    @classmethod
    def get_common_uniques(
        cls, 
        alfa: Union[Collection, Sequence], 
        beta: Union[Collection, Sequence]
    ) -> list:      
        """ Calculate an intersection as common unique elements.

        Args:
            alfa (Union[Collection, Sequence]): first object with elements
            beta (Union[Collection, Sequence]): second object with elements

        Returns:
            list: common unique elements
        """
        res = [item for item in alfa if item in beta]
        return cls.distinct(*res)
    
    @classmethod
    def is_subset(
        cls, 
        alfa: Union[Collection, Sequence], 
        beta: Union[Collection, Sequence]
    ) -> bool:       
        """ True if all distinct elements of alfa belong to elements as beta.

        Args:
            alfa (Union[Collection, Sequence]): first object with distinct elements
            beta (Union[Collection, Sequence]): second object with distinct elements

        Returns:
            bool: alfa is a subset of beta
        """
        alfa = cls.distinct(*alfa)
        return [item for item in alfa if item in beta] == alfa

    @staticmethod
    def split_sequence_gen(
        input_array: Union[Sequence, set], 
        size: int
    ):
        """ Split an array into parts of custom length.

        Args:
            input_array (Union[Sequence, set]): split array
            size (int): length of custom parts

        Yields:
            Iterator[Sequence]: custom part getting by slice
        """
        if isinstance(input_array, set):
            input_array = list(input_array)
        if not isinstance(input_array, Sequence):
            raise_if_cond(True, "The input value must be a sequence or set.", TypeError)

        for idx in range(0, len(input_array), size):
            yield input_array[idx: idx + size]

    @classmethod
    def extract_subelements(
        cls, 
        input_array: Union[dict, tuple, list, set], 
        unique_items_only: bool = False
    ) -> list:
        """ Extract elements of subcollections inside. 

        Args:
            input_array (Union[dict, tuple, list, set]): array with subelements
            unique_items_only (bool, optional): unique subelements only. Defaults to False.

        Returns:
            list: array with extracted subelements
        """
        if isinstance(input_array, dict):
            input_array = list(input_array.values())

        if not isinstance(input_array, VALID_ARRAY_TYPES):
            return input_array

        res_array = list()
        for el in input_array:
            if isinstance(el, VALID_ARRAY_TYPES):
                res_array += el
            else:
                res_array.append(el)

        if unique_items_only:
            res_array = cls.distinct(*res_array)

        return res_array
