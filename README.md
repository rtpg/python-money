
python-money
============

Primitives for working with money and currencies in Python


Installation
============

You can install this project directly from the git repository using pip:

    $ pip install -e git+http://github.com/poswald/python-money.git@0.0.1#egg=python-money

You do not have to specify the version number but it might be a good idea.

Usage
=====

This application contains several classes and functions that make dealing with
money easier and less error prone.

### Currency Types

The Currency class can be used to represent a type of Currency. It contains
values for the currency's code, ISO number, name and the country it's used in.
For example:

    Currency(code='BZD', numeric='084', name='Belize Dollar', countries=['BELIZE'])

There is a dict of all ISO-4217 currencies:

    >>> from money import CURRENCY
    >>> print CURRENCY['GBP'].name
    Pound Sterling

### Money Class

The Money class is available for doing arithmetic on values in defined
currencies. It wraps the python Decimal type and gives you several convienience
methods. Using this prevents you from making mistakes like adding Pounds and
Dollars together, multiplying two money values or comparing different
currencies. For example:

    >>> usd = Money(amount=10.00, currency=CURRENCY['USD'])
    >>> print usd
    USD 10.00

    >>> jpy = Money(amount=2000, currency=CURRENCY['JPY'])
    >>> print jpy
    JPY 2000.00

    >>> print jpy * usd
    Traceback (most recent call last):
      File "<console>", line 1, in <module>
      File "/python-money/money/Money.py", line 79, in __mul__
        raise TypeError, 'can not multiply monetary quantities'
    TypeError: can not multiply monetary quantities

    >>> print jpy > usd
    Traceback (most recent call last):
      File "<console>", line 1, in <module>
      File "/Users/poswald/Projects/python-money/money/Money.py", line 137, in __gt__
        raise TypeError, 'can not compare different currencies'
    TypeError: can not compare different currencies

    >>> print 1 % usd
    USD  0.10

    >>> print usd * 5
    USD 50.00

    >>> print (usd * 5).allocate((50,50))
    [USD 25.00, USD 25.00]
    >>> print (jpy * 5).allocate((50,50))
    [JPY 5000.00, JPY 5000.00]

### Default Currency

This package assumes that you have a preferred default currency. Somewhere in
your software's initialization you should set that currency:

    >>> from money import set_default_currency
    >>> set_default_currency(code='USD')
    >>> print Money(amount=23.45)
    USD 23.45

If you don't you will get a non-specified 'XXX' currency:

    >>> print Money(amount=23.45)
    XXX 23.45

There is also an exchange rate that may be set:

This default currency and exchange rate is used for arithmetic addition. If you
add two monetary values that are in differing currency, they will first be
converted into the default currency, and then added together.


Django
======

This package includes some classes as a convenience to Django users. These are
entirely optional.

### Model Field

Add a currency field to your models. This field takes similar parameters as
the Django DecimalField:

    from money.contrib.django.models.fields import MoneyField

    class Thing(models.Model):
        ...
        price = MoneyField(default=0, max_digits=12, decimal_places=2)
        ...

Now run ./manage.py dbsync or South migrate. Your database table will contain a
field for holding the value and a second field for the currency type. In
postgresql it might look like this:

    price          | numeric(12,2)          | not null default NULL::numeric
    price_currency | character varying(3)   | not null

The value you get from your model will be a `Money` class:

    thing = Thing.objects.get(id=123)
    print repr(thing.price)
    USD  199.99


### Form Field

The form field used by the `models.MoneyField` is also called `MoneyField` in


### Running Tests

The test suite requires `nose`, `django` and `django_nose` to be installed. They
will be downloaded and installed automatically when run.

Tests can be run via the `setup.py` script:

    $ python setup.py test

or directly via the runscripts command. This can be usefull for passing
addtional options to nose:

    $ python money/runtests.py

If you wish to contribute code, please run these tests to ensure nothing breaks.


TODO
====

* Add more currency symbols to Currency class
* Add number of decimal places to all Currencies. Who wants to help? :-)
* Change the addition operation so that it raises an Exception rather
than implicitly convert the value
* Add a convert method to explicitly convert using the exchange rate.
* Division of money should probably raise a custom error instead of assert on currency mismatch
* Division of `Money` should return `Money` instead of `Decimal` type

CHANGELOG
===

* Version 0.2.0
    - Fixed an issue with the South introspection rule for MoneyField similar to [ South #327](http://south.aeracode.org/ticket/327) You will probably need to generate a new schema migration if you are upgrading.

* Version 0.1.0
    - Initial version
