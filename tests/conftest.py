"""Shared test fixtures for AIVOCADO tests."""

import pytest
from datetime import datetime

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from sensors import SensorReading


@pytest.fixture
def sample_reading() -> SensorReading:
    """Create a sample sensor reading with optimal values."""
    return SensorReading(
        timestamp=datetime(2026, 1, 15, 12, 0, 0),
        temperature_c=22.0,
        humidity_percent=60.0,
        co2_ppm=500.0,
        light_lux=5000.0,
    )


@pytest.fixture
def low_temp_reading() -> SensorReading:
    """Create a reading with low temperature."""
    return SensorReading(
        timestamp=datetime(2026, 1, 15, 12, 0, 0),
        temperature_c=10.0,
        humidity_percent=60.0,
        co2_ppm=500.0,
        light_lux=5000.0,
    )


@pytest.fixture
def high_temp_reading() -> SensorReading:
    """Create a reading with high temperature."""
    return SensorReading(
        timestamp=datetime(2026, 1, 15, 12, 0, 0),
        temperature_c=35.0,
        humidity_percent=60.0,
        co2_ppm=500.0,
        light_lux=5000.0,
    )


@pytest.fixture
def all_out_of_range_reading() -> SensorReading:
    """Create a reading with all values out of optimal range."""
    return SensorReading(
        timestamp=datetime(2026, 1, 15, 12, 0, 0),
        temperature_c=35.0,  # Too high
        humidity_percent=20.0,  # Too low
        co2_ppm=1200.0,  # Too high
        light_lux=500.0,  # Too low
    )
