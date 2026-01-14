# AIVOCADO

Monitor your avocado plant growth using Raspberry Pi sensors and Claude AI.

## What it does

Reads sensor data (temperature, humidity, CO2, light) and displays it in a terminal dashboard. Optionally sends readings to Claude for care recommendations.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# add your ANTHROPIC_API_KEY to .env
```

## Usage

```bash
# test with mock sensor data
python main.py

# use real sensors on raspberry pi
python main.py --real

# custom intervals
python main.py --interval 5 --ai-interval 30
```

## Hardware

For real sensor readings you need:

- DHT22 (temperature/humidity)
- MH-Z19 (CO2)
- BH1750 (light)

See requirements.txt for the raspberry pi libraries.

## Optimal ranges

- Temperature: 18-26C
- Humidity: 50-70%
- CO2: 400-800 ppm
- Light: 2000-10000 lux
