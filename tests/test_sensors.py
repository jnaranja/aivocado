"""Tests for sensor module."""

import pytest
from datetime import datetime

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sensors import SensorReading, MockSensors, get_sensor_interface


class TestSensorReading:
    """Tests for SensorReading dataclass."""

    def test_sensor_reading_creation(self):
        """Test creating a SensorReading with valid values."""
        reading = SensorReading(
            timestamp=datetime.now(),
            temperature_c=22.5,
            humidity_percent=65.0,
            co2_ppm=450.0,
            light_lux=5000.0,
        )
        assert reading.temperature_c == 22.5
        assert reading.humidity_percent == 65.0
        assert reading.co2_ppm == 450.0
        assert reading.light_lux == 5000.0

    def test_sensor_reading_has_timestamp(self):
        """Test that sensor reading includes timestamp."""
        now = datetime.now()
        reading = SensorReading(
            timestamp=now,
            temperature_c=22.0,
            humidity_percent=60.0,
            co2_ppm=400.0,
            light_lux=3000.0,
        )
        assert reading.timestamp == now


class TestMockSensors:
    """Tests for MockSensors class."""

    def test_mock_sensors_returns_reading(self):
        """Test that MockSensors returns a SensorReading."""
        sensors = MockSensors()
        reading = sensors.read()
        assert isinstance(reading, SensorReading)

    def test_mock_sensors_realistic_temperature(self):
        """Test that mock temperature is in realistic range."""
        sensors = MockSensors()
        reading = sensors.read()
        # Base temp is 22 +/- 2
        assert 15 <= reading.temperature_c <= 30

    def test_mock_sensors_humidity_bounded(self):
        """Test that mock humidity is bounded 0-100."""
        sensors = MockSensors()
        for _ in range(100):  # Multiple reads to test bounds
            reading = sensors.read()
            assert 0 <= reading.humidity_percent <= 100

    def test_mock_sensors_co2_non_negative(self):
        """Test that CO2 is never below realistic minimum."""
        sensors = MockSensors()
        for _ in range(100):
            reading = sensors.read()
            assert reading.co2_ppm >= 300

    def test_mock_sensors_light_non_negative(self):
        """Test that light level is never negative."""
        sensors = MockSensors()
        for _ in range(100):
            reading = sensors.read()
            assert reading.light_lux >= 0

    def test_mock_sensors_multiple_reads_vary(self):
        """Test that multiple readings have some variation."""
        sensors = MockSensors()
        readings = [sensors.read() for _ in range(10)]
        temps = [r.temperature_c for r in readings]
        # Should have at least some variation
        assert max(temps) != min(temps)


class TestGetSensorInterface:
    """Tests for sensor interface factory function."""

    def test_get_mock_interface(self):
        """Test getting mock sensor interface."""
        interface = get_sensor_interface(use_mock=True)
        assert isinstance(interface, MockSensors)

    def test_mock_is_default(self):
        """Test that mock is the default."""
        interface = get_sensor_interface()
        assert isinstance(interface, MockSensors)

    def test_mock_interface_can_read(self):
        """Test that mock interface produces valid readings."""
        interface = get_sensor_interface(use_mock=True)
        reading = interface.read()
        assert isinstance(reading, SensorReading)
        assert reading.timestamp is not None
