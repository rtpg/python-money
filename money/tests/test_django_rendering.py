import pytest

from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from money.tests.models import (
    SimpleMoneyModel,
    MoneyModelDefaultMoneyUSD,
    MoneyModelDefaults,
)

from money.tests.views import *


class TestView(TestCase):

    def setUp(self):
        self.client = Client()

    def test_instance_view(self):
        url = reverse(instance_view)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'money|JPY 0.0|')
        self.assertContains(response, 'money.amount|0.0|')
        self.assertContains(response, 'money.currency|JPY|')

    def test_model_view(self):
        url = reverse(model_view)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'money|JPY 0.0|')
        self.assertContains(response, 'money.amount|0.0|')
        self.assertContains(response, 'money.currency|JPY|')

    def test_model_save_view(self):
        url = reverse(model_save_view)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'money|JPY 0.0|')
        self.assertContains(response, 'money.amount|0.0|')
        self.assertContains(response, 'money.currency|JPY|')


class TestEditView(TestCase):

    def setUp(self):
        self.client = Client()

    def test_form_GET(self):
        url = reverse(model_form_view)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'value="987.00"')
        self.assertContains(response, '<option value="JPY" selected="selected">JPY - Yen</option>')

    def test_form_POST(self):
        url = reverse(model_form_view)

        # We intentionally use decimals with a typically non-decimal currency
        self.client.post(url, {
            'name': 'ABC',
            'price_0': '555.5',
            'price_1': 'JPY',
        })

        # Find the object we created...
        obj = SimpleMoneyModel.objects.last()
        print "obj", obj, "obj.price", obj.price
        self.assertEqual(unicode(obj.price), u"JPY 555.5")
