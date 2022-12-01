from datetime import datetime
from unittest import TestCase

from utils.datetime_utils import *


class DatetimeUtilsTests(TestCase):
    _DASH_SEPARATED_DATE_FORMAT = "%Y-%m-%d"
    _SLASH_SEPARATED_DATE_FORMAT = "%Y/%m/%d"

    _DASH_SEPARATED_DATE_AS_STR = "2022-02-11"
    _SLASH_SEPARATED_DATE_AS_STR = "2022/02/22"

    _SAME_MONTH_START_DATE_AS_STR = "2022-05-11"
    _SAME_MONTH_END_DATE_AS_STR = "2022-05-30"

    _DIFF_MONTH_START_DATE_AS_STR = "2022-01-11"
    _DIFF_MONTH_END_DATE_AS_STR = "2022-05-30"

    _DIFF_YEAR_START_DATE_AS_STR = "2021-01-11"
    _DIFF_YEAR_END_DATE_AS_STR = "2022-01-12"

    def test_string_to_date__when_date_is_separated_with_dashes__expect_to_be_converted_to_date_object(self):
        expected_result = datetime.strptime(self._DASH_SEPARATED_DATE_AS_STR, self._DASH_SEPARATED_DATE_FORMAT).date()

        actual_result = string_to_date(self._DASH_SEPARATED_DATE_AS_STR)

        self.assertEqual(expected_result, actual_result)

    def test_string_to_date__when_date_is_separated_with_slashes__expect_to_be_converted_to_date_object(self):
        expected_result = datetime.strptime(self._SLASH_SEPARATED_DATE_AS_STR, self._SLASH_SEPARATED_DATE_FORMAT).date()

        actual_result = string_to_date(self._SLASH_SEPARATED_DATE_AS_STR)

        self.assertEqual(expected_result, actual_result)

    def test_get_months_diff_between_dates__when_dates_are_in_same_month__expect_0_months_diff(self):
        expected_result = 0

        start_date = string_to_date(self._SAME_MONTH_START_DATE_AS_STR)
        end_date = string_to_date(self._SAME_MONTH_END_DATE_AS_STR)
        actual_result = get_months_diff_between_dates(start_date, end_date)

        self.assertEqual(expected_result, actual_result)

    def test_get_months_diff_between_dates__when_dates_are_in_diff_months__expect_correct_months_diff(self):
        expected_result = 4

        start_date = string_to_date(self._DIFF_MONTH_START_DATE_AS_STR)
        end_date = string_to_date(self._DIFF_MONTH_END_DATE_AS_STR)
        actual_result = get_months_diff_between_dates(start_date, end_date)

        self.assertEqual(expected_result, actual_result)

    def test_get_months_diff_between_dates__when_period_between_dates_is_one_year__expect_12_months_diff(self):
        expected_result = 12

        start_date = string_to_date(self._DIFF_YEAR_START_DATE_AS_STR)
        end_date = string_to_date(self._DIFF_YEAR_END_DATE_AS_STR)
        actual_result = get_months_diff_between_dates(start_date, end_date)

        self.assertEqual(expected_result, actual_result)
