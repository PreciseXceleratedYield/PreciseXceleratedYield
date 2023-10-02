import yfinance as yf
from rich import print

def get_day_status(symbol):
    try:
        # Download historical daily data for the given symbol for the last 5 days
        data = yf.download(symbol, period="5d")

        # Check if data was retrieved and contains at least five rows
        if data.empty or len(data) < 5:
            return "Not enough trading data available for the last 5 days."

        # Extract OHLC data for the current and previous day
        current_close = data["Close"].iloc[-1]
        current_open = data["Open"].iloc[-1]
        previous_close = data["Close"].iloc[-2]

        # Calculate Open Change %
        open_change_percent = (( current_close - current_open) / current_open) * 100

        # Calculate Day Change %
        day_change_percent = ((current_close - previous_close) / previous_close) * 100

        # Determine the day's status based on the current close and open prices
        if current_close > current_open:
            if current_close > previous_close:
                day_status = "Super Bull"
            else:
                day_status = "Bull"
        elif current_close < current_open:
            if current_close < previous_close:
                day_status = "Danger Bear"
            else:
                day_status = "Bear"
        else:
            day_status = "Neutral"

        # Define colors based on day status
        if day_status == "Super Bull":
            status_color = "[bold green]"
        elif day_status == "Bull":
            status_color = "[green]"
        elif day_status == "Danger Bear":
            status_color = "[bold red]"
        elif day_status == "Bear":
            status_color = "[red]"
        else:
            status_color = "[blue]"

        # Create a formatted response string with color
        response = (
            f"Today's High:\t {data['High'].iloc[-1]:.2f}\n"
            f"Previous Close:\t {previous_close:.2f}  <--- NSE Day Change %:\t {day_change_percent:.2f}%\n"
            f"Today's Open:\t {current_open:.2f}  <--- NSE Open Change %:\t {open_change_percent:.2f}%\n"
            f"Today's Low:\t {data['Low'].iloc[-1]:.2f}\n"
            f"Current Close:\t {current_close:.2f}  <--- Day Status:            {status_color}{day_status}[/]"
        )

        return response

    except Exception as e:
        print(f"An error occurred: {e}")
        return f"An error occurred: {e}"

if __name__ == "__main__":
    # Define the stock symbol (NSEI for Nifty 50)
    symbol = "^NSEI"

    # Get and print the response with colors
    response = get_day_status(symbol)
    print(response)
