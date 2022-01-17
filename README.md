# py-regulars
## Helper functions for efficient work with common tasks
___
## How to use:
Write your Python code and use these functions make it cleaner.
___
## Examples:
:
```python
from query_formatter import SqlEscaper, QueryFormatter

tmpl =  """ 
    SELECT *
    FROM table1
    WHERE col_name1 = 1
    {input_value:if:
        OR 
        col_name2 = 10 AND 
        EXISTS(
            SELECT t2.id
            FROM table2 t2
            WHERE t2.col_name1 = 100
            LIMIT 1
        )
    }
    OR col_name3 = 100
"""
input_value = 10

QF = QueryFormatter(SqlEscaper())
ans = QF.format(tmpl, input_value=input_value)

>>> print(ans)

SELECT *
FROM table1
WHERE col_name1 = 1

    OR
    col_name2 = 10 AND
    EXISTS(
        SELECT t2.id
        FROM table2 t2
        WHERE t2.col_name1 = 100
        LIMIT 1
    )

OR col_name3 = 100
```
In the next case, input value is checked to in the sequence of values and constant string was added to the template with a condition:
```python
from query_formatter import SqlEscaper, QueryFormatter

tmpl =  """ 
    SELECT *
    FROM table1
    WHERE col_name1 = 1
    {input_value:in:10,20,30,100
        OR col_name2 = 10 
    }
"""
input_value = 10

QF = QueryFormatter(SqlEscaper())
ans = QF.format(tmpl, input_value=input_value)

>>> print(ans)

SELECT *
    FROM table1
    WHERE col_name1 = 1
    
        OR col_name2 = 10
```
___
## Install package:
```
pip3 install git+https://github.com/NikitaKokarev/query-formatter
```