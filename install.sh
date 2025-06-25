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

# Ask user for installation mode
echo ""
echo "📋 Installation Mode Selection:"
echo "1) Development Mode (default) - Live updates, symlink to source"
echo "2) Production Mode - Standard installation, requires reinstall for updates"
echo ""
read -p "Choose installation mode [1/2] (default: 1): " install_mode
install_mode=${install_mode:-1}

# Make the script executable
chmod +x stockCLI.py

if [ "$install_mode" = "2" ]; then
    # Production mode installation
    echo "📦 Installing Stock CLI in production mode..."
    pip3 install .
    
    echo "✅ Production installation complete!"
    echo ""
    echo "You can now use the Stock CLI with:"
    echo "  stk NVDA          # Get basic info for NVIDIA"
    echo "  stk AAPL -d       # Get detailed info for Apple"
    echo "  stk TSLA --json   # Get JSON output for Tesla"
    echo "  stk NVDA --chart  # Show price chart for NVIDIA"
    echo "  stk --help        # Show all options"
    echo ""
    echo "Note: To update the CLI, you'll need to reinstall:"
    echo "  git pull && pip3 install ."
    
else
    # Development mode installation (default)
    echo "📦 Installing Stock CLI in development mode..."
    pip3 install -e .
    
    # Create a symlink to make it globally accessible
    if [ ! -f /usr/local/bin/stk ]; then
        echo "🔗 Creating global symlink..."
        # Create /usr/local/bin if it doesn't exist
        sudo mkdir -p /usr/local/bin
        sudo ln -sf "$(pwd)/stockCLI.py" /usr/local/bin/stk
        sudo chmod +x /usr/local/bin/stk
    fi
    
    echo "✅ Development installation complete!"
    echo ""
    echo "You can now use the Stock CLI with:"
    echo "  stk NVDA          # Get basic info for NVIDIA"
    echo "  stk AAPL -d       # Get detailed info for Apple"
    echo "  stk TSLA --json   # Get JSON output for Tesla"
    echo "  stk NVDA --chart  # Show price chart for NVIDIA"
    echo "  stk AAPL --chart --period 3mo --type candlestick  # 3-month candlestick chart"
    echo "  stk --help        # Show all options"
    echo ""
    echo "🎯 Development Mode Benefits:"
    echo "  • Live updates: Changes to source code are immediately available"
    echo "  • No reinstallation needed after updates"
    echo "  • Perfect for staying up-to-date with latest features"
    echo ""
    echo "Chart Features:"
    echo "  --chart           # Display historical price chart"
    echo "  --period 1mo      # Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)"
    echo "  --type line       # Chart type (line, candlestick, volume)"
    echo ""
    echo "If the 'stk' command doesn't work immediately, try:"
    echo "  1. Restart your terminal"
    echo "  2. Or run: source ~/.bashrc (or ~/.zshrc)"
fi 