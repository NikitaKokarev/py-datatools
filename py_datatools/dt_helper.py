# -*- coding: utf-8 -*-
""" HANDLER FOR WORKING WITH DT PERIODS.
"""
__author__ = 'kokarev.nv'

from typing import Tuple
from datetime import date, timedelta, datetime
import calendar

PERIOD_TYPE_HOUR = 'hour'
PERIOD_TYPE_MONTH = 'month'
PERIOD_TYPE_YEAR = 'year'
PERIOD_TYPE_WEEK = 'week'
PERIOD_TYPE_DAY = 'day'
PERIOD_TYPE_QUARTER = 'quarter'
PERIOD_TYPE_HALF_YEAR = 'halfyear'


def is_period_week(begin: date, end: date) -> bool:
    """ Check for a period of a week.

    Args:
        begin: beginning
        end: end
    Returns:
        Is the period a week
    """
    wd_begin = begin.weekday()
    wd_end = end.weekday()
    return ((end - begin) < timedelta(7) and wd_begin <= wd_end)


def is_period_month(begin: date, end: date) -> bool:
    """ Check for a period of a month.

    Args:
        begin: beginning
        end: end
    Returns:
        Is the period month
    """
    dt_begin = to_start_of_month(begin)
    dt_end = to_end_of_month(end)
    return (
        begin == dt_begin and
        end == dt_end and
        begin.month == end.month and
        begin.year == end.year
    )


def is_period_quarter(begin: date, end: date) -> bool:
    """ Check for the period - quarter.

    Args:
        begin: beginning
        end: end
    Returns:
        Is the period a quarter.
    """
    dt_begin = to_start_of_month(begin)
    dt_end = to_end_of_month(end)
    return (
        begin == dt_begin and
        end == dt_end and
        begin.month in (1, 4, 7, 10) and
        begin.month + 2 == end.month and
        begin.year == end.year
    )


def is_period_half_year(begin: date, end: date) -> bool:
    """ Check for a period of six months.

    Args:
        begin: beginning
        end: end
    Returns:
        Is the period half a year.
    """
    dt_begin = to_start_of_month(begin)
    dt_end = to_end_of_month(end)
    return (
        begin == dt_begin and
        end == dt_end and
        begin.month in (1, 7) and
        begin.month + 5 == end.month and
        begin.year == end.year
    )


def is_period_year(begin: date, end: date) -> bool:
    """ Check for a period of one year.

    Args:
        begin: beginning
        end: end
    Returns:
        Is the period a year
    """
    dt_begin = to_begin_of_year(begin)
    dt_end = to_end_of_year(end)
    return (
        begin == dt_begin and
        end == dt_end and
        begin.year == end.year
    )


def is_period_day(begin: date, end: date) -> bool:
    """ Check for period - day.

    Args:
        begin: beginning
        end: end
    Returns:
        Is the period day
    """
    return begin == end


def is_period_other(begin: date, end: date) -> bool:
    """ Check for a dimension period of 1 day.

    Args:
        begin: beginning
        end: end
    Returns:
        Is the period from 1 day
    """
    return timedelta(days=1) <= end - begin


def get_some_days_ago(date_: date, days_count: int):
    """ Returns date = passed date - number of days.

    Args:
        date_: passed date
        days_count: days passed
    Returns:
        Date how many days have passed
    """
    return date_ - timedelta(days=days_count)


def get_current_dot_position(date_begin: date, _date_end: date, date_begin_analyze: date, today: date) -> date:
    """ Calculate the day in the past period corresponding to today.

    Args:
        date_begin: start date
        _date_end: end date
        date_begin_analyze: start date of analysis
        today: today
    Returns:
        norm_pos_date: calculated day
    """
    norm_pos_month = date_begin.month + (today.month - date_begin_analyze.month)
    # Maximum day in a month
    max_day = calendar.monthrange(date_begin.year, norm_pos_month)[1]

    # If the current day is longer than there can be in a month, leave the last day of the month.
    norm_pos_day = max_day if today.day > max_day else today.day
    norm_pos_date = date(date_begin.year, norm_pos_month, norm_pos_day)

    return norm_pos_date


def get_begin_period(date_begin: date, type_period: str = PERIOD_TYPE_MONTH) -> [date, date]:
    """ Calculate the beginning of the period.

    Args:
        date_begin: start date
        type_period: period type
    Returns:
        Start and end dates
    """
    date_begin_new = None
    if type_period == PERIOD_TYPE_MONTH:
        date_begin_new = date_begin.replace(day=1)
    if type_period == PERIOD_TYPE_YEAR:
        date_begin_new = date_begin.replace(month=1, day=1)
    return date_begin_new, date_begin


