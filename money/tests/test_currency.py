from money.money import (
    Currency,
)


def test_currency_equality():
    """
    The currency 3 letter code is what makes something unique
    """
    curr1 = Currency(
        code="ABC",
        numeric="1000",
        name="ABC Currency",
        symbol=u"$",
        decimals=2,
        countries=['My Country'])

    curr2 = Currency(
        code="ABC",
        numeric="1001",
        name="ABC Currency (Same numeric code)",
        symbol=u"#",
        decimals=1,
        countries=['My Country 2'])

    assert curr1 == curr2


def test_currency_inequality():
    """
    The currency 3 letter code is what makes something unique
    """
    curr1 = Currency(
        code="ABC",
        numeric="1000",
        name="My Currency",
        symbol=u"$",
        decimals=2,
        countries=['My Country'])

    curr2 = Currency(
        code="BCD",
        numeric="1000",
        name="My Currency",
        symbol=u"$",
        decimals=2,
        countries=['My Country'])

    assert curr1 != curr2


def test_currency_equality_against_string():
    """
    The currency can be compared to a string
    """
    curr1 = Currency(
        code="ABC",
        numeric="1000",
        name="ABC Currency",
        symbol=u"$",
        decimals=2,
        countries=['My Country'])

    assert curr1 == 'ABC'
    assert curr1 != 'DEF'

    assert curr1 == u'ABC'
    assert curr1 != u'DEF'


def test_currency_equality_against_other():
    """
    The currency can't (currently) be compared to something else...
    """
    curr1 = Currency(
        code="ABC",
        numeric="1000",
        name="ABC Currency",
        symbol=u"$",
        decimals=2,
        countries=['My Country'])

    assert curr1 != 1000
