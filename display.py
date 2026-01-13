"""
Terminal display for avocado plant monitoring dashboard.
"""

import os
from sensors import SensorReading


# Optimal ranges for avocado plant growth
OPTIMAL_RANGES = {
    'temperature': (18, 26),      # Celsius - avocados like 18-26C
    'humidity': (50, 70),         # Percent - moderate humidity
    'co2': (400, 800),            # PPM - normal to slightly elevated
    'light': (2000, 10000),       # Lux - bright indirect light (understory plant)
}


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_status_indicator(value: float, optimal_range: tuple[float, float]) -> str:
    """Return status indicator based on whether value is in optimal range."""
    low, high = optimal_range
    if low <= value <= high:
        return "[OK]"
    elif value < low:
        return "[LOW]"
    else:
        return "[HIGH]"


def create_bar(value: float, min_val: float, max_val: float, width: int = 30) -> str:
    """Create a visual bar representation of a value."""
    normalized = (value - min_val) / (max_val - min_val)
    normalized = max(0, min(1, normalized))
    filled = int(normalized * width)
    return "[" + "#" * filled + "-" * (width - filled) + "]"


def display_reading(reading: SensorReading, ai_recommendation: str = None):
    """Display sensor readings in a formatted dashboard."""
    clear_screen()

    print("=" * 60)
    print("         AVOCADO PLANT MONITORING SYSTEM")
    print("=" * 60)
    print(f"  Last Update: {reading.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()

    # Temperature
    temp_status = get_status_indicator(reading.temperature_c, OPTIMAL_RANGES['temperature'])
    temp_bar = create_bar(reading.temperature_c, 10, 40)
    print(f"  TEMPERATURE {temp_status}")
    print(f"  {reading.temperature_c:6.1f} C   {temp_bar}")
    print(f"  Optimal: {OPTIMAL_RANGES['temperature'][0]}-{OPTIMAL_RANGES['temperature'][1]} C")
    print()

    # Humidity
    hum_status = get_status_indicator(reading.humidity_percent, OPTIMAL_RANGES['humidity'])
    hum_bar = create_bar(reading.humidity_percent, 0, 100)
    print(f"  HUMIDITY {hum_status}")
    print(f"  {reading.humidity_percent:6.1f} %   {hum_bar}")
    print(f"  Optimal: {OPTIMAL_RANGES['humidity'][0]}-{OPTIMAL_RANGES['humidity'][1]} %")
    print()

    # CO2
    co2_status = get_status_indicator(reading.co2_ppm, OPTIMAL_RANGES['co2'])
    co2_bar = create_bar(reading.co2_ppm, 300, 1500)
    print(f"  CO2 LEVEL {co2_status}")
    print(f"  {reading.co2_ppm:6.0f} ppm {co2_bar}")
    print(f"  Optimal: {OPTIMAL_RANGES['co2'][0]}-{OPTIMAL_RANGES['co2'][1]} ppm")
    print()

    # Light
    light_status = get_status_indicator(reading.light_lux, OPTIMAL_RANGES['light'])
    light_bar = create_bar(reading.light_lux, 0, 20000)
    print(f"  LIGHT LEVEL {light_status}")
    print(f"  {reading.light_lux:6.0f} lux {light_bar}")
    print(f"  Optimal: {OPTIMAL_RANGES['light'][0]}-{OPTIMAL_RANGES['light'][1]} lux")
    print()

    print("=" * 60)

    if ai_recommendation:
        print("  AI RECOMMENDATIONS")
        print("-" * 60)
        # Word wrap the recommendation
        words = ai_recommendation.split()
        line = "  "
        for word in words:
            if len(line) + len(word) + 1 > 58:
                print(line)
                line = "  " + word
            else:
                line += " " + word if line != "  " else word
        if line.strip():
            print(line)
        print("=" * 60)

    print()
    print("  Press Ctrl+C to exit")
