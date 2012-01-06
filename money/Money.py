# -*- coding: utf-8 -*-
import exceptions
from decimal import Decimal

class Currency:
    code = "XXX"
    country = ""
    countries = []
    name = ""
    numeric = "999"
    exchange_rate = Decimal("1.0")
    def __init__(self, code="", numeric="999", name="", symbol=u"", decimals=2, countries=[]):
        self.code = code
        self.numeric = numeric
        self.name = name
        self.symbol = symbol
        self.decimals = decimals
        self.countries = countries

    def __repr__(self):
        return self.code
    def set_exchange_rate(self, rate):
        if not isinstance(rate, Decimal):
            rate = Decimal(str(rate))
        self.exchange_rate = rate

CURRENCY = {}
CURRENCY['XXX'] = Currency(code="XXX", numeric="999")
DEFAULT_CURRENCY = CURRENCY['XXX']

def set_default_currency(code="XXX"):
    global DEFAULT_CURRENCY
    DEFAULT_CURRENCY = CURRENCY[code]

class IncorrectMoneyInputError(exceptions.Exception):
    def __init__(self):
        return
    def __unicode__(self):
        return u"Incorrectly formatted monetary input"

class Money:
    amount = Decimal("0.0")
    currency = DEFAULT_CURRENCY
    def __init__ (self, amount=Decimal("0.0"), currency=None):
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount or 0))
        self.amount = amount
        if not currency:
            self.currency = DEFAULT_CURRENCY
        else:
            if not isinstance(currency, Currency):
                currency = CURRENCY[str(currency).upper()]
            self.currency = currency

    def __unicode__(self):
        return unicode(self.amount)
    def __float__(self):
        return float(self.amount)
    def __repr__(self):
        return '%s %5.2f' % (self.currency, self.amount)
    def __pos__(self):
        return Money(amount=self.amount, currency=self.currency)
    def __neg__(self):
        return Money(amount=-self.amount, currency=self.currency)
    def __add__(self, other):
        if isinstance(other, Money):
            if self.currency == other.currency:
                return Money(amount = self.amount + other.amount, currency = self.currency)
            else:
                s = self.convert_to_default()
                other = other.convert_to_default()
                return Money(amount = s.amount + other.amount, currency = DEFAULT_CURRENCY)
        else:
            return Money(amount = self.amount + Decimal(str(other)), currency = self.currency)
    def __sub__(self, other):
        if isinstance(other, Money):
            if self.currency == other.currency:
                return Money(amount = self.amount - other.amount, currency = self.currency)
            else:
                s = self.convert_to_default()
                other = other.convert_to_default()
                return Money(amount = s.amount - other.amount, currency = DEFAULT_CURRENCY)
        else:
            return Money(amount = self.amount - Decimal(str(other)), currency = self.currency)
    def __rsub__(self, other):
        return Money(amount = Decimal(str(other)) - self.amount, currency = self.currency)
    def __mul__(self, other):
        if isinstance(other, Money):
            raise TypeError, 'can not multiply monetary quantities'
        else:
            return Money(amount = self.amount*Decimal(str(other)), currency = self.currency)
    def __div__(self, other):
        if isinstance(other, Money):
            assert self.currency == other.currency, 'currency mismatch'
            return self.amount / other.amount
        else:
            return self.amount / Decimal(str(other))
    def __rdiv__(self, other):
        return Decimal(str(other)) / self.amount
    def __rmod__(self, other):
        """
        Calculate percentage of an amount.  The left-hand side of the operator must be a numeric value.  E.g.:
        >>> money = Money.Money(200, "USD")
        >>> 5 % money
        USD 10.00
        """
        if isinstance(other, Money):
            raise TypeError, 'invalid monetary operation'
        else:
            return Money(amount = Decimal(str(other)) * self.amount / 100, currency = self.currency)
    def convert_to_default(self):
        return Money(amount = self.amount * self.currency.exchange_rate, currency=DEFAULT_CURRENCY)
    def convert_to(self, currency):
        """
        Convert from one currency to another.
        """
        return None # TODO  (How??)

    __radd__ = __add__
    __rmul__ = __mul__

    #
    # Override comparison operators
    #
    def __eq__(self, other):
        if isinstance(other, Money):
            return (self.amount == other.amount) and (self.currency == other.currency)
        # Allow comparison to 0
        if (other == 0) and (self.amount == 0):
            return True
        return False

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result
    def __lt__(self, other):
        if isinstance(other, Money):
            if (self.currency == other.currency):
                return (self.amount < other.amount)
            else:
                raise TypeError, 'can not compare different currencies'
        else:
            return (self.amount < Decimal(str(other)))
    def __gt__(self, other):
        if isinstance(other, Money):
            if (self.currency == other.currency):
                return (self.amount > other.amount)
            else:
                raise TypeError, 'can not compare different currencies'
        else:
            return (self.amount > Decimal(str(other)))
    def __le__(self, other):
        return self < other or self == other
    def __ge__(self, other):
        return self > other or self == other

    #
    # Miscellaneous helper methods
    #

    def allocate(self, ratios):
        """
        Allocates a sum of money to several accounts.
        """
        total = sum(ratios)
        remainder = self.amount
        results = []
        for i in range(0, len(ratios)):
            results.append(Money(amount = self.amount * ratios[i] / total, currency = self.currency))
            remainder -= results[i].amount
        i = 0
        while i < remainder:
            results[i].amount += Decimal("0.01")
            i += 1
        return results

    def spell_out(self):
        """
        Spells out a monetary amount.  E.g. "Two-hundred and twenty-six dollars and seventeen cents."
        """
        pass # TODO

    def from_string(self, s):
        """
        Parses a properly formatted string and extracts the monetary value and currency
        """
        try:
            self.amount = Decimal(str(s).strip())
            self.currency = DEFAULT_CURRENCY
        except:
            try:
                s = s.strip()
                self.currency = CURRENCY[s[:3].upper()]
                self.amount = Decimal(s[3:].strip())
            except:
                raise IncorrectMoneyInputError

