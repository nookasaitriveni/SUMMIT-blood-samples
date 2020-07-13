from unittest import TestCase

from indigo.utils import get_page_numbers


class GetPageNumbersTestCase(TestCase):
    def test_show_all_when_below_threshold(self):
        self.assertSequenceEqual(get_page_numbers(1, 5), range(1, 6))
        self.assertSequenceEqual(get_page_numbers(3, 5), range(1, 6))
        self.assertSequenceEqual(get_page_numbers(5, 5), range(1, 6))

    def test_show_all_when_at_threshold(self):
        self.assertSequenceEqual(get_page_numbers(1, 11), range(1, 12))
        self.assertSequenceEqual(get_page_numbers(6, 11), range(1, 12))
        self.assertSequenceEqual(get_page_numbers(11, 11), range(1, 12))

    def test_collapse_on_both_sides_for_middle_page(self):
        self.assertSequenceEqual(
            get_page_numbers(5, 9, extremes=1, arounds=1),
            [1, None, 4, 5, 6, None, 9]
        )

    def test_collapse_middle_for_first_page(self):
        self.assertSequenceEqual(
            get_page_numbers(1, 20),
            [1, 2, 3, 4, None, 19, 20]
        )

    def test_collapse_middle_for_last_page(self):
        self.assertSequenceEqual(
            get_page_numbers(20, 20),
            [1, 2, None, 17, 18, 19, 20]
        )

    def test_fill_in_single_gaps(self):
        self.assertSequenceEqual(
            get_page_numbers(4, 7, extremes=1, arounds=1),
            range(1, 8),
        )
