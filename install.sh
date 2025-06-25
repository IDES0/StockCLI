#!/bin/bash

# Stock CLI Installation Script

echo "🚀 Installing Stock CLI..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed. Please install pip3 first."
    exit 1
fi

# Install dependencies from requirements.txt
echo "📦 Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
else
    echo "⚠️  requirements.txt not found, installing basic dependencies..."
    pip3 install yfinance plotext
fi

# Install the package in development mode
echo "📦 Installing Stock CLI in development mode..."
pip3 install -e .

# Make the script executable
chmod +x stockCLI.py

# Create a symlink to make it globally accessible (alternative method)
if [ ! -f /usr/local/bin/stk ]; then
    echo "🔗 Creating global symlink..."
    # Create /usr/local/bin if it doesn't exist
    sudo mkdir -p /usr/local/bin
    sudo ln -sf "$(pwd)/stockCLI.py" /usr/local/bin/stk
    sudo chmod +x /usr/local/bin/stk
fi

echo "✅ Installation complete!"
echo ""
echo "You can now use the Stock CLI with:"
echo "  stk NVDA          # Get basic info for NVIDIA"
echo "  stk AAPL -d       # Get detailed info for Apple"
echo "  stk TSLA --json   # Get JSON output for Tesla"
echo "  stk NVDA --chart  # Show price chart for NVIDIA"
echo "  stk AAPL --chart --period 3mo --type candlestick  # 3-month candlestick chart"
echo "  stk --help        # Show all options"
echo ""
echo "Chart Features:"
echo "  --chart           # Display historical price chart"
echo "  --period 1mo      # Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)"
echo "  --type line       # Chart type (line, candlestick, volume)"
echo ""
echo "If the 'stk' command doesn't work immediately, try:"
echo "  1. Restart your terminal"
echo "  2. Or run: source ~/.bashrc (or ~/.zshrc)"
echo "" 