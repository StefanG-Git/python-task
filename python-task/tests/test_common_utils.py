from unittest import TestCase

from utils.common_utils import get_color_code_by_number


class CommonUtilsTests(TestCase):
    _GREEN_COLOR_CODE = "007500"
    _ORANGE_COLOR_CODE = "FFA500"
    _RED_COLOR_CODE = "b30000"

    def test_get_color_code_by_number__when_number_is_less_than_3__expect_green_color_code(self):
        expected_result = self._GREEN_COLOR_CODE

        actual_result = get_color_code_by_number(2)

        self.assertEqual(expected_result, actual_result)

    def test_get_color_code_by_number__when_number_equals_3__expect_green_color_code(self):
        expected_result = self._GREEN_COLOR_CODE

        actual_result = get_color_code_by_number(3)

        self.assertEqual(expected_result, actual_result)

    def test_get_color_code_by_number__when_number_is_greater_than_3_and_less_than_12__expect_orange_color_code(self):
        expected_result = self._ORANGE_COLOR_CODE

        actual_result = get_color_code_by_number(6)

        self.assertEqual(expected_result, actual_result)

    def test_get_color_code_by_number__when_number_equals_12__expect_orange_color_code(self):
        expected_result = self._ORANGE_COLOR_CODE

        actual_result = get_color_code_by_number(12)

        self.assertEqual(expected_result, actual_result)

    def test_get_color_code_by_number__when_number_is_greater_than_12__expect_red_color_code(self):
        expected_result = self._RED_COLOR_CODE

        actual_result = get_color_code_by_number(13)

        self.assertEqual(expected_result, actual_result)
