import numpy as np
import pandas as pd
import unittest
from klib.utils import _drop_duplicates
from klib.utils import _missing_vals
from klib.utils import _validate_input_0_1
from klib.utils import _validate_input_bool

if __name__ == '__main__':
    unittest.main()


class Test__drop_duplicates(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data_dupl_df = pd.DataFrame([[pd.NA, pd.NA, pd.NA, pd.NA],
                                         [1, 2, 3, 4],
                                         [1, 2, 3, 4],
                                         [1, 2, 3, 4],
                                         [2, 3, 4, 5],
                                         [1, 2, 3, pd.NA],
                                         [pd.NA, pd.NA, pd.NA, pd.NA]])

    def test_drop_dupl(self):
        # Test dropping of duplicate rows
        self.assertAlmostEqual(_drop_duplicates(self.data_dupl_df)[0].shape, (4, 4))
        # Test if the resulting DataFrame is equal to using the pandas method
        self.assertTrue(_drop_duplicates(self.data_dupl_df)[0].equals(self.data_dupl_df.drop_duplicates()))
        # Test number of duplicates
        self.assertEqual(len(_drop_duplicates(self.data_dupl_df)[1]), 3)


class Test__missing_vals(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data_mv_df = pd.DataFrame([[1, np.nan, 3, 4],
                                       [None, 4, 5, None],
                                       ['a', 'b', pd.NA, 'd'],
                                       [True, False, 7, pd.NaT]])

        cls.data_mv_array = np.array([[1, np.nan, 3, 4],
                                      [None, 4, 5, None],
                                      ['a', 'b', pd.NA, 'd'],
                                      [True, False, 7, pd.NaT]])

        cls.data_mv_list = [[1, np.nan, 3, 4],
                            [None, 4, 5, None],
                            ['a', 'b', pd.NA, 'd'],
                            [True, False, 7, pd.NaT]]

    def test_mv_total(self):
        # Test total missing values
        self.assertAlmostEqual(_missing_vals(self.data_mv_df)['mv_total'], 5)
        self.assertAlmostEqual(_missing_vals(self.data_mv_array)['mv_total'], 5)
        self.assertAlmostEqual(_missing_vals(self.data_mv_list)['mv_total'], 5)

    def test_mv_rows(self):
        # Test missing values for each row
        expected_results = [1, 2, 1, 1]
        for i, _ in enumerate(expected_results):
            self.assertAlmostEqual(_missing_vals(self.data_mv_df)['mv_rows'][i], expected_results[i])

    def test_mv_cols(self):
        # Test missing values for each column
        expected_results = [1, 1, 1, 2]
        for i, _ in enumerate(expected_results):
            self.assertAlmostEqual(_missing_vals(self.data_mv_df)['mv_cols'][i], expected_results[i])

    def test_mv_rows_ratio(self):
        # Test missing values ratio for each row
        expected_results = [0.25, 0.5, 0.25, 0.25]
        for i, _ in enumerate(expected_results):
            self.assertAlmostEqual(_missing_vals(self.data_mv_df)['mv_rows_ratio'][i], expected_results[i])

        # Test if missing value ratio is between 0 and 1
        for i in range(len(self.data_mv_df)):
            self.assertTrue(0 <= _missing_vals(self.data_mv_df)['mv_rows_ratio'][i] <= 1)

    def test_mv_cols_ratio(self):
        # Test missing values ratio for each column
        expected_results = [1/4, 0.25, 0.25, 0.5]
        for i, _ in enumerate(expected_results):
            self.assertAlmostEqual(_missing_vals(self.data_mv_df)['mv_cols_ratio'][i], expected_results[i])

        # Test if missing value ratio is between 0 and 1
        for i in range(len(self.data_mv_df)):
            self.assertTrue(0 <= _missing_vals(self.data_mv_df)['mv_cols_ratio'][i] <= 1)


class Test__validate_input(unittest.TestCase):

    def test__validate_input_0_1(self):
        with self.assertRaises(ValueError):
            _validate_input_0_1(-0.1, '-0.1')

        with self.assertRaises(ValueError):
            _validate_input_0_1(1.1, '1.1')

    def test__validate_input_bool(self):
        # Raises an exception if the input is not boolean
        with self.assertRaises(ValueError):
            _validate_input_bool('True', None)
        with self.assertRaises(ValueError):
            _validate_input_bool(None, None)
        with self.assertRaises(ValueError):
            _validate_input_bool(1, None)