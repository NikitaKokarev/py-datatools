# -*- coding: utf-8 -*-
""" HELPER FUNCTIONS MODULE.
"""
__author__ = 'kokarev.nv'

from re import findall
from random import getrandbits
from typing import Any, Optional, Union, Collection, Sequence
from .constants import (
    PREDEFINED_TRUE_ARRAY, PREDEFINED_FALSE_ARRAY, VALID_ARRAY_TYPES, ONLY_NUMBERS_SYMBOLS
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


def try_true(value: Any) -> Any:
    """ Trying to cast a predefined value to boolean True.

    Args:
        value (Any): value to cast
    Returns:
        bool, Any: casted value or started value
    """
    return str(value).lower() in PREDEFINED_TRUE_ARRAY or value


def try_false(value: Any) -> Any:
    """ Trying to cast a predefined value to boolean False.

    Args:
        value (Any): value to cast
    Returns:
        bool, Any: casted value or started value
    """
    return False if str(value).lower() in PREDEFINED_FALSE_ARRAY else value


def try_bool(value: Any) -> Any:
    """ Trying to cast a predefined value to boolean.

    Args:
        value (Any): value to cast
    Returns:
        bool, Any: casted value or started value
    """
    if isinstance(value, bool):
        return value

    ans = try_true(value)
    if not isinstance(ans, bool):
        ans = try_false(value)

    return ans


class Collections:
    """ Collection handling functions.
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

        raise_if_cond(not isinstance(input_array, Sequence), "The input value must be a sequence or set.", TypeError)

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


class Numbers:
    """ Number handling functions.
    """
    def parse_int(number_seq: Union[int, float, str, bytes, bytearray]) -> int:
        """ Sometimes methods come with id like '1234,Enterprise Structure',
            you need to take a number from this, for example, for a request.
            If it was not possible to cast or there are no numbers in the line, then None is returned.
            allNumbers - whether to take all the numbers in the line or just the 1st occurrence.

        Args:
            number_seq: sequence containing numbers.
        Returns:
            input is casted to integer.
        """
        def get_int_sequence(num_list: list) -> int:
            """ Get a sequence of numbers

            Args:
                num_list: list of strings with numbers.
            Returns:
                int: sequence of numbers.
            """
            return int(''.join(num_list))

        if not number_seq:
            return 0

        if isinstance(number_seq, int):
            # if this is an int, then return it as is.
            ans = number_seq
        elif isinstance(number_seq, float):
            # if this is a float, then let's convert it to int.
            ans = int(number_seq)
        elif isinstance(number_seq, (bytes, bytearray)):
            ans = get_int_sequence([str(el) for el in number_seq])
        elif isinstance(number_seq, str):
            # if this is a string, then select all the numbers and return the first one that comes up.
            num_list = findall('[-]*[0-9]+', number_seq)
            raise_if_cond(not num_list, "Text does not contain a number.")
            ans = get_int_sequence(num_list)
        else:
            raise_if_cond(True, "Incorrect data type used.", TypeError)

        return ans

    @staticmethod
    def try_int(chars: Sequence) -> Optional[int]:
        """ Try to get a int number.

        Args:
            chars: sequence containing numbers.
        Returns:
            Optional[int]: sequence of numbers.
        """
        try:
            num = int(chars)
        except ValueError:
            num = None
        return num

    @staticmethod
    def try_float(chars: Sequence) -> Optional[float]:
        """ Try to get a float number.

        Args:
            chars: sequence containing numbers.
        Returns:
            Optional[float]: sequence of numbers.
        """
        try:
            num = float(chars)
        except ValueError:
            num = None
        return num

    @classmethod
    def get_formatted_tooltip(cls, number: Union[int, float, str]) -> str:
        """ Creates a formatted counter of type 2.0M, 1.3K from an integer.

        Args:
            number: sequence containing numbers.
        Returns:
            str: formatted counter of numbers.
        """
        raise_if_cond(
            not (isinstance(number, int) or isinstance(number, float) or isinstance(number, str)),
            "Incorrect data type used.",
            TypeError
        )

        if isinstance(number, str):
            int_cast = cls.try_int(number)
            number = cls.try_float(number) if int_cast is None else int_cast
            raise_if_cond(number is None, "Incorrect text contains numbers.", TypeError)

        elif isinstance(number, float):
            number = cls.try_float(number)

        if number > 999499:
            ans = ('{:.1f}' + 'M').format(number / 1000000).replace('.0', '')
        elif number > 99999:
            ans = ('{:.0f}' + 'K').format(number / 1000).replace('.0', '')
        elif number >= 1000:
            ans = ('{:.1f}' + 'K').format(number / 1000).replace('.0', '')
        elif number <= 0:
            ans = '0'
        else:
            ans = str(number).replace('.0', '')

        return ans

    @staticmethod
    def unique_id(num_digit: int=32) -> int:
        """ Random number generator from random n-bits with increment +1

        Args:
            num_digit: number of bits.
        Yields:
            int: random int number.
        """
        seed = getrandbits(num_digit)
        while True:
            yield seed
            seed += 1

    @staticmethod
    def digitize_string(chars: Optional[Sequence]) -> str:
        """ Get numbers in str, without the risk of injections or errors, then paste them into the request.

        Args:
            chars: text with numbers.
        Returns:
            str: Valid text with numbers.
        """
        if chars is None:
            return ''

        seq = str(chars)
        # zero positioned char is minus. Hold it.
        if seq[0] == '-':
            preffix = '-'
        else:
            preffix = ''

        return f"{preffix}{''.join([seq if '0' <= seq <= '9' else '' for seq in seq])}"


class CKey:
    """ Class for working with composite keys for postgres tmpls as example.
    """
    DELIMETER = '.'
    def __init__(self, *cfg: list):
        if len(cfg) != 2:
            raise Exception('This class couldn\'t used directly!')
        self.NAMES = cfg[0]
        self.TYPES = cfg[1]

    def unpack_dict(self, compk: str) -> dict:
        """ Unpacks one composite key into a dictionary.

        Args:
            compk: text value of composite key.
        Returns:
            dict of keys.
        """
        klist = compk.split(self.DELIMETER)
        return {key: self.TYPES[idx](klist[idx]) if klist[idx] else None for idx, key in enumerate(self.NAMES)}

    def unpack(self, compk: str, *names_list: list) -> list:
        """ Unpacks one composite key into a set of values.

        Args:
            compk: text value of composite key.
            names_list: names list of composite keys.
        Returns:
            list of keys.
        """
        compk_dict = self.unpack_dict(compk)
        return [compk_dict[name] for name in names_list]

    def unpack_list(self, compk_list: list, *names_list: list) -> list:
        """ Unpacks from an array of composite keys an array of values of the values of all keys.

        Args:
            compk_list: list of composite keys.
            names_list: names list of composite keys.
        Yields:
            list of keys.
        """
        for item in compk_list:
            if item:
                yield self.unpack(item, *names_list)

    def pack(self, keys_dict: dict) -> str:
        """ Makes a composite key from a set of values.

        Args:
            keys_dict: dict of keys (name: value).
        Returns:
            str: composite key.
        """
        return self.DELIMETER.join(
            [str(keys_dict.get(name)) if keys_dict.get(name) is not None else '' for name in self.NAMES]
        )


class Text:
    """ String processing class.
    """
    def crop_text_line_by_line(msg: str='', max_lines: int=2, max_len_line: int=32) -> str:
        """ Trims long lines taking into account word wraps.

        Args:
            msg (str, optional): input text. Defaults to ''.
            max_lines (int, optional): how many lines should fit. Defaults to 2.
            max_len_line (int, optional): maximum line length in characters. Defaults to 32.

        Returns:
            str: output formatted text
        """
        if not msg:
            return msg
        else:
            msg = str(msg)

        if len(msg) <= max_len_line:
            return msg

        word_list = msg.split(' ')
        output_list = []
        tail_word = ''
        current_len = 0
        for word in word_list:
            if len(output_list) <= current_len:
                output_list.append('')
            if current_len < max_lines:
                if len(output_list[current_len]+word+' ') < max_len_line:
                    if tail_word != '':
                        output_list[current_len] += f'{tail_word} {word} '
                        tail_word = ''
                    else:
                        output_list[current_len] += f'{word} '
                else:
                    tail_word = word
                    if current_len == (max_lines-1):
                        # last string contais '...' to show message truncation
                        # spaces will be trimmed
                        output_list[current_len] += word
                        output_list[current_len] = output_list[current_len][0:(max_len_line-2)].strip()+'&#133;'
                    current_len += 1
            else:
                break
        # If the allowed number of lines has been passed and there is a word left,
        # but we have not created an additional line in the output array,
        # then we add a line and throw this word there.
        if current_len < max_lines and tail_word != 0 and len(output_list) <= current_len:
            output_list.append('')
            output_list[current_len] += tail_word

        return ''.join(output_list)

    def parse_string_full_name(full_name: str) -> list:
        """ Function for parsing the full name string into its component parts.
            Takes into account that first and last names can be compound and must begin with capital letters.
            For example, Prokudina-Gorskaya Anna-Maria Fedorovna.
            In the patronymic, we capitalize only the first word, leaving the rest as the user wrote.
            If the user entered only one word, we assume that this is the Name.

        Args:
            full_name: input name.
        Returns:
            list, returned format:
            name_list[0] - Surname, name_list[1] - Name, name_list[2] - Patronymic.
        """
        if not full_name or full_name == '':
            raise_if_cond(True, 'Empty value of parsed name.')

        double_name, delimeter, i, parsed, result = False, False, -1, {0: '', 1: '', 2: ''}, []
        for item in full_name:
            # if the next char is a letter
            if item.isalpha():
                # since the next letter will now be printed, we print separators
                # if they were in the source text.
                if double_name:
                    parsed[i] += '-'
                elif delimeter and i == 2:
                    parsed[i] += ' '

                # select each new word if it is the first or immediately follows the separator.
                if (i == -1 or delimeter or double_name) and i < 2:
                    # the name must be capitalized.
                    item = item.upper()
                    # split into tokens only if there was no double name sign.
                    if not double_name:
                        i += 1
                else:
                    # that is not highlighted should be written with a small letter.
                    item = item.lower()

                # add a letter to the result.
                parsed[i] += item
                # reset the double name and delimiter features.
                double_name, delimeter = False, False
            else:
                # delimiters are only accepted after the first token.
                if i > -1:
                    # if there is a `-` character then it must be added to separate the double name.
                    if item == '-':
                        # set the double name flag.
                        double_name = True
                    if item == ' ':
                        # set the separator flag.
                        delimeter = True

        result = list(parsed.values())
        if i == -1:
            # interpret unparsed string as Name of person.
            return ['', full_name, '']

        return result


class Validators:
    """ Validator class.
    """
    def validate_inn(inn: str, kpp: str=None) -> list:
        """ Validation of the inn value in the context with the passed value kpp.

        Args:
            inn (str): inn string value
            kpp (str, optional): kpp string value. Defaults to None.

        Returns:
            list, returned format:
            valid_res[0] - is valid(bool), valid_res[1] - user_msg(str)
        """
        coefs = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
        if inn and len(inn) == 10:
            if sum(map(lambda x, y: x*int(y), coefs[2:], inn[:9])) % 11 % 10 != int(inn[9]):
                return False, 'Incorrect INN: "{}"'.format(inn)
        elif inn and len(inn) == 12:
            if (
                sum(map(lambda x, y: x*int(y), coefs[1:], inn[:10])) % 11 % 10 != int(inn[10])
                or
                sum(map(lambda x, y: x*int(y), coefs, inn[:11])) % 11 % 10 != int(inn[11])
            ):
                return False, 'Incorrect INN: "{}"'.format(inn)
            if kpp and len(kpp):
                return False, 'Entrepreneur with inn: "{}" kpp cannot be specified: "{}"'.format(inn, kpp)
        else:
            return False, 'Wrong inn lenght: {} (must be 10 or 12 characters)'.format(inn)
        return True, ''

    def validate_snils(snils: str, check_empty: bool=False) -> list:
        """ Validation of SNILS http://www.kholenkov.ru/data-validation/snils/

        Args:
            snils (str): SNILS string value
            check_empty (bool, optional): if True fills in the error text when SNILS is empty.

        Returns:
            list, returned format:
            valid_res[0] - is valid(bool), valid_res[1] - user_msg(str)
        """
        result = False
        error_msg = ''
        snils_text = str(snils)

        # SNILS cannot be '00000000000'
        if snils_text == '00000000000':
            error_msg = 'Invalid SNILS checksum.'
            return result, error_msg

        if len(snils_text) == 0:
            if check_empty:
                error_msg = 'SNILS value cannot be empty.'
        elif not ONLY_NUMBERS_SYMBOLS.match(snils_text):
            error_msg = 'The SNILS value must consist only of numbers.'
        elif len(snils_text) != 11:
            error_msg = 'SNILS value must contain 11 digits.'
        else:
            checksum = 0
            for i in range(9):
                checksum += int(snils_text[i]) * (9 - i)
            checkdigit = 0
            if checksum < 100:
                checkdigit = checksum
            elif checksum > 101:
                checkdigit = int(checksum % 101)
                if checkdigit == 100:
                    checkdigit = 0

            if checkdigit == int(snils_text[9:11]):
                result = True
            else:
                error_msg = 'Invalid SNILS checksum.'

        return result, error_msg
