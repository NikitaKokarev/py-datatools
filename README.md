# py-datatools
## Helper functions for efficient work with common tasks
___
## How to use:
Write your Python code and use these functions make it cleaner.
___
## Examples:
### Common Functions:
Execute callable object if condition statement is True:
```python
from py_datatools import exec_if_cond

condition = True

>>> exec_if_cond(condition, print, 'done', 'well')

done well
```
Raise exception if condition statement is True:
```python
from py_datatools import raise_if_cond

condition = True

>>> raise_if_cond(condition, 'value error', ValueError)

Traceback (most recent call last):
  File "<string>", line 1, in <module>
  ...
  raise exc_class(error_msg)
ValueError: value error

>>> raise_if_cond(condition, 'msg')

Traceback (most recent call last):
  File "<string>", line 1, in <module>
  ...
  raise exc_class(error_msg)
Exception: msg
```
Trying to cast a predefined value to boolean True:
```python
from py_datatools import try_true

>>> try_true('true')

True

>>> try_true('y')

True
```
Trying to cast a predefined value to boolean False:
```python
from py_datatools import try_false

>>> try_false('FAlSe')

False

>>> try_false('N')

False
```
Trying to cast a predefined value to boolean:
```python
from py_datatools import try_bool

>>> try_bool('T')

True

>>> try_bool('0')

False
```
PREDEFINED_TRUE_ARRAY = ("true", "t", "1", "yes", "y")
PREDEFINED_FALSE_ARRAY = ("false", "f", "0", "no", "n")
___
### Collections:
Unpackage the first element that casts to True. If all elems cast to False, then return the last element:
```python
from py_datatools import Collections

>>> Collections.coalesce(0, 0, False, 'False', 1)

'False'

>>> Collections.coalesce(0, 0, False)

False
```
Get only unique subelements that can be non-hashable types. Strongly typed matches only!:
```python
from py_datatools import Collections

>>> Collections.distinct(0, [0, 0, 0], False, 'False', (0, 0, 0), [0, 0, 0], 1)

[0, [0, 0, 0], False, 'False', (0, 0, 0), 1]

>>> Collections.distinct(10, False, 12, 13, {1, 1, 1}, 0, 4, 12, 6, 7)

[10, False, 12, 13, {1}, 0, 4, 6, 7]
```
Subtract beta from alfa and return a difference list:
```python
from py_datatools import Collections

>>> Collections.get_diff_list(
    [0, 0, 0, {1:2, 3:4}, 8, 9],
    (0, 0, {3, 4}, 0, 6, 7)
)

[{1: 2, 3: 4}, 8, 9]

>>> Collections.get_diff_list(
    [
        (1,),
        (1,),
        (1,),
        (1,),
        {1:2, 3:4},
        8,
        9
    ],
    ((2,), (0,), {3, 4}, (-1,), 6, 7),
    distinct=True
)

[(1,), {1: 2, 3: 4}, 8, 9]
```
Calculate an intersection as common unique elements:
```python
from py_datatools import Collections

>>> Collections.get_common_uniques(
    [0, 0, 0, {1:2, 3:4}, 8, 9, (8,), 0, 0, (8,)],
    (0, 0, {3, 4}, 0, 6, 7, (8,))
)

[0, (8,)]
```
True if all distinct elements of alfa belong to elements as beta:
```python
from py_datatools import Collections

>>> Collections.is_subset([0, 0, 0], (0, 0, {3, 4}, 0, 6, 7, (8,)))

True

>>> Collections.is_subset([0, 0, 0, 1], (0, 0, {3, 4}, 0, 6, 7, (8,)))

False
```
Split an array into parts of custom length:
```python
from py_datatools import Collections

>>> ans_gen = Collections.split_sequence_gen([0, 0, 0, {1:2, 3:4}, 8, 9], 4)

>>> for item in ans_gen:
        print(item)

[0, 0, 0, {1: 2, 3: 4}]
[8, 9]

>>> ans_gen = Collections.split_sequence_gen('0,0,d0,f', 2)

>>> for item in ans_gen:
        print(item)

0,
0,
d0
,f
```
Extract elements of subcollections inside:
```python
from py_datatools import Collections

>>> Collections.extract_subelements(
    {0: [0, 0, 0], 1: {1:2, 3:4}, 2: [8, 9]}
)

[0, 0, 0, {1: 2, 3: 4}, 8, 9]

>>> Collections.extract_subelements(
    [(1, 2), (1, 4), (1, 5), (1, 1), {1:2, 3:4}, [8, 9], '2,1'],
    unique_items_only=True
)

[1, 2, 4, 5, {1: 2, 3: 4}, 8, 9, '2,1']
```
___
### Numbers:
Unpackage the first element that casts to True. If all elems cast to False, then return the last element:
```python
from py_datatools import Numbers

>>> Numbers.parse_int(b'2')

50
```
Try to get a int number:
```python
from py_datatools import Numbers

>>> Numbers.try_int('2')

2

>>> Numbers.try_int(2.1)

2
```
Try to get a float number:
```python
from py_datatools import Numbers

>>> Numbers.try_float('2.1')

2.1

>>> Numbers.try_float(2)

2.0
```
Creates a formatted counter of type 2.0M, 1.3K from an integer:
```python
from py_datatools import Numbers

>>> Numbers.get_formatted_tooltip(1001)

1K

>>> Numbers.get_formatted_tooltip(100000)

100K

>>> Numbers.get_formatted_tooltip(999500)

1M
```
Random number generator from random n-bits with increment +1:
```python
from py_datatools import Numbers

>>> gen_func = Numbers.unique_id(8)
>>> next(gen_func)

213
>>> next(gen_func)

214
```
Get numbers in str, without the risk of injections or errors, then paste them into the request:
```python
from py_datatools import Numbers

>>> Numbers.digitize_string('-a034h3kl56,78;')

'-03435678'
```
___
### Text:
Trims long lines taking into account word wraps:
```python
from py_datatools import Text

>>> Text.crop_text_line_by_line(
        'long line longline long2line2long2 linelongline',
        max_lines=100,
        max_len_line=10
    )

'long line longline linelongline'
```
Function for parsing the full name string into its component parts:
```python
from py_datatools import Text

>>> Text.parse_string_full_name('surname Name patronymic')

['Surname', 'Name', 'Patronymic']

>>> Text.parse_string_full_name('surname Double-name patronymic')

['Surname', 'Double-Name', 'Patronymic']
```
___
### Validators:
Validation of the inn value in the context with the passed value kpp:
```python
from py_datatools import Validators

>>> Validators.validate_inn('7727563778')

(True, '')

>>> Validators.validate_inn('7727563778666')

(False, 'Wrong inn lenght: 7727563778666 (must be 10 or 12 characters)')
```
Validation of SNILS http://www.kholenkov.ru/data-validation/snils/:
```python
from py_datatools import Validators

>>> Validators.validate_snils('08336732477')

(True, '')
```
___
### SQLHelper
DTO. Enum with PostgreSQL data types:
```python
from py_datatools import SQLHelper

>>> SQLHelper.PgSqlType.INT16.value

'smallint'
```
Decorator for preparing SQL queries for logging:
```python
from py_datatools import SQLHelper

>>> SQLHelper.prepare_sql

<function SQLHelper.prepare_sql at ...>
```
Method for logging full sql query:
```python
"""
@prepare_sql
def logging_sql(query: str, qty_lines: int=20000) -> list:
    ...
"""
from py_datatools import SQLHelper

>>> SQLHelper.logging_sql()

[' \'"1" =>\' "2NULL ']
```
The method converts a hstore format string to a dict:
```python
from py_datatools import SQLHelper

>>> SQLHelper.hstore_to_dict(''' "1" => "2" ''')

{'1': '2'}
```
The method converts the hstore format string into a dict and nested entries:
```python
from py_datatools import SQLHelper

>>> SQLHelper.hstore_to_dict_recursive(''' "key1" => "value1", "key2" => "value2" ''')

{'key1': 'value1', 'key2': 'value2'}
```
___
### Datetime helper
```python
from py_datatools import (
    is_period_week,
    is_period_month,
    is_period_quarter,
    is_period_half_year,
    is_period_year,
    is_period_day,
    is_period_other,
    get_some_days_ago,
    get_current_dot_position,
    get_begin_period,
    get_end_period,
    get_default_datebegin,
    get_default_dateend,
    to_start_of_month,
    to_start_of_hour,
    to_end_of_month,
    to_end_of_day,
    to_begin_of_day,
    to_begin_of_year,
    to_end_of_year,
    to_start_of_prev_month,
    is_full_month,
    is_eq_year,
    is_eq_month,
    is_eq_two_month,
    get_prev_date_by_month,
    in_current_period,
    is_last_month_day,
    is_first_month_day,
    begin_of_current_quarter,
    end_of_current_quarter,
    timedelta_months,
    get_quarter_name,
    get_infinity_date,
    delta_month_two_period,
    split_dates_for_aggregate,
    get_left_for_aggregate,
    get_right_for_aggregate
)
```
___
## Install package:
```
pip3 install git+https://github.com/NikitaKokarev/py-datatools
```
