# StockCLI

A simple terminal application to check real-time stock prices, view historical charts, and display financial metrics for stocks.

## Features
- Real-time stock price lookup
- Colorized terminal output
- Historical price and volume charts (ASCII)
- Detailed financial and analyst metrics
- JSON output for scripting
- Custom field selection and full metrics display

## Quick Install
```bash
curl -sSL https://raw.githubusercontent.com/IDES0/StockCLI/main/install.sh | bash
```

This gives users the fastest way to get started with just one command!

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

### Installation Modes

The install script offers two installation modes:

#### 🚀 Development Mode (Default)
- **Live updates**: Changes to source code are immediately available
- **No reinstallation needed**: Just `git pull` to get updates
- **Symlink setup**: Direct access to source files
- **Perfect for**: Users who want to stay up-to-date with latest features

#### 📦 Production Mode
- **Standard installation**: Traditional package installation
- **Requires reinstall**: Run `git pull && pip3 install .` for updates
- **Independent**: Works even if source directory is moved/deleted
- **Perfect for**: Users who prefer traditional package management

The script will prompt you to choose between these modes during installation.

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

## Example Output

### Basic Stock Info
```sh
$ stk NVDA

============================================================
NVIDIA Corporation (NVDA)
============================================================

Current Price: $154.31
Change: ▲ $6.41 (+4.33%)
Previous Close: $147.90

Trading Info:
  High: $154.45
  Low: $149.28
  Volume: 267,389,333

Last Updated: 2025-06-25 16:02:18
============================================================
```

### Price Chart
```sh
$ stk NVDA --chart
```

```
                                      NVDA Stock Price - 1mo                                  
     ┌───────────────────────────────────────────────────────────────────────────────────────┐
154.3┤                                                                                      ▞│
     │                                                                                     ▗▘│
     │                                                                                     ▐ │
     │                                                                                     ▌ │
151.1┤                                                                                    ▗▘ │
     │                                                                                    ▞  │
     │                                                                                    ▌  │
     │                                                                                   ▐   │
147.8┤                                                                                   ▞   │
     │                                                                                  ▐    │
     │                                                                                 ▗▘    │
     │                                               ▗                 ▞▄▖             ▞     │
144.6┤                                              ▗▀▖         ▗▞▄▖ ▗▀  ▝▀▄▖         ▐      │
     │                                         ▄▚  ▗▘ ▝▖      ▄▀▘  ▝▀▘      ▝▀▀▀▀▀▀▀▀▀▘      │
     │                                       ▄▀  ▀▄▘   ▚   ▗▞▀                               │
     │                        ▖        ▄▄▄▀▀▀           ▚▄▀▘                                 │
141.3┤                     ▄▞▀▝▖   ▗▀▀▀                                                      │
     │                    ▞    ▝▖ ▞▘                                                         │
     │                   ▗▘     ▝▀                                                           │
     │     ▗▌            ▞                                                                   │
138.1┤     ▌▐           ▐                                                                    │
     │    ▐  ▚          ▌                                                                    │
     │    ▌  ▝▖     ▗▄▞▀                                                                     │
     │▖  ▐    ▚  ▄▄▀▘                                                                        │
134.8┤▝▀▄▌     ▀▀                                                                            │
     └┬─────────────────────┬────────────────────┬─────────────────────┬────────────────────┬┘
   26/05/2025          03/06/2025           10/06/2025            17/06/2025       24/06/2025 
Price ($)                                      Date                                           
```

## Requirements
- Python 3.7+
- [yfinance](https://pypi.org/project/yfinance/)
- [plotext](https://pypi.org/project/plotext/)

## License
MIT 