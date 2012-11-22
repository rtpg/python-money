from unittest import TestCase
from money import Money

class MoneyTestCase(TestCase):
    """
    Tests of the Money class
    """
    def testEquality(self):
        ten_bucks = Money(10, 'USD')
        a_hamilton = Money(10, 'USD')

        juu_en = Money(10, 'JPY')

        nada = Money(0, 'USD')

        # Scalars cannot be compared to Money class
        self.assertFalse(ten_bucks == 10)
        # unless it is 0
        self.assertTrue(nada == 0)

        # Money is equal to money of the same type
        self.assertTrue(ten_bucks == a_hamilton)

        # But not different currencies
        self.assertFalse(ten_bucks == juu_en)

