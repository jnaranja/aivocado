"""Tests for display module."""

import pytest

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from display import get_status_indicator, create_bar, OPTIMAL_RANGES


class TestGetStatusIndicator:
    """Tests for status indicator function."""

    def test_value_in_range_returns_ok(self):
        """Test that value within range returns OK."""
        result = get_status_indicator(22.0, (18, 26))
        assert result == "[OK]"

    def test_value_at_low_boundary_returns_ok(self):
        """Test that value at lower boundary is OK."""
        result = get_status_indicator(18.0, (18, 26))
        assert result == "[OK]"

    def test_value_at_high_boundary_returns_ok(self):
        """Test that value at upper boundary is OK."""
        result = get_status_indicator(26.0, (18, 26))
        assert result == "[OK]"

    def test_value_below_range_returns_low(self):
        """Test that value below range returns LOW."""
        result = get_status_indicator(10.0, (18, 26))
        assert result == "[LOW]"

    def test_value_above_range_returns_high(self):
        """Test that value above range returns HIGH."""
        result = get_status_indicator(30.0, (18, 26))
        assert result == "[HIGH]"

    def test_temperature_optimal_ranges(self):
        """Test status for temperature optimal ranges."""
        low, high = OPTIMAL_RANGES["temperature"]
        assert get_status_indicator(low, (low, high)) == "[OK]"
        assert get_status_indicator(high, (low, high)) == "[OK]"
        assert get_status_indicator(low - 1, (low, high)) == "[LOW]"
        assert get_status_indicator(high + 1, (low, high)) == "[HIGH]"


class TestCreateBar:
    """Tests for visual bar creation function."""

    def test_bar_minimum_value(self):
        """Test bar at minimum value."""
        bar = create_bar(0, 0, 100, width=10)
        assert bar == "[----------]"

    def test_bar_maximum_value(self):
        """Test bar at maximum value."""
        bar = create_bar(100, 0, 100, width=10)
        assert bar == "[##########]"

    def test_bar_middle_value(self):
        """Test bar at 50% value."""
        bar = create_bar(50, 0, 100, width=10)
        assert bar == "[#####-----]"

    def test_bar_below_minimum_clamped(self):
        """Test that values below minimum are clamped."""
        bar = create_bar(-50, 0, 100, width=10)
        assert bar == "[----------]"

    def test_bar_above_maximum_clamped(self):
        """Test that values above maximum are clamped."""
        bar = create_bar(200, 0, 100, width=10)
        assert bar == "[##########]"

    def test_bar_custom_width(self):
        """Test bar with custom width."""
        bar = create_bar(50, 0, 100, width=20)
        assert len(bar) == 22  # 20 + 2 brackets
        assert bar.count("#") == 10
        assert bar.count("-") == 10

    def test_bar_default_width(self):
        """Test bar with default width of 30."""
        bar = create_bar(50, 0, 100)
        assert len(bar) == 32  # 30 + 2 brackets


class TestOptimalRanges:
    """Tests for optimal range constants."""

    def test_temperature_range_exists(self):
        """Test temperature range is defined."""
        assert "temperature" in OPTIMAL_RANGES
        assert len(OPTIMAL_RANGES["temperature"]) == 2

    def test_humidity_range_exists(self):
        """Test humidity range is defined."""
        assert "humidity" in OPTIMAL_RANGES
        assert len(OPTIMAL_RANGES["humidity"]) == 2

    def test_co2_range_exists(self):
        """Test CO2 range is defined."""
        assert "co2" in OPTIMAL_RANGES
        assert len(OPTIMAL_RANGES["co2"]) == 2

    def test_light_range_exists(self):
        """Test light range is defined."""
        assert "light" in OPTIMAL_RANGES
        assert len(OPTIMAL_RANGES["light"]) == 2

    def test_temperature_range_reasonable(self):
        """Test temperature range is reasonable for avocados."""
        low, high = OPTIMAL_RANGES["temperature"]
        assert 15 <= low <= 20  # Not too cold
        assert 24 <= high <= 30  # Not too hot

    def test_ranges_are_ordered(self):
        """Test all ranges have low < high."""
        for name, (low, high) in OPTIMAL_RANGES.items():
            assert low < high, f"{name} range is invalid: {low} >= {high}"
