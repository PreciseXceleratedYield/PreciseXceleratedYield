import yfinance as yf
import warnings
from rich import print
from rich.console import Console
from rich.style import Style
import sys

# Set the PYTHONIOENCODING environment variable to 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

# Suppress yfinance warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Specify the stock symbol (NIFTY 50)
symbol = '^NSEI'

# Intervals in minutes
intervals = [5]

# Create a Console instance for rich print formatting
console = Console()

# Function to calculate the Heikin-Ashi candle colors for the last three closed candles
def calculate_last_three_heikin_ashi_colors(symbol, interval):
    # Fetch real-time data for the specified interval
    data = yf.Ticker(symbol).history(period='1d', interval=f'{interval}m')

    # Calculate Heikin-Ashi candles
    ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
    ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

    # Calculate the colors of the last three closed candles
    current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
    last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'
    second_last_closed_color = 'Bear' if ha_close.iloc[-3] < ha_open.iloc[-3] else 'Bull'
    third_last_closed_color = 'Bear' if ha_close.iloc[-4] < ha_open.iloc[-4] else 'Bull'
    fourth_last_closed_color = 'Bear' if ha_close.iloc[-5] < ha_open.iloc[-5] else 'Bull'

    print(f'Nifty Action ------> : 4th:{"🔴🔴🔴" if fourth_last_closed_color == "Bear" else "🟢🟢🟢"}|3rd:{"🔴🔴🔴" if third_last_closed_color == "Bear" else "🟢🟢🟢"}|2nd:{"🔴🔴🔴" if second_last_closed_color == "Bear" else "🟢🟢🟢"}|1st:{"🔴🔴🔴" if last_closed_color == "Bear" else "🟢🟢🟢"}|now:{"🐻🔴🛬⤵️" if current_color == "Bear" else "🐂🟢🛫⤴️"}')


    return current_color, last_closed_color, second_last_closed_color, third_last_closed_color

# Function to determine the market check based on candle colors
def get_market_check(symbol):
    # Check the colors of the last two closed candles and the currently running candle
    current_color, last_closed_color, second_last_closed_color, third_last_closed_color = calculate_last_three_heikin_ashi_colors(symbol, intervals[0])

    # Initialize messages
    title = ""

    # Define styles for rich.print
    bear_style = Style(color="red")
    bull_style = Style(color="green")
    buy_style = Style(color="green")
    sell_style = Style(color="red")

    # Determine the market check based on the candle colors and use rich.print to format output
    if last_closed_color == 'Bear' and second_last_closed_color == 'Bear':
        mktpxy = 'Bear'
        console.print("🐻🔴🔴🔴 [bold]Bearish sentiment![/bold] 🍯💰", style=bear_style)
    elif last_closed_color == 'Bull' and second_last_closed_color == 'Bull':
        mktpxy = 'Bull'
        console.print("🐂🟢🟢🟢 [bold]Bullish sentiment![/bold] 💪💰", style=bull_style)
    elif last_closed_color == 'Bear' and second_last_closed_color == 'Bull':
        mktpxy = 'Sell'
        console.print("🛒🔴🛬⤵️ [bold]Time to sell![/bold] 📉💰", style=sell_style) 
    elif last_closed_color == 'Bull' and second_last_closed_color == 'Bear':
        mktpxy = 'Buy'
        console.print("🚀🟢🛫⤴️ [bold]Time to buy![/bold] 🌠💰", style=buy_style)
    else:
        mktpxy = None
        console.print("🌟 [bold]Market on standby![/bold] 🍿💰📊")

    return mktpxy

# Call the function and store the result in a variable
mktpxy = get_market_check('^NSEI')

# Print the result (you can remove this if not needed)
print(f"mktpxy: {mktpxy}")