def get_end_period(date_end: date, type_period: str = PERIOD_TYPE_MONTH) -> [date, date]:
    """ Calculate the end of the period.

    Args:
        date_end: start date
        type_period: period type
    Returns:
        Start and end dates
    """
    date_end_new = None
    if type_period == PERIOD_TYPE_DAY:
        date_end_new = date_end
    if type_period == PERIOD_TYPE_WEEK:
        date_end_new = date_end + timedelta(weeks=1, days=-1)
    if type_period == PERIOD_TYPE_MONTH:
        month = date_end.month + 1 if date_end.month < 12 else 1
        year = date_end.year if date_end.month < 12 else date_end.year + 1
        date_end_new = date_end.replace(year=year, month=month, day=1) - timedelta(days=1)
    if type_period == PERIOD_TYPE_QUARTER:
        date_end_new = end_of_currant_quarter(date_end)
    if type_period == PERIOD_TYPE_YEAR:
        date_end_new = date_end.replace(year=date_end.year+1, month=1, day=1) - timedelta(days=1)
    date_begin, date_end = date_end, date_end_new
    return date_begin, date_end


def get_default_datebegin() -> date:
    """ Returns the default start date.

    Returns:
        standard start date
    """
    return date(1970, 1, 1)


def get_default_dateend() -> date:
    """ Returns the standard end date.

    Returns:
        standard end date
    """
    return date(2070, 12, 31)


def to_start_of_month(date_: date) -> date:
    """ Based on the passed date, returns the start date of the current month.

    Args:
        date_: date
    Returns:
        start date of the current month
    """
    return date(year=date_.year, month=date_.month, day=1)


def to_start_of_hour(date_time_: datetime) -> date:
    """ Based on the passed date, time, returns the date and time of the beginning of the hour.

    Args:
        date_time_: date time
    Returns:
        start date of the current month
    """
    return datetime(year=date_time_.year, month=date_time_.month, day=date_time_.day, hour=date_time_.hour)


def to_end_of_month(date_: date) -> date:
    """ Based on the passed date, returns the end date of the month.

    Args:
        date_: date
    Returns:
        end date of the current month
    """
    result = to_start_of_month(date_) + timedelta(days=32)
    return result - timedelta(days=result.day)


def to_end_of_day(date_: date) -> datetime:
    """ Based on the passed date, returns the date and time at 23:59:59

    Args:
        date_: date
    Returns:
        date and time of the end of the current day
    """
    return datetime.combine(date_, datetime.max.time())


def to_begin_of_day(date_: date) -> datetime:
    """ Based on the passed date, returns the date and time at 00:00:00

    Args:
        date_: date
    Returns:
        date and time of the end of the current day
    """
    return datetime.combine(date_, datetime.min.time())


def to_begin_of_year(date_: date) -> date:
    """ Start date of the year.

    Args:
        date_: date
    Returns:
        start date of the year
    """
    return date(year=date_.year, month=1, day=1)


def to_end_of_year(date_: date) -> date:
    """ End of year date.

    Args:
        date_: date
    Returns:
        end of year date
    """
    return date(year=date_.year, month=12, day=31)


def to_start_of_prev_month(date_: date) -> date:
    """ Based on the passed date, returns the start date of the previous month.

    Args:
        date_: date
    Returns:
        start date of the previous month
    """
    return (date_ - timedelta(days=date_.day)).replace(day=1)


def is_full_month(datebegin: date, dateend: date) -> bool:
    """ The method checks whether the period is a full month.

    Args:
        datebegin: start date
        dateend: end date
    Returns:
        is the period a full month.
    """
    begin = to_start_of_month(datebegin)
    end = to_end_of_month(dateend)
    return begin.day == datebegin.day and end.day == dateend.day


def is_eq_year(datebegin: date, dateend: date) -> bool:
    """ The method checks whether the period is a full year.

    Args:
        datebegin: start date
        dateend: end date
    Returns:
        is the period a full year.
    """
    if not(datebegin and dateend):
        return False
    if isinstance(datebegin, str):
        try:
            datebegin = datetime.strptime(datebegin, '%d.%m.%Y')
        except ValueError:
            datebegin = datetime.strptime(datebegin, '%Y-%m-%d')
    if isinstance(dateend, str):
        try:
            dateend = datetime.strptime(dateend, '%d.%m.%Y')
        except ValueError:
            dateend = datetime.strptime(dateend, '%Y-%m-%d')
    datebegin_year = date(datebegin.year, 1, 1)
    dateend_year = date(dateend.year, 12, 31)
    return datebegin == datebegin_year and dateend == dateend_year


