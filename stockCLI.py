#!/usr/bin/env python3
"""
Stock CLI - A simple terminal application to check stock prices
Usage: stk <symbol> [options]
"""

import sys
import argparse
import yfinance as yf
from datetime import datetime
import locale
from typing import Optional, Dict, Any
import json

# Try to import plotext for charting functionality
try:
    import plotext as plt
    PLOTEXT_AVAILABLE = True
except ImportError:
    PLOTEXT_AVAILABLE = False

# Set locale for proper number formatting
try:
    locale.setlocale(locale.LC_ALL, '')
except locale.Error:
    pass

class StockCLI:
    # Constants at class level
    DEFAULT_PERIOD = "2d"
    DEFAULT_CHART_PERIOD = "1mo"
    DEFAULT_CHART_TYPE = "line"
    
    # Number formatting constants
    TRILLION = 1e12
    BILLION = 1e9
    MILLION = 1e6
    THOUSAND = 1e3

    def __init__(self):
        self.colors = {
            'green': '\033[92m',
            'red': '\033[91m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'bold': '\033[1m',
            'reset': '\033[0m'
        }
        
        # Define available fields organized by category
        self.field_categories = {
            "Basic Info": {
                "longName": "Company Name",
                "shortName": "Short Name", 
                "symbol": "Symbol",
                "exchange": "Exchange",
                "quoteType": "Quote Type",
                "market": "Market",
                "marketState": "Market State",
                "currency": "Currency",
                "timeZoneFullName": "Time Zone"
            },
            "Price & Volume": {
                "currentPrice": "Current Price",
                "previousClose": "Previous Close",
                "open": "Open",
                "dayLow": "Day Low",
                "dayHigh": "Day High",
                "volume": "Volume",
                "averageVolume": "Avg Volume",
                "averageVolume10days": "Avg Volume (10d)",
                "bid": "Bid",
                "ask": "Ask",
                "bidSize": "Bid Size",
                "askSize": "Ask Size"
            },
            "Market Metrics": {
                "marketCap": "Market Cap",
                "enterpriseValue": "Enterprise Value",
                "floatShares": "Float Shares",
                "sharesOutstanding": "Shares Outstanding",
                "sharesShort": "Shares Short",
                "sharesShortPreviousMonthDate": "Short Month Date",
                "sharesShortPriorMonth": "Short Prior Month",
                "shortRatio": "Short Ratio",
                "shortPercentOfFloat": "Short % of Float"
            },
            "Valuation Ratios": {
                "trailingPE": "P/E Ratio (TTM)",
                "forwardPE": "Forward P/E",
                "pegRatio": "PEG Ratio",
                "priceToBook": "Price/Book",
                "enterpriseToRevenue": "Enterprise/Revenue",
                "enterpriseToEbitda": "Enterprise/EBITDA",
                "bookValue": "Book Value",
                "priceToSalesTrailing12Months": "Price/Sales"
            },
            "Financial Metrics": {
                "revenue": "Revenue",
                "revenuePerShare": "Revenue/Share",
                "revenueGrowth": "Revenue Growth",
                "grossProfits": "Gross Profits",
                "freeCashflow": "Free Cash Flow",
                "operatingCashflow": "Operating Cash Flow",
                "earningsGrowth": "Earnings Growth",
                "earningsQuarterlyGrowth": "Quarterly Earnings Growth",
                "returnOnAssets": "ROA",
                "returnOnEquity": "ROE",
                "returnOnCapital": "ROIC",
                "profitMargins": "Profit Margin",
                "operatingMargins": "Operating Margin",
                "ebitdaMargins": "EBITDA Margin",
                "grossMargins": "Gross Margin"
            },
            "Dividend Info": {
                "dividendRate": "Dividend Rate",
                "dividendYield": "Dividend Yield",
                "payoutRatio": "Payout Ratio",
                "fiveYearAvgDividendYield": "5Y Avg Dividend Yield",
                "exDividendDate": "Ex-Dividend Date",
                "lastDividendDate": "Last Dividend Date",
                "lastDividendValue": "Last Dividend Value"
            },
            "Analyst Info": {
                "targetMeanPrice": "Target Mean Price",
                "targetMedianPrice": "Target Median Price",
                "targetHighPrice": "Target High Price",
                "targetLowPrice": "Target Low Price",
                "numberOfAnalystOpinions": "Analyst Opinions",
                "recommendationMean": "Recommendation",
                "recommendationKey": "Recommendation Key"
            },
            "Technical Indicators": {
                "fiftyDayAverage": "50-Day Average",
                "twoHundredDayAverage": "200-Day Average",
                "fiftyTwoWeekLow": "52-Week Low",
                "fiftyTwoWeekHigh": "52-Week High",
                "fiftyTwoWeekChange": "52-Week Change",
                "fiftyTwoWeekChangePercent": "52-Week Change %"
            },
            "Company Info": {
                "industry": "Industry",
                "sector": "Sector",
                "country": "Country",
                "state": "State",
                "city": "City",
                "zip": "ZIP",
                "phone": "Phone",
                "website": "Website",
                "businessSummary": "Business Summary",
                "fullTimeEmployees": "Full-Time Employees"
            }
        }
        
        # Create a flat mapping of all available fields
        self.all_fields = {}
        for category, fields in self.field_categories.items():
            self.all_fields.update(fields)
    
    def colorize(self, text: str, color: str) -> str:
        """Add color to text if colors are supported"""
        if color in self.colors:
            return f"{self.colors[color]}{text}{self.colors['reset']}"
        return text
    
    def format_currency(self, value: float) -> str:
        """Format currency values with proper locale"""
        try:
            return locale.currency(value, grouping=True)
        except:
            return f"${value:,.2f}"
    
    def format_percentage(self, value: float) -> str:
        """Format percentage values"""
        return f"{value:+.2f}%"
    
    def format_large_number(self, value: float) -> str:
        """Format large numbers with appropriate suffixes"""
        if value >= self.TRILLION:
            return f"${value/self.TRILLION:.2f}T"
        elif value >= self.BILLION:
            return f"${value/self.BILLION:.2f}B"
        elif value >= self.MILLION:
            return f"${value/self.MILLION:.2f}M"
        elif value >= self.THOUSAND:
            return f"${value/self.THOUSAND:.2f}K"
        else:
            return f"${value:,.2f}"
    
    def format_field_value(self, field_key: str, value) -> str:
        """Format field values based on their type"""
        if value is None:
            return "N/A"
        
        # Handle different field types
        if field_key in ['dividendYield', 'payoutRatio', 'profitMargins', 'operatingMargins', 
                        'ebitdaMargins', 'grossMargins', 'returnOnAssets', 'returnOnEquity', 
                        'returnOnCapital', 'revenueGrowth', 'earningsGrowth', 'earningsQuarterlyGrowth',
                        'fiftyTwoWeekChangePercent', 'shortPercentOfFloat']:
            return f"{value*100:.2f}%" if isinstance(value, (int, float)) else str(value)
        
        elif field_key in ['marketCap', 'enterpriseValue', 'revenue', 'grossProfits', 
                          'freeCashflow', 'operatingCashflow', 'targetMeanPrice', 
                          'targetMedianPrice', 'targetHighPrice', 'targetLowPrice',
                          'fiftyDayAverage', 'twoHundredDayAverage', 'fiftyTwoWeekLow',
                          'fiftyTwoWeekHigh', 'fiftyTwoWeekChange', 'bookValue',
                          'dividendRate', 'lastDividendValue']:
            return self.format_large_number(value) if isinstance(value, (int, float)) else str(value)
        
        elif field_key in ['trailingPE', 'forwardPE', 'pegRatio', 'priceToBook', 
                          'enterpriseToRevenue', 'enterpriseToEbitda', 'priceToSalesTrailing12Months',
                          'shortRatio', 'recommendationMean']:
            return f"{value:.2f}" if isinstance(value, (int, float)) else str(value)
        
        elif field_key in ['volume', 'averageVolume', 'averageVolume10days', 'bidSize', 'askSize',
                          'floatShares', 'sharesOutstanding', 'sharesShort', 'sharesShortPriorMonth',
                          'numberOfAnalystOpinions', 'fullTimeEmployees']:
            return f"{value:,}" if isinstance(value, (int, float)) else str(value)
        
        else:
            return str(value)
    
    def get_stock_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Fetch stock data from Yahoo Finance"""
        try:
            # Convert to uppercase and remove any whitespace
            symbol = symbol.upper().strip()
            
            # Create ticker object
            ticker = yf.Ticker(symbol)
            
            # Get current info
            info = ticker.info
            
            # Get current price data
            hist = ticker.history(period="2d")
            
            if hist.empty:
                return None
            
            current_price = hist['Close'].iloc[-1]
            previous_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            change = current_price - previous_close
            change_percent = (change / previous_close) * 100 if previous_close != 0 else 0
            
            # Get additional data
            volume = hist['Volume'].iloc[-1] if 'Volume' in hist.columns else 0
            high = hist['High'].iloc[-1] if 'High' in hist.columns else current_price
            low = hist['Low'].iloc[-1] if 'Low' in hist.columns else current_price
            
            # Base data structure
            data = {
                'symbol': symbol,
                'name': info.get('longName', info.get('shortName', symbol)),
                'current_price': current_price,
                'previous_close': previous_close,
                'change': change,
                'change_percent': change_percent,
                'volume': volume,
                'high': high,
                'low': low,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Add all available fields from yfinance
            for field_key in self.all_fields.keys():
                if field_key in info and info[field_key] is not None:
                    data[field_key] = info[field_key]
            
            return data
            
        except Exception as e:
            print(f"Error fetching data for {symbol}: {str(e)}", file=sys.stderr)
            return None
    
    def get_historical_data(self, symbol: str, period: str = "1mo") -> Optional[Dict[str, Any]]:
        """Fetch historical stock data for charting"""
        try:
            # Convert to uppercase and remove any whitespace
            symbol = symbol.upper().strip()
            
            # Create ticker object
            ticker = yf.Ticker(symbol)
            
            # Get historical data
            hist = ticker.history(period=period)
            
            if hist.empty:
                return None
            
            # Convert dates to strings for display
            dates = [d.strftime('%d/%m/%Y') for d in hist.index]
            
            return {
                'symbol': symbol,
                'dates': dates,
                'prices': hist['Close'].tolist(),
                'volumes': hist['Volume'].tolist() if 'Volume' in hist.columns else [],
                'highs': hist['High'].tolist() if 'High' in hist.columns else [],
                'lows': hist['Low'].tolist() if 'Low' in hist.columns else [],
                'opens': hist['Open'].tolist() if 'Open' in hist.columns else []
            }
            
        except Exception as e:
            print(f"Error fetching historical data for {symbol}: {str(e)}", file=sys.stderr)
            return None
    
    def display_chart(self, symbol: str, period: str = "1mo", chart_type: str = "line"):
        """Display a chart of historical stock data"""
        if not PLOTEXT_AVAILABLE:
            print("Charting requires plotext library. Install with: pip install plotext")
            return
        
        # Get historical data
        data = self.get_historical_data(symbol, period)
        if not data:
            print(f"Could not fetch historical data for {symbol}")
            return
        
        # Clear previous plots
        plt.clear_figure()
        plt.theme('dark')
        
        if chart_type == "line":
            # Simple line chart
            plt.plot(data['dates'], data['prices'], color="green")
            plt.title(f"{symbol} Stock Price - {period}")
            plt.xlabel("Date")
            plt.ylabel("Price ($)")
            plt.show()
                
        elif chart_type == "volume":
            # Volume chart
            if len(data['volumes']) > 0:
                plt.bar(data['dates'], data['volumes'], color="blue")
                plt.title(f"{symbol} Trading Volume - {period}")
                plt.xlabel("Date")
                plt.ylabel("Volume")
                plt.show()
            else:
                print("Volume data not available")
    
    def display_stock_info(self, data: Dict[str, Any], detailed: bool = False, 
                          specific_fields: Optional[list] = None, show_all: bool = False):
        """Display stock information in a formatted way"""
        if not data:
            print("No data available for this symbol.")
            return
        
        # Header
        print(f"\n{self.colorize('=' * 60, 'bold')}")
        name_symbol = f"{data['name']} ({data['symbol']})"
        print(f"{self.colorize(name_symbol, 'bold')}")
        print(f"{self.colorize('=' * 60, 'bold')}")
        
        # Price and change
        price_color = 'green' if data['change'] >= 0 else 'red'
        change_symbol = '▲' if data['change'] >= 0 else '▼'
        
        print(f"\n{self.colorize('Current Price:', 'bold')} {self.colorize(self.format_currency(data['current_price']), price_color)}")
        change_text = f"{change_symbol} {self.format_currency(data['change'])} ({self.format_percentage(data['change_percent'])})"
        print(f"{self.colorize('Change:', 'bold')} {self.colorize(change_text, price_color)}")
        print(f"{self.colorize('Previous Close:', 'bold')} {self.format_currency(data['previous_close'])}")
        
        # Basic trading info (only show in detailed mode)
        if detailed:
            print(f"\n{self.colorize('Trading Info:', 'bold')}")
            print(f"  High: {self.format_currency(data['high'])}")
            print(f"  Low: {self.format_currency(data['low'])}")
            print(f"  Volume: {data['volume']:,}")
        
        # Display additional information based on options
        if detailed or specific_fields or show_all:
            if show_all:
                # Display all available fields organized by category
                self._display_all_fields(data)
            elif specific_fields:
                # Display only specified fields
                self._display_specific_fields(data, specific_fields)
            else:
                # Display traditional detailed info (backward compatibility)
                self._display_detailed_info(data)
        
        # Timestamp
        print(f"\n{self.colorize('Last Updated:', 'bold')} {data['timestamp']}")
        print(f"{self.colorize('=' * 60, 'bold')}\n")
    
    def _display_detailed_info(self, data: Dict[str, Any]):
        """Display comprehensive detailed information"""
        print(f"\n{self.colorize('Additional Info:', 'bold')}")
        if 'marketCap' in data:
            print(f"  Market Cap: {self.format_large_number(data['marketCap'])}")
        if 'trailingPE' in data:
            print(f"  P/E Ratio: {data['trailingPE']:.2f}")
        if 'dividendYield' in data:
            print(f"  Dividend Yield: {data['dividendYield']*100:.2f}%")
    
    def _display_specific_fields(self, data: Dict[str, Any], fields: list):
        """Display only the specified fields"""
        print(f"\n{self.colorize('Requested Fields:', 'bold')}")
        for field in fields:
            if field in self.all_fields:
                display_name = self.all_fields[field]
                value = data.get(field)
                formatted_value = self.format_field_value(field, value)
                print(f"  {display_name}: {formatted_value}")
            else:
                print(f"  {field}: Field not available")
    
    def _display_all_fields(self, data: Dict[str, Any]):
        """Display all available fields organized by category"""
        for category, fields in self.field_categories.items():
            # Check if any fields in this category have data
            category_data = []
            for field_key, display_name in fields.items():
                if field_key in data and data[field_key] is not None:
                    formatted_value = self.format_field_value(field_key, data[field_key])
                    category_data.append((display_name, formatted_value))
            
            if category_data:
                print(f"\n{self.colorize(f'{category}:', 'bold')}")
                for display_name, formatted_value in category_data:
                    print(f"  {display_name}: {formatted_value}")
    
    def run(self, args):
        """Main CLI runner"""
        parser = argparse.ArgumentParser(
            description='Get real-time stock information',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  stk NVDA                    # Get basic info for NVIDIA
  stk AAPL -d                 # Get detailed info for Apple
  stk TSLA --json             # Get JSON output for Tesla
  stk NVDA --chart            # Show price chart for NVIDIA
  stk AAPL --chart --period 3mo --type candlestick  # 3-month candlestick chart
  stk NVDA --all              # Show all available metrics organized by category
  stk AAPL --fields marketCap trailingPE dividendYield  # Show specific fields
  stk --list-fields           # List all available fields
            """
        )
        
        parser.add_argument('symbol', nargs='?', help='Stock symbol (e.g., NVDA, AAPL, TSLA)')
        parser.add_argument('-d', '--detailed', action='store_true', 
                          help='Show detailed information including market cap, P/E ratio, etc.')
        parser.add_argument('--json', action='store_true',
                          help='Output data in JSON format')
        parser.add_argument('--no-colors', action='store_true',
                          help='Disable colored output')
        
        # Chart options
        parser.add_argument('--chart', action='store_true',
                          help='Display a chart of historical data')
        parser.add_argument('--period', default='1mo',
                          choices=['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'],
                          help='Time period for chart data (default: 1mo)')
        parser.add_argument('--type', default='line',
                          choices=['line', 'candlestick', 'volume'],
                          help='Chart type (default: line)')
        
        # Field selection options
        parser.add_argument('--all', action='store_true',
                          help='Show all available metrics organized by category')
        parser.add_argument('--fields', nargs='+', metavar='FIELD',
                          help='Show specific fields (e.g., marketCap trailingPE dividendYield)')
        parser.add_argument('--list-fields', action='store_true',
                          help='List all available fields and exit')
        
        # Parse arguments
        parsed_args = parser.parse_args(args)
        
        # Handle list-fields option
        if parsed_args.list_fields:
            self._list_available_fields()
            return
        
        # Check if symbol is required
        if not parsed_args.symbol and not parsed_args.list_fields:
            parser.error("symbol is required unless using --list-fields")
        
        # Disable colors if requested
        if parsed_args.no_colors:
            self.colors = {color: '' for color in self.colors}
        
        # Handle chart display
        if parsed_args.chart:
            self.display_chart(parsed_args.symbol, parsed_args.period, parsed_args.type)
            return
        
        # Get stock data
        data = self.get_stock_data(parsed_args.symbol)
        
        if not data:
            print(f"Could not fetch data for symbol: {parsed_args.symbol}")
            print("Please check the symbol and try again.")
            sys.exit(1)
        
        # Display results
        if parsed_args.json:
            # Remove timestamp for JSON output
            json_data = data.copy()
            del json_data['timestamp']
            print(json.dumps(json_data, indent=2))
        else:
            self.display_stock_info(data, parsed_args.detailed, parsed_args.fields, parsed_args.all)
    
    def _list_available_fields(self):
        """List all available fields organized by category"""
        print(f"{self.colorize('Available Fields:', 'bold')}")
        print("=" * 50)
        
        for category, fields in self.field_categories.items():
            print(f"\n{self.colorize(category, 'bold')}")
            print("-" * len(category))
            for field_key, display_name in fields.items():
                print(f"  {field_key:<25} - {display_name}")
        
        print(f"\n{self.colorize('Usage Examples:', 'bold')}")
        print("-" * 20)
        print("  stk AAPL --all")
        print("  stk NVDA --fields marketCap trailingPE dividendYield")
        print("  stk TSLA --fields revenue profitMargins returnOnEquity")

def main():
    """Entry point for the CLI"""
    cli = StockCLI()
    cli.run(sys.argv[1:])

if __name__ == "__main__":
    main()
