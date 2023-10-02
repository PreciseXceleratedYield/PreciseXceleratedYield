from colorama import Fore, Style
from mktpxy import mktpxy


symbol = "^NSEI"  # Replace "AAPL" with the actual symbol you want to use

# Get the market check result

#print(f"Market Check from mktpxy script: {mktpxy}")


# Function to generate the message in Telugu and English
def generate_message(action):
    if mktpxy == 'Buy':
        telugu_message = f"{Style.BRIGHT}{Fore.GREEN}🟢🛫⤴️ ఇప్పుడు స్టాక్ మార్కెట్ అభివృద్ధి  కోసం సిద్ధమవుతోంది.{Style.RESET_ALL}"
        english_message = f"{Style.BRIGHT}{Fore.GREEN}🟢🛫⤴️ Stock market is currently growing.{Style.RESET_ALL}"
    elif mktpxy == 'Sell':
        telugu_message = f"{Style.BRIGHT}{Fore.RED}🔴🛬⤵️ ఇప్పుడు స్టాక్ మార్కెట్ పతనానికి సిద్ధమవుతోంది.{Style.RESET_ALL}"
        english_message = f"{Style.BRIGHT}{Fore.RED}🔴🛬⤵️ The stock market is currently declining.{Style.RESET_ALL}"
    elif mktpxy == 'Bull':
        telugu_message = f"{Style.BRIGHT}{Fore.GREEN}🟢🟢🟢 ఇప్పుడు స్టాక్ మార్కెట్ అభివృద్ధి చెందుతోంది.{Style.RESET_ALL}"
        english_message = f"{Style.BRIGHT}{Fore.GREEN}🟢🟢🟢 Right now, the stock market is growing.{Style.RESET_ALL}"
    elif mktpxy == 'Bear':
        telugu_message = f"{Style.BRIGHT}{Fore.RED}🔴🔴🔴 ఇప్పుడు స్టాక్ మార్కెట్ పతనమవుతోంది.{Style.RESET_ALL}"
        english_message = f"{Style.BRIGHT}{Fore.RED}🔴🔴🔴 The stock market is currently falling.{Style.RESET_ALL}"
    else:
        telugu_message = "ఇప్పుడు స్టాక్ మార్కెట్ అనిశ్చితంగా ఉంది"
        english_message = "The stock market is uncertain right now."

    return telugu_message, english_message

# Get the messages
telugu_message, english_message = generate_message(mktpxy)

# Print the messages with color
print(Fore.LIGHTYELLOW_EX + telugu_message + Style.RESET_ALL)
print("Settings- https://trendlyne.com/fundamentals/your-parameters/updated-desc-param/")
print("Nifty Chart - https://www.tradingview.com/chart/btaFLTYa/?symbol=NSE%3ANIFTY")
print("Portfolio - https://trendlyne.com/portfolio/387368")
print(Fore.LIGHTYELLOW_EX + english_message + Style.RESET_ALL)
