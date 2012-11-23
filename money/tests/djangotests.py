from django.test import TestCase

from money.tests.models import TestMoneyModel, TestMoneyModelDefaultMoneyUSD, TestMoneyModelDefaults
from money import Money, CURRENCY


class MoneyFieldTestCase(TestCase):

    def setUp(self):
        #cleanup all entities
        TestMoneyModel.objects.all().delete()
        TestMoneyModelDefaultMoneyUSD.objects.all().delete()
        TestMoneyModelDefaults.objects.all().delete()

    def assertSameCurrency(self, moneys, currency=None):
        currencies = set([m.currency for m in moneys])
        self.assertTrue(len(currencies) == 1)
        if currency:
            self.assertEqual(currencies.pop().code, currency)

    def testCreating(self):
        ind = 0
        for code, currency in CURRENCY.items():
            ind = ind + 1
            price = Money(ind*1000.0, code)
            TestMoneyModel.objects.create(name=currency.name, price=price)
        count = TestMoneyModel.objects.all().count()
        self.assertEqual(len(CURRENCY), count)

        for code in CURRENCY:
            count = TestMoneyModel.objects.filter(price_currency=code).count()
            self.assertTrue(count == 1)

    def testRetrive(self):
        price = Money(100, "USD")
        TestMoneyModel.objects.create(name="one hundred dollars", price=price)


        #Filter
        qset = TestMoneyModel.objects.filter(price=price)
        self.assertEqual(qset.count(), 1)
        self.assertEqual(qset[0].price, price)

        #Get
        entry = TestMoneyModel.objects.get(price=price)
        self.assertEqual(entry.price, price)

        #test retrieving without currency
        entry = TestMoneyModel.objects.get(price=100)
        self.assertEqual(entry.price, price)

    def testAssign(self):
        ent = TestMoneyModel(name='test', price=Money(100, "USD"))
        ent.save()
        self.assertEquals(ent.price, Money(100, "USD"))

        ent.price = Money(10, "USD")
        ent.save()
        self.assertEquals(ent.price, Money(10, "USD"))

        ent_same = TestMoneyModel.objects.get(pk=ent.id)
        self.assertEquals(ent_same.price, Money(10, "USD"))

    def testRetreiveAndUpdate(self):
        created = TestMoneyModel.objects.create(name="one hundred dollars", price=Money(100, "USD"))
        created.save()
        self.assertEquals(created.price, Money(100, "USD"))

        ent = TestMoneyModel.objects.filter(price__exact=Money(100, "USD")).get()
        self.assertEquals(ent.price, Money(100, "USD"))
        ent.price.amount = 300
        ent.save()

        ent = TestMoneyModel.objects.filter(price__exact=Money(300, "USD")).get()
        self.assertEquals(ent.price, Money(300, "USD"))

    def testDefaults(self):
        ent = TestMoneyModelDefaultMoneyUSD.objects.create(name='0 USD')
        ent = TestMoneyModelDefaultMoneyUSD.objects.get(pk=ent.id)
        self.assertEquals(ent.price, Money(0, 'USD'))

        ent = TestMoneyModelDefaults.objects.create(name='100 USD', price=100)
        ent = TestMoneyModelDefaults.objects.get(pk=ent.id)
        self.assertEquals(ent.price, Money(100, 'USD'))

    def testLookup(self):
        USD100 = Money(100, "USD")
        EUR100 = Money(100, "EUR")
        UAH100 = Money(100, "UAH")

        TestMoneyModel.objects.create(name="one hundred dollars", price=USD100)
        TestMoneyModel.objects.create(name="one hundred and one dollars", price=USD100+1)
        TestMoneyModel.objects.create(name="ninety nine dollars", price=USD100-1)

        TestMoneyModel.objects.create(name="one hundred euros", price=EUR100)
        TestMoneyModel.objects.create(name="one hundred and one euros", price=EUR100+1)
        TestMoneyModel.objects.create(name="ninety nine euros", price=EUR100-1)

        TestMoneyModel.objects.create(name="one hundred hrivnyas", price=UAH100)
        TestMoneyModel.objects.create(name="one hundred and one hrivnyas", price=UAH100+1)
        TestMoneyModel.objects.create(name="ninety nine hrivnyas", price=UAH100-1)


        #Exact:

        qset = TestMoneyModel.objects.filter(price__exact=USD100)
        self.assertEqual(qset.count(), 1)
        qset = TestMoneyModel.objects.filter(price__exact=EUR100)
        self.assertEqual(qset.count(), 1)
        qset = TestMoneyModel.objects.filter(price__exact=UAH100)
        self.assertEqual(qset.count(), 1)

        #Less then:

        qset = TestMoneyModel.objects.filter(price__lt=USD100)
        self.assertEqual(qset.count(), 1)
        self.assertEqual(qset[0].price, USD100-1)

        qset = TestMoneyModel.objects.filter(price__lt=EUR100)
        self.assertEqual(qset.count(), 1)
        self.assertEqual(qset[0].price, EUR100-1)

        qset = TestMoneyModel.objects.filter(price__lt=UAH100)
        self.assertEqual(qset.count(), 1)
        self.assertEqual(qset[0].price, UAH100-1)

        #Greater then:

        qset = TestMoneyModel.objects.filter(price__gt=USD100)
        self.assertEqual(qset.count(), 1)
        self.assertEqual(qset[0].price, USD100+1)

        qset = TestMoneyModel.objects.filter(price__gt=EUR100)
        self.assertEqual(qset.count(), 1)
        self.assertEqual(qset[0].price, EUR100+1)

        qset = TestMoneyModel.objects.filter(price__gt=UAH100)
        self.assertEqual(qset.count(), 1)
        self.assertEqual(qset[0].price, UAH100+1)

        #Less then or equal:

        qset = TestMoneyModel.objects.filter(price__lte=USD100)
        self.assertEqual(qset.count(), 2)
        self.assertSameCurrency([ent.price for ent in qset], "USD")
        for ent in qset: self.assertTrue(ent.price.amount <= 100)

        qset = TestMoneyModel.objects.filter(price__lte=EUR100)
        self.assertEqual(qset.count(), 2)
        self.assertSameCurrency([ent.price for ent in qset], "EUR")
        for ent in qset: self.assertTrue(ent.price.amount <= 100)

        qset = TestMoneyModel.objects.filter(price__lte=UAH100)
        self.assertEqual(qset.count(), 2)
        self.assertSameCurrency([ent.price for ent in qset], "UAH")
        for ent in qset: self.assertTrue(ent.price.amount <= 100)


        #Greater then or equal:

        qset = TestMoneyModel.objects.filter(price__gte=USD100)
        self.assertEqual(qset.count(), 2)
        self.assertSameCurrency([ent.price for ent in qset], "USD")

        qset = TestMoneyModel.objects.filter(price__gte=EUR100)
        self.assertEqual(qset.count(), 2)
        self.assertSameCurrency([ent.price for ent in qset], "EUR")

        qset = TestMoneyModel.objects.filter(price__gte=UAH100)
        self.assertEqual(qset.count(), 2)
        self.assertSameCurrency([ent.price for ent in qset], "UAH")

    def testPriceAttribute(self):
        e = TestMoneyModel()
        e.price = Money(0, "BGN")
        e.price.amount = 3
        self.assertEqual(e.price, Money(3, "BGN"))
        e.price.from_string("BGN 5.0")
        self.assertEqual(e.price, Money(5, "BGN"))

    def testPriceAttributeInConstructor(self):
        e1 = TestMoneyModel(price=Money(100, "USD"))
        e2 = TestMoneyModel(price=Money(200, "JPY"))
        self.assertEqual(e1.price, Money(100, "USD"))
        self.assertEqual(e2.price, Money(200, "JPY"))

    def testPriceAttributeUpdate(self):
        e2 = TestMoneyModel(price=Money(200, "JPY"))
        e2.price = Money(300, "USD")
        self.assertEqual(e2.price, Money(300, "USD"))

    def testPriceFromString(self):
        e2 = TestMoneyModel(price=Money(200, "JPY"))
        e2.price.from_string("USD 400")
        self.assertEqual(e2.price, Money(400, "USD"))

    def testZeroEdgeCase(self):
        created = TestMoneyModel.objects.create(name="zero dollars", price=Money(0, "USD"))
        self.assertEquals(created.price, Money(0, "USD"))

        ent = TestMoneyModel.objects.filter(price__exact=Money(0, "USD")).get()
        self.assertEquals(ent.price, Money(0, "USD"))


class TestMoneyFieldFixtureLoading(TestCase):

    fixtures = ['testdata.json',]

    def testDataWasLoaded(self):
        model1 = TestMoneyModel.objects.get(pk=1001)
        self.assertEqual(model1.price, Money("123.45", "JPY"))