def is_eq_month(datebegin: date, dateend: date) -> bool:
    """ The method checks whether the period is greater than a month.
        If the Month is a whole month, then it is suitable for constructing using aggregates or
        counting using formulas.

        Formula: Date of the left period < first day of the right period - number of days
        in the month of the left period.
        “the first day of the right period” - because to obtain aggregates for the month,
        it is necessary that the period be more than a month.
        In such cases, if a period of 1 month + 1 day is selected, then we will build by aggregates.
        Or if a full month falls within the selected period.

    Args:
        datebegin: start date
        dateend: end date
    Returns:
        is the period more than a month
    """
    if not(datebegin and dateend):
        return False

    is_border_period = (datebegin < to_start_of_month(dateend) and is_last_month_day(dateend)
                        or is_first_month_day(datebegin) and dateend > to_end_of_month(datebegin))

    return (datebegin == to_start_of_month(dateend) and to_end_of_month(datebegin) == dateend
            or datebegin < to_start_of_month(dateend) - timedelta(days=to_end_of_month(datebegin).day - 1)
            or is_border_period)


def is_eq_two_month(datebegin: date, dateend: date) -> bool:
    """ The method checks whether the period is two months.

    Args:
        datebegin: start date
        dateend: end date
    Returns:
        is the period two months
    """
    if not(datebegin and dateend):
        return False
    return datebegin + timedelta(days=30) == to_start_of_month(dateend)


def get_prev_date_by_month(datebegin: date, quant: str) -> date:
    """ Method for calculating the date a month or a day ago for the very first date, depending on the quantum.

    Args:
        datebegin: start date
        quant: quantum
    Returns:
        date one month or day ago for the very first date.
    """
    delta = timedelta(days=1) if quant == PERIOD_TYPE_DAY else timedelta(days=to_end_of_month(datebegin).day)

    if datebegin.month - (datebegin - delta).month == 2:
        if datebegin.month != 1:
            rs_date = datetime(year=datebegin.year, month=datebegin.month - 1, day=datebegin.day).date()
        else:
            rs_date = datetime(year=datebegin.year - 1, month=12, day=datebegin.day).date()
    else:
        rs_date = datebegin - delta
    return rs_date


def in_current_period(datebegin: date, dateend: date) -> bool:
    """ The method checks whether we are in a period or not, relative to the current date.

    Args:
        datebegin: start date
        dateend: end date
    Returns:
        are we in the period or not, relative to the current date.
    """
    return datebegin <= datetime.now().date() <= dateend


def is_last_month_day(day: date) -> bool:
    """ The method checks whether the last day of the month is passed.

    Args:
        day: date
    Returns:
        Is the last day of the month transmitted.
    """
    return (day + timedelta(days=1)).month != day.month


def is_first_month_day(day: date) -> bool:
    """ The method checks whether the first day of the month is passed.

    Args:
        day: date
    Returns:
        Is the first day of the month transmitted.
    """
    return (day - timedelta(days=1)).month != day.month


def begin_of_currant_quarter(currant_date: date) -> date:
    """ The method finds the start date of the quarter in which the current date falls.

    Args:
        current_date: current date
    Returns:
        quarter start date
    """
    # находим даты начал кварталов текущего года
    currant_quarter = date(year=currant_date.year, month=1, day=1)
    second_quarter = date(year=currant_date.year, month=4, day=1)
    third_quarter = date(year=currant_date.year, month=7, day=1)
    fourth_quarter = date(year=currant_date.year, month=10, day=1)
    # отбираем дату квартала, в промежуток которой попала текущая дата
    if fourth_quarter <= currant_date:
        currant_quarter = fourth_quarter
    elif third_quarter <= currant_date:
        currant_quarter = third_quarter
    elif second_quarter <= currant_date:
        currant_quarter = second_quarter
    return currant_quarter


def end_of_currant_quarter(currant_date: date) -> date:
    """ The method finds the last date of the quarter in which the current date falls.

    Args:
        current_date: date
    Returns:
        last date of the quarter
    """
    begin_quarter = begin_of_currant_quarter(currant_date)
    return to_end_of_month(date(year=begin_quarter.year, month=begin_quarter.month + 2, day=1))


