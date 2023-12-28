# -*- coding: utf-8 -*-

"""
INIT PY_DATATOOLS
~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2022 by Nikita Kokarev.
:license: GNU General Public License v3 (GPLv3), see LICENSE for more details.
"""
__author__ = 'kokarev.nv'

from .py_datatools import (
    exec_if_cond, raise_if_cond, try_true, try_false, try_bool, Collections, Numbers, Text, CKey, Validators,
    SQLHelper
)
from .dt_helper import (
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
