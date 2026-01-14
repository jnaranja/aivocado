"""
API client for pushing sensor readings and AI analysis to external service.
"""

import os
import httpx
from datetime import datetime
from sensors import SensorReading


class APIClient:
    """Client for pushing updates to external API."""

    def __init__(self, base_url: str = None, api_key: str = None):
        self._base_url = base_url or os.getenv("AIVOCADO_API_URL")
        self._api_key = api_key or os.getenv("AIVOCADO_API_KEY")
        self._enabled = bool(self._base_url and self._api_key)

        if not self._enabled:
            print("API client disabled: missing AIVOCADO_API_URL or AIVOCADO_API_KEY")

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json"
        }

    def push_reading(self, reading: SensorReading) -> bool:
        """
        POST /readings
        Push sensor reading to external API.

        Request body:
        {
            "timestamp": "2026-01-14T10:30:00Z",
            "temperature_c": 22.5,
            "humidity_percent": 65.0,
            "co2_ppm": 450,
            "light_lux": 5000
        }
        """
        if not self._enabled:
            return False

        payload = {
            "timestamp": reading.timestamp.isoformat(),
            "temperature_c": reading.temperature_c,
            "humidity_percent": reading.humidity_percent,
            "co2_ppm": reading.co2_ppm,
            "light_lux": reading.light_lux
        }

        try:
            resp = httpx.post(
                f"{self._base_url}/readings",
                json=payload,
                headers=self._headers(),
                timeout=5.0
            )
            return resp.status_code == 200
        except Exception as e:
            print(f"API error (push_reading): {e}")
            return False

    def push_analysis(self, reading: SensorReading, recommendation: str) -> bool:
        """
        POST /analysis
        Push AI analysis to external API.

        Request body:
        {
            "timestamp": "2026-01-14T10:30:00Z",
            "reading": {
                "temperature_c": 22.5,
                "humidity_percent": 65.0,
                "co2_ppm": 450,
                "light_lux": 5000
            },
            "recommendation": "All conditions optimal. Your avocado is thriving."
        }
        """
        if not self._enabled:
            return False

        payload = {
            "timestamp": datetime.now().isoformat(),
            "reading": {
                "temperature_c": reading.temperature_c,
                "humidity_percent": reading.humidity_percent,
                "co2_ppm": reading.co2_ppm,
                "light_lux": reading.light_lux
            },
            "recommendation": recommendation
        }

        try:
            resp = httpx.post(
                f"{self._base_url}/analysis",
                json=payload,
                headers=self._headers(),
                timeout=5.0
            )
            return resp.status_code == 200
        except Exception as e:
            print(f"API error (push_analysis): {e}")
            return False

    def push_alert(self, alert_type: str, message: str, reading: SensorReading = None) -> bool:
        """
        POST /alerts
        Push alert when conditions are out of range.

        Request body:
        {
            "timestamp": "2026-01-14T10:30:00Z",
            "type": "temperature_high",
            "message": "Temperature is above optimal range",
            "reading": { ... }  // optional
        }
        """
        if not self._enabled:
            return False

        payload = {
            "timestamp": datetime.now().isoformat(),
            "type": alert_type,
            "message": message
        }

        if reading:
            payload["reading"] = {
                "temperature_c": reading.temperature_c,
                "humidity_percent": reading.humidity_percent,
                "co2_ppm": reading.co2_ppm,
                "light_lux": reading.light_lux
            }

        try:
            resp = httpx.post(
                f"{self._base_url}/alerts",
                json=payload,
                headers=self._headers(),
                timeout=5.0
            )
            return resp.status_code == 200
        except Exception as e:
            print(f"API error (push_alert): {e}")
            return False
