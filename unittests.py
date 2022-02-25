import unittest
from main import Grid


class Testchecknum(unittest.TestCase):
    """ Check that the values Grid.checknum() returns match ones
        calculated by hand.
    """

    def setUp(self):
        self.grid = Grid(0, 0, True, threshold=4, iterations=100)

    def test_001(self):
        """ -i in set
            since: -i   * -i   - i = -1-i,
                   -1-i * -1-i - i = i,
                   i    * i    - i = -1-i
        """
        self.assertFalse(self.grid.checknum(-1.0j))

    def test_002(self):
        """ 1 passes threshold of 4 after two iterations
            since: 1 * 1 + 1 = 2,
                   2 * 2 + 1 = 5,
        """
        self.assertEqual(self.grid.checknum(1.0), 2)

    def test_003(self):
        """ 2i passes threshold of 4 after one iterations
            since: 2i * 2i + 2i = -4+2i,
                   |-4+2i|      = square root of 20
        """
        self.assertEqual(self.grid.checknum(2.0j), 1)

    def test_004(self):
        """ 0.7 passes threshold of 4 after three iterations
            since: 0.7   * 0.7     + 0.7 = 1.19,
                   1.19   * 1.19   + 0.7 = 2.1161,
                   2.1161 * 2.1161 + 0.7 = 5.17787921
        """
        self.assertEqual(self.grid.checknum(0.7), 3)

    def test_005(self):
        """ 0.3-i passes threshold of 4 after three iterations
            since: 0.3-i          * 0.3-i          + 0.3-i = 0.61-1.6i,
                   0.61-1.6i      * 0.61-1.6i      + 0.3-i = -1.8879+0.952i,
                   -1.8879+0.952i * -1.8879+0.952i + 0.3-i = 2.95786241-4.5945616i,
                   |2.95786241-4.5945616i| > 5
        """
        self.assertEqual(self.grid.checknum(0.3-1.0j), 3)

    def test_006(self):
        """ 0 in set
            since: 0 * 0 + 0 = 0
        """
        self.assertFalse(self.grid.checknum(0.0))

    def test_007(self):
        """ -3 passes threshold of 4 after one iteration
            since: -3 * -3 - 3 = 6
        """
        self.assertEqual(self.grid.checknum(-3.0), 1)

    def test_008(self):
        """ -3i passes threshold of 4 after one iteration
            since: -3i * -3i - 3i = -9-3i,
                   |-9-3i| = square root of 90
        """
        self.assertEqual(self.grid.checknum(-3.0j), 1)

    def test_009(self):
        """ -3-3i passes threshold of 4 after one iteration
            since: 3-3i * 3-3i - 3-3i = -3+15i,
                   |-3+15i| = square root of 234
        """
        self.assertEqual(self.grid.checknum(-3-3.0j), 1)


class _Testcheckfill(unittest.TestCase):
    """ Check Grid.fill()
    """

    def _test_001(self):
        """ Filling a two-by-two grid returns a checksum of three
            since: (from Testchecknum.test_006) 0+0i  in set,
                   (from Testchecknum.test_007) -3+0i returns 1,
                   (from Testchecknum.test_008) 0-3i  returns 1,
                   (from Testchecknum.test_009) -3-3i returns 1,
        """
        self.assertEqual(Grid(2, 2, True, threshold=4, iterations=100, scale=3.0).fill(), 3)

    def test_002(self):
        """ Filling a 20-by-15 grid returns a checksum of 600
        """
        self.assertEqual(Grid(20, 15, True, threshold=4, iterations=100).fill(), 600)


if __name__ == '__main__':
    unittest.main()