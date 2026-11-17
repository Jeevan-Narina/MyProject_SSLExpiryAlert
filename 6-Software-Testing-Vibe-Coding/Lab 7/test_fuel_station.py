
from hypothesis import given, strategies as st
from fuel_station import parse_purchase, volume_average, payable_bill
import math


# Test 1: Fuzz testing parse_purchase()

@given(st.text())
def test_parse_purchase_no_crash(s):
    try:
        result = parse_purchase(s)

        assert isinstance(result, tuple)
        assert len(result) == 2
        assert result[0].strip() != ""
        assert math.isfinite(result[1])
        assert result[1] > 0

    except ValueError:
        # Invalid input must be rejected safely.
        pass


# Test 2: Fuzz testing volume_average()

@given(st.text())
def test_volume_average_no_crash(s):
    try:
        result = volume_average(s)

        assert isinstance(result, int)
        assert result >= 0

    except ValueError:
        # Invalid input must be rejected safely.
        pass


# Test 3: Fuzz testing payable_bill()

@given(st.text())
def test_payable_bill_no_crash(s):
    try:
        result = payable_bill(s)

        assert math.isfinite(result)
        assert result >= 0

    except ValueError:
        # Invalid input must be rejected safely.
        pass
