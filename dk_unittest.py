import unittest
from dk import *

class TestDk(unittest.TestCase):
    def setUp(self):
        loadLines()
        pass
    
    def test_sorted(self):
        """
        make sure the first item in the sorted list is the one that has timestamp 0
        """
        self.assertEqual(loadLines()[0], [0, Measurement(accelerometer_x_val=-1.163086, accelerometer_y_val=0.238281, accelerometer_z_val=-1.051758, gyroscope_x_val=4.81493, gyroscope_y_val=-15.695393, gyroscope_z_val=-6.593897)])
        
    def test_searchContinuityAboveValue_01(self):
        """
        most basic search
        """
        for d in ["accelerometer_x_val", "accelerometer_y_val", "accelerometer_z_val", "gyroscope_x_val", "gyroscope_y_val", "gyroscope_z_val"]:
            self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000, -16, 1), 0)  # -16 is the lowest value globally in the provided data set
        self.assertRaises(ValueError, searchContinuityAboveValue, "some invalid data measurement", 0, 10000000000, -16, 1)
        
    def test_searchContinuityAboveValue_02(self):
        """
        play with indices
        """
        for d in ["accelerometer_x_val", "accelerometer_y_val", "accelerometer_z_val", "gyroscope_x_val", "gyroscope_y_val", "gyroscope_z_val"]:
            self.assertEqual(             searchContinuityAboveValue( d,      0,      100000, -16, 1), 0)
            self.assertEqual(             searchContinuityAboveValue( d, 100000, 10000000000, -16, 1), 101143)
            self.assertEqual(             searchContinuityAboveValue( d,      0,           1, -16, 1), 0)
            self.assertRaises(IndexError, searchContinuityAboveValue, d,      1,           0, -16, 1)
            self.assertRaises(IndexError, searchContinuityAboveValue, d,     -1,           0, -16, 1)
        
    def test_searchContinuityAboveValue_03(self):
        """
        play with threshold
        """
        d="accelerometer_x_val"
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,           -1.17, 1), 0)
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,           -1.16, 1), 1249)
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,               0, 1), 24973)
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,           16.39, 1), 1106330)
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,           16.40, 1), None)
        d="accelerometer_y_val"
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,            0.03, 1), 0)
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,            0.04, 1), 0)
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,               1, 1), 26222)
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,           23.10, 1), 1093843)
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,           23.11, 1), None)
        d="accelerometer_z_val"
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,           -1.32, 1), 0)
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,           -1.31, 1), 0)
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,           -1.00, 1), 4996)
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,           30.97, 1), 1092596)
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,           30.98, 1), None)
        d="gyroscope_x_val"
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,           -0.49, 1), 0)
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,           -0.48, 1), 0)
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,   3.14159265358, 1), 0)
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,           24.59, 1), 1092596)
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,           24.60, 1), None)
        d="gyroscope_y_val"
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,          -15.70, 1), 0)
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,          -15.69, 1), 1249)
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,            0.32, 1), 253482)
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,           62.63, 1), 1092596)
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,           62.64, 1), None)
        d="gyroscope_z_val"
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,           -6.60, 1), 0)
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,           -6.59, 1), 1249)
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,           -6.58, 1), 1249)
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,           41.07, 1), 1081356)
        self.assertEqual(searchContinuityAboveValue(d, 0, 10000000000,           41.08, 1), None)
        
    def test_searchContinuityAboveValue_04(self):
        """
        play with winLength
        """
        for d in ["accelerometer_x_val", "accelerometer_y_val", "accelerometer_z_val", "gyroscope_x_val", "gyroscope_y_val", "gyroscope_z_val"]:
            self.assertEqual(             searchContinuityAboveValue( d, 0, 10000000000, -16,   2), 0)
            self.assertEqual(             searchContinuityAboveValue( d, 0, 10000000000, -16,   64), 0)
            self.assertEqual(             searchContinuityAboveValue( d, 0, 10000000000, -16, 2048), None)
            self.assertRaises(IndexError, searchContinuityAboveValue, d, 0, 10000000000, -16,    0)
            self.assertRaises(IndexError, searchContinuityAboveValue, d, 0, 10000000000, -16,   -1)
        
    def test_searchContinuityAboveValue_05(self):
        """
        play with indices and threshold
        """
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val",      0,      100000, -32, 1), 0)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val",      0,      100000, -16, 1), 0)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val",      0,      100000,   0, 1), 24973)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val",      0,      100000,  16, 1), None)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val",      0,      100000,  17, 1), None)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val", 100000, 10000000000, -32, 1), 101143)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val", 100000, 10000000000, -16, 1), 101143)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val", 100000, 10000000000,   0, 1), 101143)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val", 100000, 10000000000,  16, 1), 1106330)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val", 100000, 10000000000,  17, 1), None)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val",      0,           1, -32, 1), 0)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val",      0,           1, -16, 1), 0)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val",      0,           1,   0, 1), None)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val",      0,           1,  16, 1), None)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val",      0,           1,  17, 1), None)
            
    def test_searchContinuityAboveValue_07(self):
        """
        play with indices and winLength
        """
        self.assertEqual(searchContinuityAboveValue("accelerometer_z_val",      0,      100000, -16,    2), 0)
        self.assertEqual(searchContinuityAboveValue("accelerometer_z_val",      0,      100000, -16,   64), 0)
        self.assertEqual(searchContinuityAboveValue("accelerometer_z_val",      0,      100000, -16,  128), None)
        self.assertEqual(searchContinuityAboveValue("accelerometer_z_val", 100000, 10000000000, -16,    2), 101143)
        self.assertEqual(searchContinuityAboveValue("accelerometer_z_val", 100000, 10000000000, -16,  512), 101143)
        self.assertEqual(searchContinuityAboveValue("accelerometer_z_val", 100000, 10000000000, -16, 1024), None)

    def test_searchContinuityAboveValue_08(self):
        """
        play with threshold and winLength
        """
        self.assertEqual(searchContinuityAboveValue("gyroscope_y_val", 0, 10000000000, -15.70,    2), 0)
        self.assertEqual(searchContinuityAboveValue("gyroscope_y_val", 0, 10000000000, -15.70,  512), 0)
        self.assertEqual(searchContinuityAboveValue("gyroscope_y_val", 0, 10000000000, -15.70, 1024), None)
        self.assertEqual(searchContinuityAboveValue("gyroscope_y_val", 0, 10000000000, -15.69,    2), 1249)
        self.assertEqual(searchContinuityAboveValue("gyroscope_y_val", 0, 10000000000, -15.69,  512), 1249)
        self.assertEqual(searchContinuityAboveValue("gyroscope_y_val", 0, 10000000000, -15.69, 1024), None)
        self.assertEqual(searchContinuityAboveValue("gyroscope_y_val", 0, 10000000000,   0.32,    2), 253482)
        self.assertEqual(searchContinuityAboveValue("gyroscope_y_val", 0, 10000000000,   0.32,    8), 253482)
        self.assertEqual(searchContinuityAboveValue("gyroscope_y_val", 0, 10000000000,   0.32,   16), 616847)
        self.assertEqual(searchContinuityAboveValue("gyroscope_y_val", 0, 10000000000,   0.32,  256), 616847)
        self.assertEqual(searchContinuityAboveValue("gyroscope_y_val", 0, 10000000000,   0.32,  512), None)
        self.assertEqual(searchContinuityAboveValue("gyroscope_y_val", 0, 10000000000,  62.63,    2), None)
        
    def test_searchContinuityAboveValue_09(self):
        """
        play with indices, threshold, and winLength
        """
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val",      0,      100000, -32,    2), 0)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val",      0,      100000, -32,   64), 0)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val",      0,      100000, -32,  128), None)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val",      0,      100000, -16,    2), 0)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val",      0,      100000, -16,   64), 0)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val",      0,      100000, -16,  128), None)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val",      0,      100000,   0,    2), 24973)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val",      0,      100000,   0,   32), 24973)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val",      0,      100000,   0,   64), None)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val", 100000, 10000000000, -32,    2), 101143)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val", 100000, 10000000000, -32, 1024), 101143)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val", 100000, 10000000000, -32, 2048), None)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val", 100000, 10000000000, -16,    2), 101143)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val", 100000, 10000000000, -16,  512), 101143)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val", 100000, 10000000000, -16, 1024), None)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val", 100000, 10000000000,   0,    2), 101143)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val", 100000, 10000000000,   0,  512), 101143)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val", 100000, 10000000000,   0, 1024), None)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val", 100000, 10000000000,  16,    2), None)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val",      0,           1, -32,    2), None)
        self.assertEqual(searchContinuityAboveValue("accelerometer_x_val",      0,           1, -16,    2), None)
        
    def test_backSearchContinuityWithinRange_01(self):
        """
        test value validation
        """
        self.assertRaises(IndexError, backSearchContinuityWithinRange, "accelerometer_y_val",           0, 100000,     1,     1,    1)
        self.assertRaises(IndexError, backSearchContinuityWithinRange, "accelerometer_y_val",           1,     -1,     1,     1,    1)
        self.assertRaises(ValueError, backSearchContinuityWithinRange, "accelerometer_y_val",           1,      0,     2,     1,    1)
        self.assertRaises(IndexError, backSearchContinuityWithinRange, "accelerometer_y_val",           1,      0,     1,     1,    0)
        
    def test_backSearchContinuityWithinRange_02(self):
        """
        test most basic search
        """
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val",      100000,      0,   -14,    24,    1), 99894)
        
    def test_backSearchContinuityWithinRange_03(self):
        """
        test different ranges
        """
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val",           1,      0,   -14,    24,    1), None)
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val", 10000000000, 100000,   -14,    24,    1), 1592068)
        
    def test_backSearchContinuityWithinRange_04(self):
        """
        test different thresholds
        """
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val",      100000,      0,   -10,    10,    1), 99894)
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val",      100000,      0,    -5,     5,    1), 99894)
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val",      100000,      0, -0.01,  0.01,    1), None)
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val",      100000,      0,  0.24,  0.25,    1), 93651)
        
    def test_backSearchContinuityWithinRange_05(self):
        """
        test different winLengths
        """
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val",      100000,      0,   -14,    24,    2), 99894)
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val",      100000,      0,   -14,    24,   64), 99894)
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val",      100000,      0,   -14,    24,  128), None)
        
    def test_backSearchContinuityWithinRange_06(self):
        """
        combine different ranges and thresholds
        """
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val",           1,      0,   -10,    10,    1), None)
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val", 10000000000, 100000,    -5,     5,    1), 1592068)
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val", 10000000000, 100000, -0.01,  0.01,    1), 1558354)
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val", 10000000000, 100000,  0.24,  0.25,    1), 874076)
        
    def test_backSearchContinuityWithinRange_07(self):
        """
        combine different ranges and winLengths
        """
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val",           1,      0,   -14,    24,    2), None)
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val",           1,      0,   -14,    24,   64), None)
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val",           1,      0,   -14,    24,  128), None)
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val", 10000000000, 100000,   -14,    24,    2), 1592068)
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val", 10000000000, 100000,   -14,    24,   64), 1592068)
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val", 10000000000, 100000,   -14,    24,  128), 1592068)
        
    def test_backSearchContinuityWithinRange_08(self):
        """
        combine different thresholds and winLengths
        """
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val",      100000,      0,   -10,    10,    2), 99894)
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val",      100000,      0,   -10,    10,   64), 99894)
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val",      100000,      0,   -10,    10,  128), None)
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val",      100000,      0,    -5,     5,    2), 99894)
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val",      100000,      0,    -5,     5,   64), 99894)
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val",      100000,      0,    -5,     5,  128), None)
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val",      100000,      0, -0.01,  0.01,    2), None)
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val",      100000,      0,  0.24,  0.25,    2), None)
        
    def test_backSearchContinuityWithinRange_09(self):
        """
        combine different ranges, thresholds, and winLengths
        """
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val",           1,      0,   -10,    10,    2), None)
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val", 10000000000, 100000,    -5,     5,    2), 1592068)
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val", 10000000000, 100000,    -5,     5,   64), 1592068)
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val", 10000000000, 100000,    -5,     5,  128), 1592068)
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val", 10000000000, 100000, -0.01,  0.01,    2), 1344828)
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val", 10000000000, 100000, -0.01,  0.01,   64), None)
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val", 10000000000, 100000,  0.24,  0.25,    2), 756700)
        self.assertEqual(             backSearchContinuityWithinRange( "accelerometer_y_val", 10000000000, 100000,  0.24,  0.25,   64), None)
        
if __name__ == '__main__':
    unittest.main()
