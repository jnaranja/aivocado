"""
AI advisor for avocado plant growth optimization using Claude.
"""

import os
from anthropic import Anthropic
from sensors import SensorReading
from display import OPTIMAL_RANGES


SYSTEM_PROMPT = """You are an expert botanist specializing in avocado plant cultivation.
Your role is to analyze sensor readings from an avocado plant monitoring system and provide
concise, actionable recommendations to optimize plant growth.

Optimal conditions for avocado plants:
- Temperature: 18-26°C (avoid frost and extreme heat)
- Humidity: 50-70% (moderate humidity)
- CO2: 400-800 ppm (normal atmospheric to slightly elevated)
- Light: 2,000-10,000 lux (bright indirect light, avocados are understory trees)

Keep your responses brief (2-3 sentences max) and focus on the most important adjustment needed.
If all readings are optimal, provide a short encouraging status update."""


class AIAdvisor:
    """Claude-powered advisor for plant growth optimization."""

    def __init__(self, api_key: str = None):
        self._api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self._client = None
        if self._api_key:
            self._client = Anthropic(api_key=self._api_key)

    def get_recommendation(self, reading: SensorReading) -> str:
        """Get AI recommendation based on current sensor readings."""
        if not self._client:
            return self._get_fallback_recommendation(reading)

        prompt = self._build_prompt(reading)

        try:
            response = self._client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=150,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            print(f"AI API error: {e}")
            return self._get_fallback_recommendation(reading)

    def _build_prompt(self, reading: SensorReading) -> str:
        """Build the prompt with current sensor readings."""
        return f"""Current sensor readings for my avocado plant:
- Temperature: {reading.temperature_c:.1f}°C
- Humidity: {reading.humidity_percent:.1f}%
- CO2: {reading.co2_ppm:.0f} ppm
- Light: {reading.light_lux:.0f} lux

What adjustments should I make for optimal growth?"""

    def _get_fallback_recommendation(self, reading: SensorReading) -> str:
        """Generate basic recommendation without AI when API is unavailable."""
        issues = []

        temp_low, temp_high = OPTIMAL_RANGES['temperature']
        if reading.temperature_c < temp_low:
            issues.append("Temperature too low - consider warming the area")
        elif reading.temperature_c > temp_high:
            issues.append("Temperature too high - improve ventilation")

        hum_low, hum_high = OPTIMAL_RANGES['humidity']
        if reading.humidity_percent < hum_low:
            issues.append("Humidity too low - mist leaves or use humidifier")
        elif reading.humidity_percent > hum_high:
            issues.append("Humidity too high - improve air circulation")

        co2_low, co2_high = OPTIMAL_RANGES['co2']
        if reading.co2_ppm < co2_low:
            issues.append("CO2 below normal - ensure adequate ventilation")
        elif reading.co2_ppm > co2_high:
            issues.append("CO2 elevated - increase fresh air exchange")

        light_low, light_high = OPTIMAL_RANGES['light']
        if reading.light_lux < light_low:
            issues.append("Light insufficient - move closer to window or add grow light")
        elif reading.light_lux > light_high:
            issues.append("Light too intense - add shade or move plant")

        if not issues:
            return "All conditions optimal! Your avocado plant is in a great environment."

        return " | ".join(issues[:2])  # Return top 2 issues