def timedelta_months(sourcedate: str, months: int) -> timedelta:
    """ The method calculates timedelta for the passed months.

    Args:
        sourcedate: Source date
        months: Number of months in which to count days
    Returns:
        timedelta - how many days need to be added to get the specified number of months
    """
    new_date = sourcedate
    if isinstance(new_date, str):
        new_date = datetime.strptime(new_date, '%d.%m.%Y').date()
    if isinstance(new_date, int):
        new_date = datetime.strptime(str(new_date), '%Y%m%d').date()
    month = new_date.month - 1 + months
    year = new_date.year + month // 12
    month = month % 12 + 1
    day = min(new_date.day, calendar.monthrange(year, month)[1])
    delta = date(year, month, day) - new_date - timedelta(days=1)
    return delta


def get_quarter_name(currant_date: date) -> str:
    """ Return the name of the quarter (Roman numeral).

    Args:
        current_date: date
    Returns:
        name of the quarter
    """
    date_name = None
    if 1 <= currant_date.month < 4:
        date_name = 'I'
    elif 4 <= currant_date.month < 7:
        date_name = 'II'
    elif 7 <= currant_date.month < 10:
        date_name = 'III'
    elif 10 <= currant_date.month:
        date_name = 'IV'
    return date_name


def get_infinity_date(currant_date) -> date:
    """ Return the maximum date if currant_date is infinity.

    Args:
        current_date: date
    Returns:
        maximum date
    """
    if isinstance(currant_date, str):
        if currant_date == 'infinity' or currant_date is None:
            currant_date = date(9999, 12, 31)
        else:
            currant_date = datetime.strptime(currant_date, "%Y-%m-%d").date()

    return currant_date


def delta_month_two_period(first: datetime, second: datetime) -> int:
    """ The method counts how many months are between 2 dates.

    Args:
        first: Date
        second: Date
    Returns:
        Number of months between dates
    """
    if not first or not second:
        return 0
    if first > second:
        first, second = second, first
    delta = 0
    while True:
        mdays = calendar.monthrange(first.year, second.month)[1]
        first += timedelta(days=mdays)
        if first <= second:
            delta += 1
        else:
            break
    return delta


def split_dates_for_aggregate(date_begin: date, date_end: date) -> Tuple[date, date, date, date, date, date]:
    """ The method generates dates for the left, central and right periods for construction using monthly aggregates.

    Args:
        date_begin: period start date
        date_end: period end date
    Returns:
        Start date of the left period,
        End date of the left period,
        Start date of the central period,
        End date of the central period,
        Start date of the right period,
        End date of the right period
    """
    begin_left = end_left = begin_center = end_center = begin_right = begin_end = None
    if date_begin and date_end:
        begin_left, end_left, begin_center = get_left_for_aggregate(date_begin, date_end)
        end_center, begin_right, begin_end = get_right_for_aggregate(date_begin, date_end, end_left)
    return begin_left, end_left, begin_center, end_center, begin_right, begin_end


def get_left_for_aggregate(date_begin: date, date_end: date) -> Tuple[date, date, date]:
    """ The method generates the start date of the central period, the start date and the end date of the left period.
        To build by aggregates. Works on a monthly basis.

    Args:
        date_begin: period start date
        date_end: period end date
    Returns:
        Left period start date, Left period end date, Center period start date.
    """
    begin_left = end_left = begin_center = None
    if date_begin:
        date_begin_left, date_end_left = get_end_period(date_begin)
        date_end_left = min(date_end, date_end_left)
        if date_begin_left != to_start_of_month(date_begin):
            begin_left = date_begin_left
            end_left = date_end_left

            if date_end_left != date_end:
                begin_center = date_end_left + timedelta(days=1)

        elif is_eq_month(date_begin, date_end):
            begin_center = date_begin_left
    return begin_left, end_left, begin_center


def get_right_for_aggregate(date_begin: date, date_end: date, date_end_left: date) -> Tuple[date, date, date]:
    """ The method generates the end date of the central period, the start date and the end date of the right period.
        To build by aggregates. Works on a monthly basis.
    Args:
        date_begin: period start date
        date_end: period end date
        date_end_left: end date of the left period (needed so as not to conflict with the left period,
                                                if they are building in the middle of the month)
    Returns:
        End date of the central period, Start date of the right period, End date of the right period
    """
    end_center = begin_right = begin_end = None
    date_begin_right, date_end_right = get_begin_period(date_end)
    if date_end_left != date_end_right:
        if to_end_of_month(date_end) != date_end_right:
            begin_right = date_begin_right
            begin_end = date_end_right

            if date_begin_right != date_begin:
                end_center = date_begin_right - timedelta(days=1)

        elif is_eq_month(date_begin, date_end):
            end_center = date_end_right
    return end_center, begin_right, begin_end
