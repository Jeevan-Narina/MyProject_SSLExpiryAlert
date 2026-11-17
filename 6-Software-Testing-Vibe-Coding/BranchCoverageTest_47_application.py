
import pytest
from fuel_station import fuel_bill, pump_allowed, session_status


# FUEL BILL - BRANCH COVERAGE TESTS

def test_invalid_fuel_grade():
    with pytest.raises(ValueError):
        fuel_bill("kerosene", 20, "silver")


def test_negative_litres():
    with pytest.raises(ValueError):
        fuel_bill("regular", -5, "silver")


def test_regular_fuel_within_coverage():
    assert fuel_bill("regular", 8, "silver") == 0


def test_gold_regular_coverage():
    assert fuel_bill("regular", 14, "gold") == 0


def test_gold_diesel_coverage():
    assert fuel_bill("diesel", 20, "gold") == 0


def test_diesel_with_extra_litres():
    assert fuel_bill("diesel", 25, "silver") == 450


def test_regular_with_extra_litres():
    assert fuel_bill("regular", 20, "silver") == 1050


def test_extra_litres_exactly_30():
    assert fuel_bill("regular", 40, "silver") == 3150


def test_large_extra_litres_silver():
    assert fuel_bill("regular", 50, "silver") == 3960


def test_large_extra_litres_gold():
    assert fuel_bill("regular", 60, "gold") == 4275


# PUMP ALLOWED - BRANCH COVERAGE TESTS

def test_fleet_within_limit():
    assert pump_allowed(150, 3, True) is True


def test_fleet_above_limit():
    assert pump_allowed(250, 3, True) is False


def test_non_fleet_within_limit_one_container():
    assert pump_allowed(50, 1, False) is True


def test_non_fleet_above_litre_limit():
    assert pump_allowed(70, 1, False) is False


def test_non_fleet_multiple_containers():
    assert pump_allowed(50, 2, False) is False


# SESSION STATUS - BRANCH COVERAGE TESTS

def test_card_payment_day_active():
    assert session_status(60, True, False) == "active"


def test_cash_payment_day_active():
    assert session_status(30, False, False) == "active"


def test_card_payment_night_active():
    assert session_status(90, True, True) == "active"


def test_cash_payment_night_active():
    assert session_status(60, False, True) == "active"


def test_card_payment_warning():
    assert session_status(50, True, False) == "warning"


def test_cash_payment_warning():
    assert session_status(20, False, False) == "warning"


def test_night_warning():
    assert session_status(80, True, True) == "warning"


def test_timed_out():
    assert session_status(10, False, False) == "timed_out"
