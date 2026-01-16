"""Tests for AI advisor module."""

import pytest
from unittest.mock import Mock, patch, MagicMock

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from ai_advisor import AIAdvisor, SYSTEM_PROMPT


class TestAIAdvisorInit:
    """Tests for AIAdvisor initialization."""

    def test_init_without_api_key(self):
        """Test initialization without API key."""
        with patch.dict("os.environ", {}, clear=True):
            advisor = AIAdvisor(api_key=None)
            assert advisor._client is None

    def test_init_with_api_key(self):
        """Test initialization with API key."""
        with patch("ai_advisor.Anthropic") as mock_anthropic:
            advisor = AIAdvisor(api_key="test-key")
            mock_anthropic.assert_called_once_with(api_key="test-key")

    def test_init_from_env(self):
        """Test initialization from environment variable."""
        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "env-key"}):
            with patch("ai_advisor.Anthropic") as mock_anthropic:
                advisor = AIAdvisor()
                mock_anthropic.assert_called_once_with(api_key="env-key")


class TestAIAdvisorBuildPrompt:
    """Tests for prompt building."""

    def test_prompt_includes_temperature(self, sample_reading):
        """Test that prompt includes temperature."""
        advisor = AIAdvisor(api_key=None)
        prompt = advisor._build_prompt(sample_reading)
        assert "22.0" in prompt
        assert "Temperature" in prompt

    def test_prompt_includes_humidity(self, sample_reading):
        """Test that prompt includes humidity."""
        advisor = AIAdvisor(api_key=None)
        prompt = advisor._build_prompt(sample_reading)
        assert "60.0" in prompt
        assert "Humidity" in prompt

    def test_prompt_includes_co2(self, sample_reading):
        """Test that prompt includes CO2."""
        advisor = AIAdvisor(api_key=None)
        prompt = advisor._build_prompt(sample_reading)
        assert "500" in prompt
        assert "CO2" in prompt

    def test_prompt_includes_light(self, sample_reading):
        """Test that prompt includes light."""
        advisor = AIAdvisor(api_key=None)
        prompt = advisor._build_prompt(sample_reading)
        assert "5000" in prompt
        assert "Light" in prompt


class TestAIAdvisorFallback:
    """Tests for fallback recommendations when API unavailable."""

    def test_fallback_optimal_conditions(self, sample_reading):
        """Test fallback message when all conditions optimal."""
        advisor = AIAdvisor(api_key=None)
        result = advisor._get_fallback_recommendation(sample_reading)
        assert "optimal" in result.lower()

    def test_fallback_low_temperature(self, low_temp_reading):
        """Test fallback detects low temperature."""
        advisor = AIAdvisor(api_key=None)
        result = advisor._get_fallback_recommendation(low_temp_reading)
        assert "low" in result.lower() or "warm" in result.lower()

    def test_fallback_high_temperature(self, high_temp_reading):
        """Test fallback detects high temperature."""
        advisor = AIAdvisor(api_key=None)
        result = advisor._get_fallback_recommendation(high_temp_reading)
        assert "high" in result.lower() or "ventilation" in result.lower()

    def test_fallback_multiple_issues(self, all_out_of_range_reading):
        """Test fallback handles multiple issues."""
        advisor = AIAdvisor(api_key=None)
        result = advisor._get_fallback_recommendation(all_out_of_range_reading)
        # Should mention at least one issue
        assert len(result) > 10

    def test_fallback_limits_to_two_issues(self, all_out_of_range_reading):
        """Test fallback only shows top 2 issues."""
        advisor = AIAdvisor(api_key=None)
        result = advisor._get_fallback_recommendation(all_out_of_range_reading)
        # Count pipe separators (max 1 for 2 issues)
        assert result.count("|") <= 1


class TestAIAdvisorGetRecommendation:
    """Tests for getting recommendations."""

    def test_uses_fallback_when_no_client(self, sample_reading):
        """Test uses fallback when no API client."""
        advisor = AIAdvisor(api_key=None)
        result = advisor.get_recommendation(sample_reading)
        assert "optimal" in result.lower()

    def test_calls_api_when_available(self, sample_reading):
        """Test calls API when client available."""
        with patch("ai_advisor.Anthropic") as mock_anthropic:
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.content = [MagicMock(text="AI recommendation")]
            mock_client.messages.create.return_value = mock_response
            mock_anthropic.return_value = mock_client

            advisor = AIAdvisor(api_key="test-key")
            result = advisor.get_recommendation(sample_reading)

            assert result == "AI recommendation"
            mock_client.messages.create.assert_called_once()

    def test_falls_back_on_api_error(self, sample_reading):
        """Test falls back to rule-based on API error."""
        with patch("ai_advisor.Anthropic") as mock_anthropic:
            mock_client = MagicMock()
            mock_client.messages.create.side_effect = Exception("API Error")
            mock_anthropic.return_value = mock_client

            advisor = AIAdvisor(api_key="test-key")
            result = advisor.get_recommendation(sample_reading)

            # Should return fallback, not raise exception
            assert "optimal" in result.lower()


class TestSystemPrompt:
    """Tests for system prompt configuration."""

    def test_system_prompt_mentions_avocado(self):
        """Test system prompt is about avocados."""
        assert "avocado" in SYSTEM_PROMPT.lower()

    def test_system_prompt_includes_ranges(self):
        """Test system prompt includes optimal ranges."""
        assert "18" in SYSTEM_PROMPT  # Temperature low
        assert "26" in SYSTEM_PROMPT  # Temperature high

    def test_system_prompt_requests_brevity(self):
        """Test system prompt asks for brief responses."""
        assert "brief" in SYSTEM_PROMPT.lower() or "concise" in SYSTEM_PROMPT.lower()
