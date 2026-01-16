# AIVOCADO

[![CI](https://github.com/jnaranja/aivocado/actions/workflows/ci.yml/badge.svg)](https://github.com/jnaranja/aivocado/actions/workflows/ci.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Monitor your avocado plant growth using Raspberry Pi sensors and Claude AI.

## Features

- **Real-time Monitoring**: Track temperature, humidity, CO2, and light levels
- **AI-Powered Recommendations**: Get plant care advice from Claude AI
- **Terminal Dashboard**: Visual display with status indicators and progress bars
- **Mock Mode**: Test without hardware using simulated sensor data
- **External API Integration**: Push readings to your own backend service
- **Graceful Degradation**: Works offline with rule-based recommendations

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/jnaranja/aivocado.git
cd aivocado

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .

# Configure environment
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
```

### Usage

```bash
# Test with mock sensor data
python main.py

# Use real sensors on Raspberry Pi
python main.py --real

# Custom intervals
python main.py --interval 5 --ai-interval 30
```

## Hardware Requirements

For real sensor readings, you need:

| Sensor | Measurement | Protocol |
|--------|------------|----------|
| DHT22 | Temperature & Humidity | GPIO |
| MH-Z19 | CO2 | UART |
| BH1750 | Light | I2C |

Install Raspberry Pi dependencies:

```bash
pip install -e ".[raspi]"
```

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Claude API key for AI recommendations |
| `AIVOCADO_API_URL` | No | External API base URL |
| `AIVOCADO_API_KEY` | No | External API authentication key |

### Command Line Options

| Option | Default | Description |
|--------|---------|-------------|
| `--real` | False | Use real Raspberry Pi sensors |
| `--interval` | 10 | Seconds between readings |
| `--ai-interval` | 60 | Seconds between AI recommendations |

## Optimal Growing Conditions

AIVOCADO monitors against these optimal ranges for avocado plants:

| Parameter | Optimal Range | Notes |
|-----------|--------------|-------|
| Temperature | 18-26°C | Avocados prefer mild temperatures |
| Humidity | 50-70% | Moderate humidity |
| CO2 | 400-800 ppm | Normal to slightly elevated |
| Light | 2,000-10,000 lux | Bright indirect (understory plant) |

## Development

### Setup

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Format code
black .

# Lint
ruff check .

# Type check
mypy .
```

### Project Structure

```
aivocado/
├── main.py           # Entry point and main loop
├── sensors.py        # Sensor interfaces (mock and real)
├── display.py        # Terminal UI dashboard
├── ai_advisor.py     # Claude AI integration
├── api_client.py     # External API client
├── tests/            # Test suite
└── .github/workflows # CI/CD configuration
```

## API Integration

AIVOCADO can push data to an external API. Configure `AIVOCADO_API_URL` and `AIVOCADO_API_KEY` environment variables.

### Endpoints

- `POST /readings` - Push sensor readings
- `POST /analysis` - Push AI recommendations
- `POST /alerts` - Push out-of-range alerts

See [api_client.py](api_client.py) for request/response formats.

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Anthropic](https://www.anthropic.com/) for Claude AI
- [Adafruit](https://www.adafruit.com/) for sensor libraries
