from django.db import models
from money.contrib.django.models import fields
from money import Money

# Tests for Django models. We set up three types of models with different
# ways of specifying defaults

class TestMoneyModel(models.Model):
    name = models.CharField(max_length=100)
    # Default should be '0.000 XXX'
    price = fields.MoneyField(max_digits=12, decimal_places=3)

    def __unicode__(self):
        return self.name + " " + str(self.price)


class TestMoneyModelDefaultMoneyUSD(models.Model):
    name = models.CharField(max_length=100)
    price = fields.MoneyField(max_digits=12, decimal_places=3, default=Money("123.45", "USD"))
    zero = fields.MoneyField(max_digits=12, decimal_places=3, default=Money("0", "USD"))

    def __unicode__(self):
        return self.name + " " + str(self.price)


class TestMoneyModelDefaults(models.Model):
    name = models.CharField(max_length=100)
    price = fields.MoneyField(max_digits=12, decimal_places=3, default="123.45", default_currency="USD")
    zero = fields.MoneyField(max_digits=12, decimal_places=3, default="0", default_currency="USD")

    def __unicode__(self):
        return self.name + " " + str(self.price)

