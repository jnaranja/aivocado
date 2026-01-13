"""
Sensor interface for avocado plant monitoring.
Supports both mock data (for testing) and real Raspberry Pi sensors.
"""

import random
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass
class SensorReading:
    """Container for all sensor readings at a point in time."""
    timestamp: datetime
    temperature_c: float  # Celsius
    humidity_percent: float  # 0-100%
    co2_ppm: float  # Parts per million
    light_lux: float  # Lux


class SensorInterface(Protocol):
    """Protocol for sensor implementations."""
    def read(self) -> SensorReading:
        """Read current sensor values."""
        ...


class MockSensors:
    """Mock sensor implementation for testing without hardware."""

    def __init__(self):
        # Base values that drift slightly over time
        self._base_temp = 22.0
        self._base_humidity = 65.0
        self._base_co2 = 450.0
        self._base_light = 5000.0

    def read(self) -> SensorReading:
        """Generate realistic mock sensor readings."""
        return SensorReading(
            timestamp=datetime.now(),
            temperature_c=self._base_temp + random.uniform(-2, 2),
            humidity_percent=max(0, min(100, self._base_humidity + random.uniform(-5, 5))),
            co2_ppm=max(300, self._base_co2 + random.uniform(-50, 50)),
            light_lux=max(0, self._base_light + random.uniform(-1000, 1000)),
        )


class RaspberryPiSensors:
    """
    Real Raspberry Pi sensor implementation.
    Requires: DHT22 (temp/humidity), MH-Z19 (CO2), BH1750 (light)
    """

    def __init__(self):
        self._dht_pin = 4  # GPIO pin for DHT22
        self._initialized = False
        self._init_sensors()

    def _init_sensors(self):
        """Initialize sensor connections."""
        try:
            import board
            import adafruit_dht
            import smbus2

            self._dht = adafruit_dht.DHT22(board.D4)
            self._bus = smbus2.SMBus(1)
            self._initialized = True
        except ImportError:
            print("Warning: Raspberry Pi sensor libraries not available.")
            print("Install with: pip install adafruit-circuitpython-dht smbus2")
            self._initialized = False
        except Exception as e:
            print(f"Warning: Could not initialize sensors: {e}")
            self._initialized = False

    def _read_co2(self) -> float:
        """Read CO2 from MH-Z19 sensor via UART."""
        try:
            import serial
            ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)
            ser.write(b'\xff\x01\x86\x00\x00\x00\x00\x00\x79')
            response = ser.read(9)
            ser.close()
            if len(response) == 9:
                return response[2] * 256 + response[3]
        except Exception:
            pass
        return 400.0  # Default value

    def _read_light(self) -> float:
        """Read light level from BH1750 sensor via I2C."""
        try:
            BH1750_ADDR = 0x23
            self._bus.write_byte(BH1750_ADDR, 0x10)
            import time
            time.sleep(0.2)
            data = self._bus.read_i2c_block_data(BH1750_ADDR, 0x10, 2)
            return (data[0] << 8 | data[1]) / 1.2
        except Exception:
            return 5000.0  # Default value

    def read(self) -> SensorReading:
        """Read all sensors and return combined reading."""
        if not self._initialized:
            # Fall back to mock data if sensors not available
            return MockSensors().read()

        try:
            temp = self._dht.temperature
            humidity = self._dht.humidity
        except Exception:
            temp = 22.0
            humidity = 60.0

        return SensorReading(
            timestamp=datetime.now(),
            temperature_c=temp or 22.0,
            humidity_percent=humidity or 60.0,
            co2_ppm=self._read_co2(),
            light_lux=self._read_light(),
        )


def get_sensor_interface(use_mock: bool = True) -> SensorInterface:
    """Factory function to get appropriate sensor interface."""
    if use_mock:
        return MockSensors()
    return RaspberryPiSensors()
