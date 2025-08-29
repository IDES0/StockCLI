#!/bin/zsh

# Stock CLI Installation Script for Zsh

echo "🚀 Installing Stock CLI for Zsh..."

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

# Configuration file for Zsh
ZSH_CONFIG_FILE="$HOME/.zshrc"

# Check if a directory is in PATH
is_in_path() {
    local dir="$1"
    echo "$PATH" | tr ':' '\n' | grep -q "^$dir$"
}

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

    # Determine the best location for the symlink
    local_bin="$HOME/.local/bin"
    usr_local_bin="/usr/local/bin"

    # Check if ~/.local/bin exists and is in PATH
    if [ -d "$local_bin" ] && is_in_path "$local_bin"; then
        symlink_dir="$local_bin"
        echo "🔗 Using ~/.local/bin for symlink (already in PATH)"
    elif [ -w "$usr_local_bin" ] && is_in_path "$usr_local_bin"; then
        symlink_dir="$usr_local_bin"
        echo "🔗 Using /usr/local/bin for symlink (already in PATH)"
    else
        # Create ~/.local/bin and add to PATH
        symlink_dir="$local_bin"
        mkdir -p "$local_bin"
        echo "🔗 Creating ~/.local/bin and adding to PATH"

        # Add to PATH in .zshrc if not already there
        if ! is_in_path "$local_bin"; then
            echo "" >> "$ZSH_CONFIG_FILE"
            echo "# Stock CLI PATH addition" >> "$ZSH_CONFIG_FILE"
            echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$ZSH_CONFIG_FILE"
            echo "✅ Added ~/.local/bin to PATH in $ZSH_CONFIG_FILE"
            echo "🔄 Please restart your terminal or run: source $ZSH_CONFIG_FILE"
        fi
    fi

    # Create the symlink
    symlink_path="$symlink_dir/stk"
    if [ -L "$symlink_path" ]; then
        rm "$symlink_path"
    fi

    ln -sf "$(pwd)/stockCLI.py" "$symlink_path"
    chmod +x "$symlink_path"

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

    # Check if the command is immediately available
    if command -v stk &> /dev/null; then
        echo "✅ The 'stk' command is now available!"
    else
        echo "⚠️  The 'stk' command might not be immediately available."
        echo "   Try one of these solutions:"
        echo "   1. Restart your terminal"
        echo "   2. Run: source $ZSH_CONFIG_FILE"
        echo "   3. Or run the script directly: python3 stockCLI.py"
    fi
fi