#!/usr/bin/env python3
"""
Avocado Plant Monitoring System

Monitors temperature, humidity, CO2, and light levels for optimal avocado growth.
Uses Claude AI to provide recommendations for adjustments.

Usage:
    python main.py              # Run with mock sensors (testing)
    python main.py --real       # Run with real Raspberry Pi sensors

Environment:
    ANTHROPIC_API_KEY          # Required for AI recommendations
    AIVOCADO_API_URL           # External API base URL (optional)
    AIVOCADO_API_KEY           # External API key (optional)
"""

import argparse
import time
import sys

from dotenv import load_dotenv
load_dotenv()

from sensors import get_sensor_interface
from display import display_reading
from ai_advisor import AIAdvisor
from api_client import APIClient


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Avocado Plant Monitoring System"
    )
    parser.add_argument(
        "--real",
        action="store_true",
        help="Use real Raspberry Pi sensors instead of mock data"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=10,
        help="Seconds between readings (default: 10)"
    )
    parser.add_argument(
        "--ai-interval",
        type=int,
        default=60,
        help="Seconds between AI recommendations (default: 60)"
    )
    return parser.parse_args()


def main():
    """Main monitoring loop."""
    args = parse_args()

    # Initialize components
    sensors = get_sensor_interface(use_mock=not args.real)
    advisor = AIAdvisor()
    api = APIClient()

    print("Starting Avocado Plant Monitoring System...")
    print(f"Mode: {'Real sensors' if args.real else 'Mock sensors (testing)'}")
    print(f"Reading interval: {args.interval}s")
    print(f"AI recommendation interval: {args.ai_interval}s")
    print()

    last_ai_update = 0
    current_recommendation = "Initializing... gathering first readings."

    try:
        while True:
            # Read sensors
            reading = sensors.read()

            # Push reading to external API
            api.push_reading(reading)

            # Get AI recommendation if interval has passed
            current_time = time.time()
            if current_time - last_ai_update >= args.ai_interval:
                current_recommendation = advisor.get_recommendation(reading)
                api.push_analysis(reading, current_recommendation)
                last_ai_update = current_time

            # Display dashboard
            display_reading(reading, current_recommendation)

            # Wait for next reading
            time.sleep(args.interval)

    except KeyboardInterrupt:
        print("\n\nMonitoring stopped. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
