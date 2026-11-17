
import pytest
from fuel_station import fuel_bill, pump_allowed, session_status


# FUEL BILL TEST CASES

def test_invalid_fuel_grade():
    with pytest.raises(ValueError):
        fuel_bill("kerosene", 20, "silver")


def test_negative_litres():
    with pytest.raises(ValueError):
        fuel_bill("regular", -5, "silver")


def test_regular_fuel_within_covered_litres():
    assert fuel_bill("regular", 8, "silver") == 0


def test_gold_regular_fuel_coverage():
    assert fuel_bill("regular", 14, "gold") == 0


def test_gold_premium_fuel_coverage():
    assert fuel_bill("premium", 19, "gold") == 0


def test_diesel_with_extra_litres():
    assert fuel_bill("diesel", 25, "silver") == 450


def test_regular_fuel_with_extra_litres():
    assert fuel_bill("regular", 20, "silver") == 1050


def test_diesel_large_extra_litres():
    assert fuel_bill("diesel", 60, "silver") == 3360


def test_regular_large_extra_litres():
    assert fuel_bill("regular", 50, "silver") == 3960


def test_gold_regular_large_extra_litres():
    assert fuel_bill("regular", 60, "gold") == 4275


# PUMP ALLOWED TEST CASES

def test_fleet_within_limit():
    assert pump_allowed(150, 3, True) is True


def test_fleet_above_limit():
    assert pump_allowed(250, 3, True) is False


def test_non_fleet_within_limit():
    assert pump_allowed(50, 1, False) is True


def test_non_fleet_above_litre_limit():
    assert pump_allowed(70, 1, False) is False


def test_non_fleet_multiple_containers():
    assert pump_allowed(50, 2, False) is False


# SESSION STATUS TEST CASES

def test_card_payment_active_day():
    assert session_status(60, True, False) == "active"


def test_cash_payment_active_day():
    assert session_status(30, False, False) == "active"


def test_card_payment_active_night():
    assert session_status(90, True, True) == "active"


def test_warning_status():
    assert session_status(50, True, False) == "warning"


def test_night_warning_status():
    assert session_status(80, True, True) == "warning"


def test_timed_out_status():
    assert session_status(10, False, False) == "timed_out"
