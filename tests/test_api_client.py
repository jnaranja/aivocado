"""Tests for API client module."""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from api_client import APIClient
from sensors import SensorReading


class TestAPIClientInit:
    """Tests for APIClient initialization."""

    def test_init_disabled_without_config(self):
        """Test client is disabled without URL and key."""
        with patch.dict("os.environ", {}, clear=True):
            client = APIClient()
            assert client._enabled is False

    def test_init_disabled_without_url(self):
        """Test client is disabled without URL."""
        with patch.dict("os.environ", {"AIVOCADO_API_KEY": "key"}, clear=True):
            client = APIClient()
            assert client._enabled is False

    def test_init_disabled_without_key(self):
        """Test client is disabled without key."""
        with patch.dict("os.environ", {"AIVOCADO_API_URL": "http://example.com"}, clear=True):
            client = APIClient()
            assert client._enabled is False

    def test_init_enabled_with_both(self):
        """Test client is enabled with both URL and key."""
        client = APIClient(base_url="http://example.com", api_key="test-key")
        assert client._enabled is True

    def test_init_from_env(self):
        """Test initialization from environment."""
        env = {
            "AIVOCADO_API_URL": "http://example.com",
            "AIVOCADO_API_KEY": "env-key",
        }
        with patch.dict("os.environ", env, clear=True):
            client = APIClient()
            assert client._enabled is True
            assert client._base_url == "http://example.com"
            assert client._api_key == "env-key"


class TestAPIClientHeaders:
    """Tests for API client headers."""

    def test_headers_include_auth(self):
        """Test headers include authorization."""
        client = APIClient(base_url="http://example.com", api_key="test-key")
        headers = client._headers()
        assert "Authorization" in headers
        assert headers["Authorization"] == "Bearer test-key"

    def test_headers_include_content_type(self):
        """Test headers include content type."""
        client = APIClient(base_url="http://example.com", api_key="test-key")
        headers = client._headers()
        assert headers["Content-Type"] == "application/json"


class TestAPIClientPushReading:
    """Tests for pushing sensor readings."""

    def test_push_reading_disabled_returns_false(self, sample_reading):
        """Test push returns False when disabled."""
        with patch.dict("os.environ", {}, clear=True):
            client = APIClient()
            result = client.push_reading(sample_reading)
            assert result is False

    def test_push_reading_success(self, sample_reading):
        """Test successful reading push."""
        with patch("api_client.httpx.post") as mock_post:
            mock_post.return_value = MagicMock(status_code=200)

            client = APIClient(base_url="http://example.com", api_key="key")
            result = client.push_reading(sample_reading)

            assert result is True
            mock_post.assert_called_once()

    def test_push_reading_correct_endpoint(self, sample_reading):
        """Test reading pushed to correct endpoint."""
        with patch("api_client.httpx.post") as mock_post:
            mock_post.return_value = MagicMock(status_code=200)

            client = APIClient(base_url="http://example.com", api_key="key")
            client.push_reading(sample_reading)

            call_args = mock_post.call_args
            assert "/readings" in call_args[0][0]

    def test_push_reading_handles_error(self, sample_reading):
        """Test push handles network error gracefully."""
        with patch("api_client.httpx.post") as mock_post:
            mock_post.side_effect = Exception("Network error")

            client = APIClient(base_url="http://example.com", api_key="key")
            result = client.push_reading(sample_reading)

            assert result is False


class TestAPIClientPushAnalysis:
    """Tests for pushing AI analysis."""

    def test_push_analysis_disabled_returns_false(self, sample_reading):
        """Test push returns False when disabled."""
        with patch.dict("os.environ", {}, clear=True):
            client = APIClient()
            result = client.push_analysis(sample_reading, "test recommendation")
            assert result is False

    def test_push_analysis_success(self, sample_reading):
        """Test successful analysis push."""
        with patch("api_client.httpx.post") as mock_post:
            mock_post.return_value = MagicMock(status_code=200)

            client = APIClient(base_url="http://example.com", api_key="key")
            result = client.push_analysis(sample_reading, "test recommendation")

            assert result is True

    def test_push_analysis_correct_endpoint(self, sample_reading):
        """Test analysis pushed to correct endpoint."""
        with patch("api_client.httpx.post") as mock_post:
            mock_post.return_value = MagicMock(status_code=200)

            client = APIClient(base_url="http://example.com", api_key="key")
            client.push_analysis(sample_reading, "recommendation")

            call_args = mock_post.call_args
            assert "/analysis" in call_args[0][0]


class TestAPIClientPushAlert:
    """Tests for pushing alerts."""

    def test_push_alert_disabled_returns_false(self):
        """Test push returns False when disabled."""
        with patch.dict("os.environ", {}, clear=True):
            client = APIClient()
            result = client.push_alert("temp_high", "Temperature alert")
            assert result is False

    def test_push_alert_success(self):
        """Test successful alert push."""
        with patch("api_client.httpx.post") as mock_post:
            mock_post.return_value = MagicMock(status_code=200)

            client = APIClient(base_url="http://example.com", api_key="key")
            result = client.push_alert("temp_high", "Temperature is high")

            assert result is True

    def test_push_alert_with_reading(self, sample_reading):
        """Test alert push with reading included."""
        with patch("api_client.httpx.post") as mock_post:
            mock_post.return_value = MagicMock(status_code=200)

            client = APIClient(base_url="http://example.com", api_key="key")
            result = client.push_alert("temp_high", "Alert", reading=sample_reading)

            assert result is True
            call_kwargs = mock_post.call_args[1]
            assert "reading" in call_kwargs["json"]

    def test_push_alert_correct_endpoint(self):
        """Test alert pushed to correct endpoint."""
        with patch("api_client.httpx.post") as mock_post:
            mock_post.return_value = MagicMock(status_code=200)

            client = APIClient(base_url="http://example.com", api_key="key")
            client.push_alert("test_type", "test message")

            call_args = mock_post.call_args
            assert "/alerts" in call_args[0][0]
