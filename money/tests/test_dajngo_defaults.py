import pytest

from money.money import Money
from money.tests.models import ALL_PARAMETRIZED_MODELS


@pytest.mark.django_db
@pytest.mark.parametrize("cls", ALL_PARAMETRIZED_MODELS)
def test_manager_create(cls):
    instance = cls.objects.create()
    assert instance.value == instance.expected_value()
    assert instance.value.amount == instance.expected_value().amount
    assert instance.value.currency == instance.expected_value().currency


@pytest.mark.parametrize("cls", ALL_PARAMETRIZED_MODELS)
def test_instance_create(cls):
    instance = cls()  # should not touch the db
    assert instance.value == instance.expected_value()
    assert instance.value.amount == instance.expected_value().amount
    assert instance.value.currency == instance.expected_value().currency


@pytest.mark.django_db
@pytest.mark.parametrize("cls", ALL_PARAMETRIZED_MODELS)
def test_instance_save(cls):
    instance = cls()
    instance.save()
    assert instance.value == instance.expected_value()
    assert instance.value.amount == instance.expected_value().amount
    assert instance.value.currency == instance.expected_value().currency


@pytest.mark.django_db
@pytest.mark.parametrize("cls", ALL_PARAMETRIZED_MODELS)
def test_manager_create_override_with_money(cls):
    overridden_value = Money("9876", "EUR")
    instance = cls.objects.create(value=overridden_value)
    assert instance.value != instance.expected_value()
    assert instance.value.amount != instance.expected_value().amount
    assert instance.value.currency != instance.expected_value().currency

    assert instance.value == overridden_value
    assert instance.value.amount == overridden_value.amount
    assert instance.value.currency == overridden_value.currency


@pytest.mark.parametrize("cls", ALL_PARAMETRIZED_MODELS)
def test_instance_create_override_with_money(cls):
    overridden_value = Money("8765", "EUR")
    instance = cls(value=overridden_value)
    assert instance.value != instance.expected_value()
    assert instance.value.amount != instance.expected_value().amount
    assert instance.value.currency != instance.expected_value().currency

    assert instance.value == overridden_value
    assert instance.value.amount == overridden_value.amount
    assert instance.value.currency == overridden_value.currency
