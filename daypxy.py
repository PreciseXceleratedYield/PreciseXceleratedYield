import yfinance as yf
import os
import sys

def get_nse_action():
    # Define the stock symbol (NSEI for Nifty 50)
    stock_symbol = "^NSEI"

    try:
        # Redirect standard output to os.devnull to suppress messages
        sys.stdout = open(os.devnull, 'w')

        # Download today's data
        data = yf.download(stock_symbol, period="1d")
    except Exception as e:
        print(f"Error: {e}")
        return "Error", None

    finally:
        # Restore standard output
        sys.stdout.close()
        sys.stdout = sys.__stdout__

    # Extract today's open, yesterday's close, and current price
    today_open = data['Open'].iloc[0]
    yesterday_close = data['Close'].iloc[0]
    current_price = data['Close'].iloc[-1]

    # Initialize Day Action as an empty string
    nse_action = ""

    # Determine the candlestick condition for today
    if current_price > today_open and current_price > yesterday_close:
        nse_action = "Congratulations! You're entering a SuperBull market. Good luck with your investments!"
        nse_factor = "Keep in mind that SuperBull markets can be highly volatile, so stay vigilant."
    elif current_price < today_open and current_price < yesterday_close:
        nse_action = "Be cautious! You're entering a DangerBear market. Make informed decisions and manage risks."
        nse_factor = "DangerBear markets can be challenging, so consider your investment strategy carefully."
    elif current_price > today_open:
        nse_action = "You're in a Bull market. Best of luck with your trades!"
        nse_factor = "Bull markets can offer opportunities, but monitor the trend closely."
    elif current_price < today_open:
        nse_action = "Prepare for a Bear market. Stay defensive and focus on risk management."
        nse_factor = "Bear markets can be challenging, so be cautious with your investments."
    else:
        nse_action = "The market condition is Neutral. Take your time to assess the situation."
        nse_factor = "In Neutral markets, it's essential to have a well-defined strategy."

    return nse_action, nse_factor

# Call the get_nse_action function
nse_action, nse_factor = get_nse_action()
print(f"NSE Action: {nse_action}")
print(f"NSE Factor: {nse_factor}")





