# StockCLI

A simple terminal application to check real-time stock prices, view historical charts, and display financial metrics for stocks.

## Features
- Real-time stock price lookup
- Colorized terminal output
- Historical price and volume charts (ASCII)
- Detailed financial and analyst metrics
- JSON output for scripting
- Custom field selection and full metrics display

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/IDES0/StockCLI.git
   cd StockCLI
   ```
2. Run the install script:
   ```sh
   ./install.sh
   ```

## Usage

```sh
stk SYMBOL [options]
```

### Examples
```sh
stk NVDA                    # Get basic info for NVIDIA
stk AAPL -d                 # Get detailed info for Apple
stk TSLA --json             # Get JSON output for Tesla
stk NVDA --chart            # Show price chart for NVIDIA
stk AAPL --chart --period 3mo --type candlestick  # 3-month candlestick chart
stk NVDA --all              # Show all available metrics organized by category
stk AAPL --fields marketCap trailingPE dividendYield  # Show specific fields
stk --list-fields           # List all available fields
```

### Main Options
- `-d, --detailed`         Show detailed info (market cap, P/E, etc.)
- `--json`                 Output as JSON
- `--no-colors`            Disable colored output
- `--chart`                Show historical price/volume chart
- `--period`               Chart period (1d, 5d, 1mo, 3mo, etc.)
- `--type`                 Chart type (line, candlestick, volume)
- `--all`                  Show all available metrics
- `--fields FIELD [FIELD ...]`  Show specific fields
- `--list-fields`          List all available fields

## Requirements
- Python 3.7+
- [yfinance](https://pypi.org/project/yfinance/)
- [plotext](https://pypi.org/project/plotext/)

## License
MIT 