#
# Definitions of ISO 4217 Currencies
# Source: http://www.currency-iso.org/
# Symbols: http://www.xe.com/symbols.php
#
# Note that the decimal code of N/A has been mapped to None

CURRENCY['AED'] = Currency(code='AED', numeric='784', decimals=2, symbol=u'', name=u'UAE Dirham', countries=[u'UNITED ARAB EMIRATES'])
CURRENCY['AFN'] = Currency(code='AFN', numeric='971', decimals=2, symbol=u'؋', name=u'Afghani', countries=[u'AFGHANISTAN'])
CURRENCY['ALL'] = Currency(code='ALL', numeric='008', decimals=2, symbol=u'Lek', name=u'Lek', countries=[u'ALBANIA'])
CURRENCY['AMD'] = Currency(code='AMD', numeric='051', decimals=2, symbol=u'', name=u'Armenian Dram', countries=[u'ARMENIA'])
CURRENCY['ANG'] = Currency(code='ANG', numeric='532', decimals=2, symbol=u'ƒ', name=u'Netherlands Antillean Guilder', countries=[u'CURA\xc7AO', u'SINT MAARTEN (DUTCH PART)'])
CURRENCY['AOA'] = Currency(code='AOA', numeric='973', decimals=2, symbol=u'', name=u'Kwanza', countries=[u'ANGOLA'])
CURRENCY['ARS'] = Currency(code='ARS', numeric='032', decimals=2, symbol=u'$', name=u'Argentine Peso', countries=[u'ARGENTINA'])
CURRENCY['AUD'] = Currency(code='AUD', numeric='036', decimals=2, symbol=u'$', name=u'Australian Dollar', countries=[u'AUSTRALIA', u'CHRISTMAS ISLAND', u'COCOS (KEELING) ISLANDS', u'HEARD ISLAND AND McDONALD ISLANDS', u'KIRIBATI', u'NAURU', u'NORFOLK ISLAND', u'TUVALU'])
CURRENCY['AWG'] = Currency(code='AWG', numeric='533', decimals=2, symbol=u'ƒ', name=u'Aruban Florin', countries=[u'ARUBA'])
CURRENCY['AZN'] = Currency(code='AZN', numeric='944', decimals=2, symbol=u'ман', name=u'Azerbaijanian Manat', countries=[u'AZERBAIJAN'])
CURRENCY['BAM'] = Currency(code='BAM', numeric='977', decimals=2, symbol=u'KM', name=u'Convertible Mark', countries=[u'BOSNIA AND HERZEGOVINA'])
CURRENCY['BBD'] = Currency(code='BBD', numeric='052', decimals=2, symbol=u'$', name=u'Barbados Dollar', countries=[u'BARBADOS'])
CURRENCY['BDT'] = Currency(code='BDT', numeric='050', decimals=2, symbol=u'', name=u'Taka', countries=[u'BANGLADESH'])
CURRENCY['BGN'] = Currency(code='BGN', numeric='975', decimals=2, symbol=u'лв', name=u'Bulgarian Lev', countries=[u'BULGARIA'])
CURRENCY['BHD'] = Currency(code='BHD', numeric='048', decimals=3, symbol=u'', name=u'Bahraini Dinar', countries=[u'BAHRAIN'])
CURRENCY['BIF'] = Currency(code='BIF', numeric='108', decimals=0, symbol=u'', name=u'Burundi Franc', countries=[u'BURUNDI'])
CURRENCY['BMD'] = Currency(code='BMD', numeric='060', decimals=2, symbol=u'$', name=u'Bermudian Dollar', countries=[u'BERMUDA'])
CURRENCY['BND'] = Currency(code='BND', numeric='096', decimals=2, symbol=u'$', name=u'Brunei Dollar', countries=[u'BRUNEI DARUSSALAM'])
CURRENCY['BOB'] = Currency(code='BOB', numeric='068', decimals=2, symbol=u'$b', name=u'Boliviano', countries=[u'BOLIVIA, PLURINATIONAL STATE OF'])
CURRENCY['BOV'] = Currency(code='BOV', numeric='984', decimals=2, symbol=u'', name=u'Mvdol', countries=[u'BOLIVIA, PLURINATIONAL STATE OF'])
CURRENCY['BRL'] = Currency(code='BRL', numeric='986', decimals=2, symbol=u'R$', name=u'Brazilian Real', countries=[u'BRAZIL'])
CURRENCY['BSD'] = Currency(code='BSD', numeric='044', decimals=2, symbol=u'$', name=u'Bahamian Dollar', countries=[u'BAHAMAS'])
CURRENCY['BTN'] = Currency(code='BTN', numeric='064', decimals=2, symbol=u'', name=u'Ngultrum', countries=[u'BHUTAN'])
CURRENCY['BWP'] = Currency(code='BWP', numeric='072', decimals=2, symbol=u'P', name=u'Pula', countries=[u'BOTSWANA'])
CURRENCY['BYR'] = Currency(code='BYR', numeric='974', decimals=0, symbol=u'p.', name=u'Belarussian Ruble', countries=[u'BELARUS'])
CURRENCY['BZD'] = Currency(code='BZD', numeric='084', decimals=2, symbol=u'BZ$', name=u'Belize Dollar', countries=[u'BELIZE'])
CURRENCY['CAD'] = Currency(code='CAD', numeric='124', decimals=2, symbol=u'$', name=u'Canadian Dollar', countries=[u'CANADA'])
CURRENCY['CDF'] = Currency(code='CDF', numeric='976', decimals=2, symbol=u'', name=u'Congolese Franc', countries=[u'CONGO, THE DEMOCRATIC REPUBLIC OF'])
CURRENCY['CHE'] = Currency(code='CHE', numeric='947', decimals=2, symbol=u'', name=u'WIR Euro', countries=[u'SWITZERLAND'])
CURRENCY['CHF'] = Currency(code='CHF', numeric='756', decimals=2, symbol=u'Fr.', name=u'Swiss Franc', countries=[u'LIECHTENSTEIN', u'SWITZERLAND'])
CURRENCY['CHW'] = Currency(code='CHW', numeric='948', decimals=2, symbol=u'', name=u'WIR Franc', countries=[u'SWITZERLAND'])
CURRENCY['CLF'] = Currency(code='CLF', numeric='990', decimals=0, symbol=u'', name=u'Unidades de fomento', countries=[u'CHILE'])
CURRENCY['CLP'] = Currency(code='CLP', numeric='152', decimals=0, symbol=u'$', name=u'Chilean Peso', countries=[u'CHILE'])
CURRENCY['CNY'] = Currency(code='CNY', numeric='156', decimals=2, symbol=u'¥', name=u'Yuan Renminbi', countries=[u'CHINA'])
CURRENCY['COP'] = Currency(code='COP', numeric='170', decimals=2, symbol=u'$', name=u'Colombian Peso', countries=[u'COLOMBIA'])
CURRENCY['COU'] = Currency(code='COU', numeric='970', decimals=2, symbol=u'', name=u'Unidad de Valor Real', countries=[u'COLOMBIA'])
CURRENCY['CRC'] = Currency(code='CRC', numeric='188', decimals=2, symbol=u'₡', name=u'Costa Rican Colon', countries=[u'COSTA RICA'])
CURRENCY['CUC'] = Currency(code='CUC', numeric='931', decimals=2, symbol=u'', name=u'Peso Convertible', countries=[u'CUBA'])
CURRENCY['CUP'] = Currency(code='CUP', numeric='192', decimals=2, symbol=u'₱', name=u'Cuban Peso', countries=[u'CUBA'])
CURRENCY['CVE'] = Currency(code='CVE', numeric='132', decimals=2, symbol=u'', name=u'Cape Verde Escudo', countries=[u'CAPE VERDE'])
CURRENCY['CZK'] = Currency(code='CZK', numeric='203', decimals=2, symbol=u'Kč', name=u'Czech Koruna', countries=[u'CZECH REPUBLIC'])
CURRENCY['DJF'] = Currency(code='DJF', numeric='262', decimals=0, symbol=u'', name=u'Djibouti Franc', countries=[u'DJIBOUTI'])
CURRENCY['DKK'] = Currency(code='DKK', numeric='208', decimals=2, symbol=u'kr', name=u'Danish Krone', countries=[u'DENMARK', u'FAROE ISLANDS', u'GREENLAND'])
CURRENCY['DOP'] = Currency(code='DOP', numeric='214', decimals=2, symbol=u'RD$', name=u'Dominican Peso', countries=[u'DOMINICAN REPUBLIC'])
CURRENCY['DZD'] = Currency(code='DZD', numeric='012', decimals=2, symbol=u'', name=u'Algerian Dinar', countries=[u'ALGERIA'])
CURRENCY['EGP'] = Currency(code='EGP', numeric='818', decimals=2, symbol=u'£', name=u'Egyptian Pound', countries=[u'EGYPT'])
CURRENCY['ERN'] = Currency(code='ERN', numeric='232', decimals=2, symbol=u'', name=u'Nakfa', countries=[u'ERITREA'])
CURRENCY['ETB'] = Currency(code='ETB', numeric='230', decimals=2, symbol=u'', name=u'Ethiopian Birr', countries=[u'ETHIOPIA'])
CURRENCY['EUR'] = Currency(code='EUR', numeric='978', decimals=2, symbol=u'€', name=u'Euro', countries=[u'\xc5LAND ISLANDS', u'ANDORRA', u'AUSTRIA', u'BELGIUM', u'CYPRUS', u'ESTONIA', u'EUROPEAN UNION ', u'FINLAND', u'FRANCE', u'FRENCH GUIANA', u'FRENCH SOUTHERN TERRITORIES', u'GERMANY', u'GREECE', u'GUADELOUPE', u'HOLY SEE (VATICAN CITY STATE)', u'IRELAND', u'ITALY', u'LUXEMBOURG', u'MALTA', u'MARTINIQUE', u'MAYOTTE', u'MONACO', u'MONTENEGRO', u'NETHERLANDS', u'PORTUGAL', u'R\xc9UNION', u'SAINT BARTH\xc9LEMY', u'SAINT MARTIN (FRENCH PART)', u'SAINT PIERRE AND MIQUELON', u'SAN MARINO', u'SLOVAKIA', u'SLOVENIA', u'SPAIN', u'Vatican City State (HOLY SEE)'])
CURRENCY['FJD'] = Currency(code='FJD', numeric='242', decimals=2, symbol=u'$', name=u'Fiji Dollar', countries=[u'FIJI'])
CURRENCY['FKP'] = Currency(code='FKP', numeric='238', decimals=2, symbol=u'£', name=u'Falkland Islands Pound', countries=[u'FALKLAND ISLANDS (MALVINAS)'])
CURRENCY['GBP'] = Currency(code='GBP', numeric='826', decimals=2, symbol=u'£', name=u'Pound Sterling', countries=[u'GUERNSEY', u'ISLE OF MAN', u'JERSEY', u'UNITED KINGDOM'])
CURRENCY['GEL'] = Currency(code='GEL', numeric='981', decimals=2, symbol=u'', name=u'Lari', countries=[u'GEORGIA'])
CURRENCY['GHS'] = Currency(code='GHS', numeric='936', decimals=2, symbol=u'', name=u'Ghana Cedi', countries=[u'GHANA'])
CURRENCY['GIP'] = Currency(code='GIP', numeric='292', decimals=2, symbol=u'£', name=u'Gibraltar Pound', countries=[u'GIBRALTAR'])
CURRENCY['GMD'] = Currency(code='GMD', numeric='270', decimals=2, symbol=u'', name=u'Dalasi', countries=[u'GAMBIA'])
CURRENCY['GNF'] = Currency(code='GNF', numeric='324', decimals=0, symbol=u'', name=u'Guinea Franc', countries=[u'GUINEA'])
CURRENCY['GTQ'] = Currency(code='GTQ', numeric='320', decimals=2, symbol=u'Q', name=u'Quetzal', countries=[u'GUATEMALA'])
CURRENCY['GYD'] = Currency(code='GYD', numeric='328', decimals=2, symbol=u'$', name=u'Guyana Dollar', countries=[u'GUYANA'])
CURRENCY['HKD'] = Currency(code='HKD', numeric='344', decimals=2, symbol=u'HK$', name=u'Hong Kong Dollar', countries=[u'HONG KONG'])
CURRENCY['HNL'] = Currency(code='HNL', numeric='340', decimals=2, symbol=u'L', name=u'Lempira', countries=[u'HONDURAS'])
CURRENCY['HRK'] = Currency(code='HRK', numeric='191', decimals=2, symbol=u'kn', name=u'Croatian Kuna', countries=[u'CROATIA'])
CURRENCY['HTG'] = Currency(code='HTG', numeric='332', decimals=2, symbol=u'', name=u'Gourde', countries=[u'HAITI'])
CURRENCY['HUF'] = Currency(code='HUF', numeric='348', decimals=2, symbol=u'Ft', name=u'Forint', countries=[u'HUNGARY'])
CURRENCY['IDR'] = Currency(code='IDR', numeric='360', decimals=2, symbol=u'Rp', name=u'Rupiah', countries=[u'INDONESIA'])
CURRENCY['ILS'] = Currency(code='ILS', numeric='376', decimals=2, symbol=u'₪', name=u'New Israeli Sheqel', countries=[u'ISRAEL'])
CURRENCY['INR'] = Currency(code='INR', numeric='356', decimals=2, symbol=u'', name=u'Indian Rupee', countries=[u'BHUTAN', u'INDIA'])
CURRENCY['IQD'] = Currency(code='IQD', numeric='368', decimals=3, symbol=u'', name=u'Iraqi Dinar', countries=[u'IRAQ'])
CURRENCY['IRR'] = Currency(code='IRR', numeric='364', decimals=2, symbol=u'﷼', name=u'Iranian Rial', countries=[u'IRAN, ISLAMIC REPUBLIC OF'])
CURRENCY['ISK'] = Currency(code='ISK', numeric='352', decimals=0, symbol=u'kr', name=u'Iceland Krona', countries=[u'ICELAND'])
CURRENCY['JMD'] = Currency(code='JMD', numeric='388', decimals=2, symbol=u'J$', name=u'Jamaican Dollar', countries=[u'JAMAICA'])
CURRENCY['JOD'] = Currency(code='JOD', numeric='400', decimals=3, symbol=u'', name=u'Jordanian Dinar', countries=[u'JORDAN'])
CURRENCY['JPY'] = Currency(code='JPY', numeric='392', decimals=0, symbol=u'¥', name=u'Yen', countries=[u'JAPAN'])
CURRENCY['KES'] = Currency(code='KES', numeric='404', decimals=2, symbol=u'', name=u'Kenyan Shilling', countries=[u'KENYA'])
CURRENCY['KGS'] = Currency(code='KGS', numeric='417', decimals=2, symbol=u'лв', name=u'Som', countries=[u'KYRGYZSTAN'])
CURRENCY['KHR'] = Currency(code='KHR', numeric='116', decimals=2, symbol=u'៛', name=u'Riel', countries=[u'CAMBODIA'])
CURRENCY['KMF'] = Currency(code='KMF', numeric='174', decimals=0, symbol=u'', name=u'Comoro Franc', countries=[u'COMOROS'])
CURRENCY['KPW'] = Currency(code='KPW', numeric='408', decimals=2, symbol=u'₩', name=u'North Korean Won', countries=[u'KOREA, DEMOCRATIC PEOPLE\u2019S REPUBLIC OF'])
CURRENCY['KRW'] = Currency(code='KRW', numeric='410', decimals=0, symbol=u'₩', name=u'Won', countries=[u'KOREA, REPUBLIC OF'])
CURRENCY['KWD'] = Currency(code='KWD', numeric='414', decimals=3, symbol=u'', name=u'Kuwaiti Dinar', countries=[u'KUWAIT'])
CURRENCY['KYD'] = Currency(code='KYD', numeric='136', decimals=2, symbol=u'$', name=u'Cayman Islands Dollar', countries=[u'CAYMAN ISLANDS'])
CURRENCY['KZT'] = Currency(code='KZT', numeric='398', decimals=2, symbol=u'лв', name=u'Tenge', countries=[u'KAZAKHSTAN'])
CURRENCY['LAK'] = Currency(code='LAK', numeric='418', decimals=2, symbol=u'₭', name=u'Kip', countries=[u'LAO PEOPLE\u2019S DEMOCRATIC REPUBLIC'])
CURRENCY['LBP'] = Currency(code='LBP', numeric='422', decimals=2, symbol=u'£', name=u'Lebanese Pound', countries=[u'LEBANON'])
CURRENCY['LKR'] = Currency(code='LKR', numeric='144', decimals=2, symbol=u'₨', name=u'Sri Lanka Rupee', countries=[u'SRI LANKA'])
CURRENCY['LRD'] = Currency(code='LRD', numeric='430', decimals=2, symbol=u'$', name=u'Liberian Dollar', countries=[u'LIBERIA'])
CURRENCY['LSL'] = Currency(code='LSL', numeric='426', decimals=2, symbol=u'', name=u'Loti', countries=[u'LESOTHO'])
CURRENCY['LTL'] = Currency(code='LTL', numeric='440', decimals=2, symbol=u'Lt', name=u'Lithuanian Litas', countries=[u'LITHUANIA'])
CURRENCY['LVL'] = Currency(code='LVL', numeric='428', decimals=2, symbol=u'Ls', name=u'Latvian Lats', countries=[u'LATVIA'])
CURRENCY['LYD'] = Currency(code='LYD', numeric='434', decimals=3, symbol=u'', name=u'Libyan Dinar', countries=[u'LIBYA'])
CURRENCY['MAD'] = Currency(code='MAD', numeric='504', decimals=2, symbol=u'', name=u'Moroccan Dirham', countries=[u'MOROCCO', u'WESTERN SAHARA'])
CURRENCY['MDL'] = Currency(code='MDL', numeric='498', decimals=2, symbol=u'', name=u'Moldovan Leu', countries=[u'MOLDOVA, REPUBLIC OF'])
CURRENCY['MGA'] = Currency(code='MGA', numeric='969', decimals=2, symbol=u'', name=u'Malagasy Ariary', countries=[u'MADAGASCAR'])
CURRENCY['MKD'] = Currency(code='MKD', numeric='807', decimals=2, symbol=u'ден', name=u'Denar', countries=[u'MACEDONIA, THE FORMER YUGOSLAV REPUBLIC OF'])
CURRENCY['MMK'] = Currency(code='MMK', numeric='104', decimals=2, symbol=u'', name=u'Kyat', countries=[u'MYANMAR'])
CURRENCY['MNT'] = Currency(code='MNT', numeric='496', decimals=2, symbol=u'₮', name=u'Tugrik', countries=[u'MONGOLIA'])
CURRENCY['MOP'] = Currency(code='MOP', numeric='446', decimals=2, symbol=u'', name=u'Pataca', countries=[u'MACAO'])
CURRENCY['MRO'] = Currency(code='MRO', numeric='478', decimals=2, symbol=u'', name=u'Ouguiya', countries=[u'MAURITANIA'])
CURRENCY['MUR'] = Currency(code='MUR', numeric='480', decimals=2, symbol=u'₨', name=u'Mauritius Rupee', countries=[u'MAURITIUS'])
CURRENCY['MVR'] = Currency(code='MVR', numeric='462', decimals=2, symbol=u'', name=u'Rufiyaa', countries=[u'MALDIVES'])
CURRENCY['MWK'] = Currency(code='MWK', numeric='454', decimals=2, symbol=u'', name=u'Kwacha', countries=[u'MALAWI'])
CURRENCY['MXN'] = Currency(code='MXN', numeric='484', decimals=2, symbol=u'$', name=u'Mexican Peso', countries=[u'MEXICO'])
CURRENCY['MXV'] = Currency(code='MXV', numeric='979', decimals=2, symbol=u'', name=u'Mexican Unidad de Inversion (UDI)', countries=[u'MEXICO'])
CURRENCY['MYR'] = Currency(code='MYR', numeric='458', decimals=2, symbol=u'RM', name=u'Malaysian Ringgit', countries=[u'MALAYSIA'])
CURRENCY['MZN'] = Currency(code='MZN', numeric='943', decimals=2, symbol=u'MT', name=u'Mozambique Metical', countries=[u'MOZAMBIQUE'])
CURRENCY['NAD'] = Currency(code='NAD', numeric='516', decimals=2, symbol=u'$', name=u'Namibia Dollar', countries=[u'NAMIBIA'])
CURRENCY['NGN'] = Currency(code='NGN', numeric='566', decimals=2, symbol=u'₦', name=u'Naira', countries=[u'NIGERIA'])
CURRENCY['NIO'] = Currency(code='NIO', numeric='558', decimals=2, symbol=u'C$', name=u'Cordoba Oro', countries=[u'NICARAGUA'])
CURRENCY['NOK'] = Currency(code='NOK', numeric='578', decimals=2, symbol=u'kr', name=u'Norwegian Krone', countries=[u'BOUVET ISLAND', u'NORWAY', u'SVALBARD AND JAN MAYEN'])
CURRENCY['NPR'] = Currency(code='NPR', numeric='524', decimals=2, symbol=u'₨', name=u'Nepalese Rupee', countries=[u'NEPAL'])
CURRENCY['NZD'] = Currency(code='NZD', numeric='554', decimals=2, symbol=u'$', name=u'New Zealand Dollar', countries=[u'COOK ISLANDS', u'NEW ZEALAND', u'NIUE', u'PITCAIRN', u'TOKELAU'])
CURRENCY['OMR'] = Currency(code='OMR', numeric='512', decimals=3, symbol=u'﷼', name=u'Rial Omani', countries=[u'OMAN'])
CURRENCY['PAB'] = Currency(code='PAB', numeric='590', decimals=2, symbol=u'B/.', name=u'Balboa', countries=[u'PANAMA'])
CURRENCY['PEN'] = Currency(code='PEN', numeric='604', decimals=2, symbol=u'S/.', name=u'Nuevo Sol', countries=[u'PERU'])
CURRENCY['PGK'] = Currency(code='PGK', numeric='598', decimals=2, symbol=u'', name=u'Kina', countries=[u'PAPUA NEW GUINEA'])
CURRENCY['PHP'] = Currency(code='PHP', numeric='608', decimals=2, symbol=u'₱', name=u'Philippine Peso', countries=[u'PHILIPPINES'])
CURRENCY['PKR'] = Currency(code='PKR', numeric='586', decimals=2, symbol=u'₨', name=u'Pakistan Rupee', countries=[u'PAKISTAN'])
CURRENCY['PLN'] = Currency(code='PLN', numeric='985', decimals=2, symbol=u'zł', name=u'Zloty', countries=[u'POLAND'])
CURRENCY['PYG'] = Currency(code='PYG', numeric='600', decimals=0, symbol=u'Gs', name=u'Guarani', countries=[u'PARAGUAY'])
CURRENCY['QAR'] = Currency(code='QAR', numeric='634', decimals=2, symbol=u'﷼', name=u'Qatari Rial', countries=[u'QATAR'])
CURRENCY['RON'] = Currency(code='RON', numeric='946', decimals=2, symbol=u'lei', name=u'New Romanian Leu', countries=[u'ROMANIA'])
CURRENCY['RSD'] = Currency(code='RSD', numeric='941', decimals=2, symbol=u'Дин.', name=u'Serbian Dinar', countries=[u'SERBIA '])
CURRENCY['RUB'] = Currency(code='RUB', numeric='643', decimals=2, symbol=u'руб', name=u'Russian Ruble', countries=[u'RUSSIAN FEDERATION'])
CURRENCY['RWF'] = Currency(code='RWF', numeric='646', decimals=0, symbol=u'', name=u'Rwanda Franc', countries=[u'RWANDA'])
CURRENCY['SAR'] = Currency(code='SAR', numeric='682', decimals=2, symbol=u'﷼', name=u'Saudi Riyal', countries=[u'SAUDI ARABIA'])
CURRENCY['SBD'] = Currency(code='SBD', numeric='090', decimals=2, symbol=u'$', name=u'Solomon Islands Dollar', countries=[u'SOLOMON ISLANDS'])
CURRENCY['SCR'] = Currency(code='SCR', numeric='690', decimals=2, symbol=u'₨', name=u'Seychelles Rupee', countries=[u'SEYCHELLES'])
CURRENCY['SDG'] = Currency(code='SDG', numeric='938', decimals=2, symbol=u'', name=u'Sudanese Pound', countries=[u'SUDAN'])
CURRENCY['SEK'] = Currency(code='SEK', numeric='752', decimals=2, symbol=u'kr', name=u'Swedish Krona', countries=[u'SWEDEN'])
CURRENCY['SGD'] = Currency(code='SGD', numeric='702', decimals=2, symbol=u'$', name=u'Singapore Dollar', countries=[u'SINGAPORE'])
CURRENCY['SHP'] = Currency(code='SHP', numeric='654', decimals=2, symbol=u'£', name=u'Saint Helena Pound', countries=[u'SAINT HELENA, ASCENSION AND TRISTAN DA CUNHA'])
CURRENCY['SLL'] = Currency(code='SLL', numeric='694', decimals=2, symbol=u'', name=u'Leone', countries=[u'SIERRA LEONE'])
CURRENCY['SOS'] = Currency(code='SOS', numeric='706', decimals=2, symbol=u'S', name=u'Somali Shilling', countries=[u'SOMALIA'])
CURRENCY['SRD'] = Currency(code='SRD', numeric='968', decimals=2, symbol=u'$', name=u'Surinam Dollar', countries=[u'SURINAME'])
CURRENCY['SSP'] = Currency(code='SSP', numeric='728', decimals=2, symbol=u'', name=u'South Sudanese Pound', countries=[u'SOUTH SUDAN'])
CURRENCY['STD'] = Currency(code='STD', numeric='678', decimals=2, symbol=u'', name=u'Dobra', countries=[u'SAO TOME AND PRINCIPE'])
CURRENCY['SVC'] = Currency(code='SVC', numeric='222', decimals=2, symbol=u'$', name=u'El Salvador Colon', countries=[u'EL SALVADOR'])
CURRENCY['SYP'] = Currency(code='SYP', numeric='760', decimals=2, symbol=u'£', name=u'Syrian Pound', countries=[u'SYRIAN ARAB REPUBLIC'])
CURRENCY['SZL'] = Currency(code='SZL', numeric='748', decimals=2, symbol=u'', name=u'Lilangeni', countries=[u'SWAZILAND'])
CURRENCY['THB'] = Currency(code='THB', numeric='764', decimals=2, symbol=u'฿', name=u'Baht', countries=[u'THAILAND'])
CURRENCY['TJS'] = Currency(code='TJS', numeric='972', decimals=2, symbol=u'', name=u'Somoni', countries=[u'TAJIKISTAN'])
CURRENCY['TMT'] = Currency(code='TMT', numeric='934', decimals=2, symbol=u'', name=u'Turkmenistan New Manat', countries=[u'TURKMENISTAN'])
CURRENCY['TND'] = Currency(code='TND', numeric='788', decimals=3, symbol=u'', name=u'Tunisian Dinar', countries=[u'TUNISIA'])
CURRENCY['TOP'] = Currency(code='TOP', numeric='776', decimals=2, symbol=u'', name=u'Pa’anga', countries=[u'TONGA'])
CURRENCY['TRY'] = Currency(code='TRY', numeric='949', decimals=2, symbol=u'TL', name=u'Turkish Lira', countries=[u'TURKEY'])
CURRENCY['TTD'] = Currency(code='TTD', numeric='780', decimals=2, symbol=u'TT$', name=u'Trinidad and Tobago Dollar', countries=[u'TRINIDAD AND TOBAGO'])
CURRENCY['TWD'] = Currency(code='TWD', numeric='901', decimals=2, symbol=u'NT$', name=u'New Taiwan Dollar', countries=[u'TAIWAN, PROVINCE OF CHINA'])
CURRENCY['TZS'] = Currency(code='TZS', numeric='834', decimals=2, symbol=u'', name=u'Tanzanian Shilling', countries=[u'TANZANIA, UNITED REPUBLIC OF'])
CURRENCY['UAH'] = Currency(code='UAH', numeric='980', decimals=2, symbol=u'₴', name=u'Hryvnia', countries=[u'UKRAINE'])
CURRENCY['UGX'] = Currency(code='UGX', numeric='800', decimals=2, symbol=u'', name=u'Uganda Shilling', countries=[u'UGANDA'])
CURRENCY['USD'] = Currency(code='USD', numeric='840', decimals=2, symbol=u'$', name=u'US Dollar', countries=[u'AMERICAN SAMOA', u'BONAIRE, SINT EUSTATIUS AND SABA', u'BRITISH INDIAN OCEAN TERRITORY', u'ECUADOR', u'EL SALVADOR', u'GUAM', u'HAITI', u'MARSHALL ISLANDS', u'MICRONESIA, FEDERATED STATES OF', u'NORTHERN MARIANA ISLANDS', u'PALAU', u'PANAMA', u'PUERTO RICO', u'TIMOR-LESTE', u'TURKS AND CAICOS ISLANDS', u'UNITED STATES', u'UNITED STATES MINOR OUTLYING ISLANDS', u'VIRGIN ISLANDS (BRITISH)', u'VIRGIN ISLANDS (US)'])
CURRENCY['USN'] = Currency(code='USN', numeric='997', decimals=2, symbol=u'$', name=u'US Dollar (Next day)', countries=[u'UNITED STATES'])
CURRENCY['USS'] = Currency(code='USS', numeric='998', decimals=2, symbol=u'$', name=u'US Dollar (Same day)', countries=[u'UNITED STATES'])
CURRENCY['UYI'] = Currency(code='UYI', numeric='940', decimals=0, symbol=u'', name=u'Uruguay Peso en Unidades Indexadas (URUIURUI)', countries=[u'URUGUAY'])
CURRENCY['UYU'] = Currency(code='UYU', numeric='858', decimals=2, symbol=u'$U', name=u'Peso Uruguayo', countries=[u'URUGUAY'])
CURRENCY['UZS'] = Currency(code='UZS', numeric='860', decimals=2, symbol=u'лв', name=u'Uzbekistan Sum', countries=[u'UZBEKISTAN'])
CURRENCY['VEF'] = Currency(code='VEF', numeric='937', decimals=2, symbol=u'Bs', name=u'Bolivar Fuerte', countries=[u'VENEZUELA, BOLIVARIAN REPUBLIC OF'])
CURRENCY['VND'] = Currency(code='VND', numeric='704', decimals=0, symbol=u'₫', name=u'Dong', countries=[u'VIET NAM'])
CURRENCY['VUV'] = Currency(code='VUV', numeric='548', decimals=0, symbol=u'', name=u'Vatu', countries=[u'VANUATU'])
CURRENCY['WST'] = Currency(code='WST', numeric='882', decimals=2, symbol=u'', name=u'Tala', countries=[u'SAMOA'])
CURRENCY['XAF'] = Currency(code='XAF', numeric='950', decimals=0, symbol=u'', name=u'CFA Franc BEAC', countries=[u'CAMEROON', u'CENTRAL AFRICAN REPUBLIC', u'CHAD', u'CONGO', u'EQUATORIAL GUINEA', u'GABON'])
CURRENCY['XAG'] = Currency(code='XAG', numeric='961', decimals=0, symbol=u'', name=u'Silver', countries=[u'ZZ11_Silver'])
CURRENCY['XAU'] = Currency(code='XAU', numeric='959', decimals=0, symbol=u'', name=u'Gold', countries=[u'ZZ08_Gold'])
CURRENCY['XBA'] = Currency(code='XBA', numeric='955', decimals=0, symbol=u'', name=u'Bond Markets Unit European Composite Unit (EURCO)', countries=[u'ZZ01_Bond Markets Unit European_EURCO'])
CURRENCY['XBB'] = Currency(code='XBB', numeric='956', decimals=0, symbol=u'', name=u'Bond Markets Unit European Monetary Unit (E.M.U.-6)', countries=[u'ZZ02_Bond Markets Unit European_EMU-6'])
CURRENCY['XBC'] = Currency(code='XBC', numeric='957', decimals=0, symbol=u'', name=u'Bond Markets Unit European Unit of Account 9 (E.U.A.-9)', countries=[u'ZZ03_Bond Markets Unit European_EUA-9'])
CURRENCY['XBD'] = Currency(code='XBD', numeric='958', decimals=0, symbol=u'', name=u'Bond Markets Unit European Unit of Account 17 (E.U.A.-17)', countries=[u'ZZ04_Bond Markets Unit European_EUA-17'])
CURRENCY['XCD'] = Currency(code='XCD', numeric='951', decimals=2, symbol=u'$', name=u'East Caribbean Dollar', countries=[u'ANGUILLA', u'ANTIGUA AND BARBUDA', u'DOMINICA', u'GRENADA', u'MONTSERRAT', u'SAINT KITTS AND NEVIS', u'SAINT LUCIA', u'SAINT VINCENT AND THE GRENADINES'])
CURRENCY['XDR'] = Currency(code='XDR', numeric='960', decimals=0, symbol=u'', name=u'SDR (Special Drawing Right)', countries=[u'INTERNATIONAL MONETARY FUND (IMF)\xa0'])
CURRENCY['XFU'] = Currency(code='XFU', numeric='Nil', decimals=0, symbol=u'', name=u'UIC-Franc', countries=[u'ZZ05_UIC-Franc'])
CURRENCY['XOF'] = Currency(code='XOF', numeric='952', decimals=0, symbol=u'', name=u'CFA Franc BCEAO', countries=[u'BENIN', u'BURKINA FASO', u"C\xd4TE D'IVOIRE", u'GUINEA-BISSAU', u'MALI', u'NIGER', u'SENEGAL', u'TOGO'])
CURRENCY['XPD'] = Currency(code='XPD', numeric='964', decimals=0, symbol=u'', name=u'Palladium', countries=[u'ZZ09_Palladium'])
CURRENCY['XPF'] = Currency(code='XPF', numeric='953', decimals=0, symbol=u'', name=u'CFP Franc', countries=[u'FRENCH POLYNESIA', u'NEW CALEDONIA', u'WALLIS AND FUTUNA'])
CURRENCY['XPT'] = Currency(code='XPT', numeric='962', decimals=0, symbol=u'', name=u'Platinum', countries=[u'ZZ10_Platinum'])
CURRENCY['XSU'] = Currency(code='XSU', numeric='994', decimals=0, symbol=u'', name=u'Sucre', countries=[u'SISTEMA UNITARIO DE COMPENSACION REGIONAL DE PAGOS "SUCRE" '])
CURRENCY['XTS'] = Currency(code='XTS', numeric='963', decimals=0, symbol=u'', name=u'Codes specifically reserved for testing purposes', countries=[u'ZZ06_Testing_Code'])
CURRENCY['XUA'] = Currency(code='XUA', numeric='965', decimals=0, symbol=u'', name=u'ADB Unit of Account', countries=[u'MEMBER COUNTRIES OF THE AFRICAN DEVELOPMENT BANK GROUP'])
CURRENCY['XXX'] = Currency(code='XXX', numeric='999', decimals=0, symbol=u'', name=u'The codes assigned for transactions where no currency is involved', countries=[u'ZZ07_No_Currency'])
CURRENCY['YER'] = Currency(code='YER', numeric='886', decimals=2, symbol=u'﷼', name=u'Yemeni Rial', countries=[u'YEMEN'])
CURRENCY['ZAR'] = Currency(code='ZAR', numeric='710', decimals=2, symbol=u'R', name=u'Rand', countries=[u'LESOTHO', u'NAMIBIA', u'SOUTH AFRICA'])
CURRENCY['ZMK'] = Currency(code='ZMK', numeric='894', decimals=2, symbol=u'', name=u'Zambian Kwacha', countries=[u'ZAMBIA'])
CURRENCY['ZWL'] = Currency(code='ZWL', numeric='932', decimals=2, symbol=u'', name=u'Zimbabwe Dollar', countries=[u'ZIMBABWE'])
