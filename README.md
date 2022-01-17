# py-regulars
## Helper functions for efficient work with common tasks
___
## How to use:
Write your Python code and use these functions make it cleaner.
___
## Examples:
### Common Functions:
Execute callable object if condition statement is True:
```python
from py_regulars import exec_if_cond

condition = True

>>> exec_if_cond(condition, print, 'done', 'well')

done well
```
Raise exception if condition statement is True:
```python
from py_regulars import raise_if_cond

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
___
### Collations:
Trying to cast a predefined value to boolean True:
```python
from py_regulars import Collations

>>> Collations.try_true('true')

True

>>> Collations.try_true('y')

True
```
Trying to cast a predefined value to boolean False:
```python
from py_regulars import Collations

>>> Collations.try_false('FAlSe')

False

>>> Collations.try_false('N')

False
```
Trying to cast a predefined value to boolean:
```python
from py_regulars import Collations

>>> Collations.try_bool('T')

True

>>> Collations.try_bool('0')

False
```
PREDEFINED_TRUE_ARRAY = ("true", "t", "1", "yes", "y")  
PREDEFINED_FALSE_ARRAY = ("false", "f", "0", "no", "n")
___
### Collections:
Unpackage the first element that casts to True. If all elems cast to False, then return the last element:
```python
from py_regulars import Collections

>>> Collections.coalesce(0, 0, False, 'False', 1)

'False'

>>> Collections.coalesce(0, 0, False)

False
```
Get only unique subelements that can be non-hashable types. Strongly typed matches only!:
```python
from py_regulars import Collections

>>> Collections.distinct(0, [0, 0, 0], False, 'False', (0, 0, 0), [0, 0, 0], 1)

[0, [0, 0, 0], False, 'False', (0, 0, 0), 1]

>>> Collections.distinct(10, False, 12, 13, {1, 1, 1}, 0, 4, 12, 6, 7)

[10, False, 12, 13, {1}, 0, 4, 6, 7]
```
Subtract beta from alfa and return a difference list:
```python
from py_regulars import Collections

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
from py_regulars import Collections

>>> Collections.get_common_uniques(
    [0, 0, 0, {1:2, 3:4}, 8, 9, (8,), 0, 0, (8,)],
    (0, 0, {3, 4}, 0, 6, 7, (8,))
)

[0, (8,)]
```
True if all distinct elements of alfa belong to elements as beta:
```python
from py_regulars import Collections

>>> Collections.is_subset([0, 0, 0], (0, 0, {3, 4}, 0, 6, 7, (8,)))

True

>>> Collections.is_subset([0, 0, 0, 1], (0, 0, {3, 4}, 0, 6, 7, (8,)))

False
```
Split an array into parts of custom length:
```python
from py_regulars import Collections

>>> ans_gen = Collections.split_sequence_gen([0, 0, 0, {1:2, 3:4}, 8, 9], 4)

>>> for item in ans_gen:
        print(item)

[0, 0, 0, {1: 2, 3: 4}]
[8, 9]

>>> ans_gen = Collections.split_sequence_gen('0,0,d0,fgderg8_ytert9(9)', 2)

>>> for item in ans_gen:
        print(item)
        
0,
0,
d0
,f
gd
er
g8
_y
te
rt
9(
9)
```
Extract elements of subcollections inside:
```python
from py_regulars import Collections

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
## Install package:
```
pip3 install git+https://github.com/NikitaKokarev/py-regulars
```