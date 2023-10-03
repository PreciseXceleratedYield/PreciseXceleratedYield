from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from login_get_kite import get_kite, remove_token
import sys
from time import sleep
import traceback
import os
import subprocess
from cnstpxy import dir_path

SILVER = "\033[97m"
UNDERLINE = "\033[4m"
RESET = "\033[0m"
print(f'{SILVER}{UNDERLINE}"PXY™ PreciseXceleratedYield Pvt Ltd® All Rights Reserved."{RESET}')

logging = Logger(30, dir_path + "main.log")

try:
    sys.stdout = open('output.txt', 'w')
    broker = get_kite(api="bypass", sec_dir=dir_path)
except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to get holdings")
    sys.exit(1)

def order_place(index, row):
    try:
        exchsym = str(index).split(":")
        if len(exchsym) >= 2:
            logging.info(f"Placing order for {exchsym[1]}, {str(row)}")
            order_id = broker.order_place(
                tradingsymbol=exchsym[1],
                exchange=exchsym[0],
                transaction_type='SELL',
                quantity=int(row['qty']),
                order_type='LIMIT',
                product='CNC',
                variety='regular',
                price=round_to_paise(row['ltp'], -0.3)
            )
            if order_id:
                logging.info(f"Order {order_id} placed for {exchsym[1]} successfully")
                return True
            else:
                logging.error("Order placement failed")
        else:
            logging.error("Invalid format for 'index'")
    except Exception as e:
        print(traceback.format_exc())
        logging.error(f"{str(e)} while placing order")
    return False

def get_holdingsinfo(resp_list, broker):
    try:
        df = pd.DataFrame(resp_list)
        df['source'] = 'holdings'
        return df
    except Exception as e:
        print(f"An error occurred in holdings: {e}")
        return None

def get_positionsinfo(resp_list, broker):
    try:
        df = pd.DataFrame(resp_list)
        df['source'] = 'positions'
        return df
    except Exception as e:
        print(f"An error occurred in positions: {e}")
        return None

while True:
    
    try:
        import sys
        import traceback
        import pandas as pd
        import datetime
        import time
        from login_get_kite import get_kite, remove_token
        from cnstpxy import dir_path
        from toolkit.logger import Logger
        from toolkit.currency import round_to_paise
        import csv
        from cnstpxy import sellbuff, secs, perc_col_name
        from time import sleep
        import subprocess
        from selfpxy import spiritual_messages
        import random
        import os
        import numpy as np
        from mktpxy import mktpxy
        from daypxy import get_nse_action

        subprocess.run(['python', 'buypxy.py'])

        logging.debug("are we having any holdings to check")
        holdings_response = broker.kite.holdings()
        positions_response = broker.kite.positions()['net']

        holdings_df = get_holdingsinfo(holdings_response, broker)
        positions_df = get_positionsinfo(positions_response, broker)
        # Add 'key' column to holdings_df and positions_df
        # Create 'key' column if holdings_df is not empty
        holdings_df['key'] = holdings_df['exchange'] + ":" + holdings_df['tradingsymbol'] if not holdings_df.empty else None

        # Create 'key' column if positions_df is not empty
        positions_df['key'] = positions_df['exchange'] + ":" + positions_df['tradingsymbol'] if not positions_df.empty else None

        combined_df = pd.concat([holdings_df, positions_df], ignore_index=True)

        # Get OHLC data for the 'key' column
        lst = combined_df['key'].tolist()
        resp = broker.kite.ohlc(lst)

        # Create a dictionary from the response for easier mapping
        dct = {
            k: {
                'ltp': v['ohlc'].get('ltp', v['last_price']),
                'open': v['ohlc']['open'],
                'high': v['ohlc']['high'],
                'low': v['ohlc']['low'],
                'close_price': v['ohlc']['close'],
            }
            for k, v in resp.items()
        }

        # Add 'ltp', 'open', 'high', and 'low' columns to the DataFrame
        combined_df['ltp'] = combined_df.apply(lambda row: dct.get(row['key'], {}).get('ltp', row['last_price']), axis=1)
        combined_df['open'] = combined_df['key'].map(lambda x: dct.get(x, {}).get('open', 0))
        combined_df['high'] = combined_df['key'].map(lambda x: dct.get(x, {}).get('high', 0))
        combined_df['low'] = combined_df['key'].map(lambda x: dct.get(x, {}).get('low', 0))
        combined_df['close_price'] = combined_df['key'].map(lambda x: dct.get(x, {}).get('close_price', 0))
        combined_df['qty'] = combined_df.apply(lambda row: row['quantity'] + row['t1_quantity'] if row['source'] == 'holdings' else row['quantity'], axis=1)

        # Calculate 'Invested' column
        combined_df['Invested'] = combined_df['qty'] * combined_df['average_price']

        # Calculate 'value' column as 'qty' * 'ltp'
        combined_df['value'] = combined_df['qty'] * combined_df['ltp']
        combined_df['value_H'] = combined_df['qty'] * combined_df['high']

        # Calculate 'PnL' column as 'value' - 'Invested'
        combined_df['PnL'] = combined_df['value'] - combined_df['Invested']
        combined_df['PnL_H'] = combined_df['value_H'] - combined_df['Invested']

        # Calculate 'PnL%' column as ('PnL' / 'Invested') * 100
        combined_df['PnL%'] = (combined_df['PnL'] / combined_df['Invested']) * 100
        combined_df['PnL%_H'] = (combined_df['PnL_H'] / combined_df['Invested']) * 100

        # Calculate 'Yvalue' column as 'qty' * 'close'
        combined_df['Yvalue'] = combined_df['qty'] * combined_df['close_price']

        # Calculate 'dPnL' column as 'close_price' - 'ltp'
        combined_df['dPnL'] = combined_df['value'] - combined_df['Yvalue']

        # Calculate 'dPnL%' column as ('dPnL' / 'Invested') * 100
        combined_df['dPnL%'] = (combined_df['PnL'] / combined_df['Yvalue']) * 100

        # Round all numeric columns to 2 decimal places
        numeric_columns = ['qty', 'average_price', 'Invested','Yvalue', 'ltp', 'open', 'high', 'low','value', 'PnL', 'PnL%','PnL%_H', 'dPnL', 'dPnL%']
        combined_df[numeric_columns] = combined_df[numeric_columns].round(2)        # Filter combined_df
        filtered_df = combined_df[(combined_df['qty'] > 0) & (combined_df['PnL%'] > 1.4)]

        # Filter combined_df for rows where 'qty' is greater than 0
        combined_df_positive_qty = combined_df[(combined_df['qty'] > 0) & (combined_df['source'] == 'holdings')]

        # Calculate and print the sum of 'PnL' values and its total 'PnL%' for rows where 'qty' is greater than 0
        total_PnL = combined_df_positive_qty['PnL'].sum()
        total_PnL_percentage = (total_PnL / combined_df_positive_qty['Invested'].sum()) * 100

        # Calculate and print the sum of 'dPnL' values and its total 'dPnL%' for rows where 'qty' is greater than 0
        total_dPnL = combined_df_positive_qty['dPnL'].sum()
        total_dPnL_percentage = (total_dPnL / combined_df_positive_qty['Invested'].sum()) * 100

        import pandas as pd

        # Assuming you have a list of instrument keys, e.g., ['NIFTY50', 'RELIANCE', ...]
        # Replace this with your actual list of keys
        instrument_keys = ['NSE:NIFTY 50']

        # Create an empty DataFrame named NIFTY
        NIFTY = pd.DataFrame()

        # Get OHLC data for the list of keys
        resp = broker.kite.ohlc("NSE:NIFTY 50")

        # Create a dictionary from the response for easier mapping
        dct = {
            k: {
                'ltp': v['ohlc'].get('ltp', v['last_price']),
                'open': v['ohlc']['open'],
                'high': v['ohlc']['high'],
                'low': v['ohlc']['low'],
                'close_price': v['ohlc']['close'],
            }
            for k, v in resp.items()
        }

        # Set the 'key' column to the instrument keys from your list
        NIFTY['key'] = instrument_keys

        # Populate other columns based on the dct dictionary
        NIFTY['ltp'] = NIFTY['key'].map(lambda x: dct.get(x, {}).get('ltp', 0))
        NIFTY['timestamp'] = pd.to_datetime('now').strftime('%H:%M:%S')
        NIFTY['open'] = NIFTY['key'].map(lambda x: dct.get(x, {}).get('open', 0))
        NIFTY['high'] = NIFTY['key'].map(lambda x: dct.get(x, {}).get('high', 0))
        NIFTY['low'] = NIFTY['key'].map(lambda x: dct.get(x, {}).get('low', 0))
        NIFTY['close_price'] = NIFTY['key'].map(lambda x: dct.get(x, {}).get('close_price', 0))
        NIFTY['Day_Change_Perc'] = round(((NIFTY['ltp'] - NIFTY['close_price']) / NIFTY['close_price']) * 100, 2)
        NIFTY['Open_Change_Perc'] = round(((NIFTY['ltp'] - NIFTY['open']) / NIFTY['open']) * 100, 2)

        # Assuming you have a DataFrame named "NIFTY" with columns 'ltp', 'low', 'high', 'close'

        # Calculate the metrics
        NIFTY['strength'] = ((NIFTY['ltp'] - (NIFTY['low'] - 0.01)) / ((NIFTY['high'] + 0.01) - (NIFTY['low'] - 0.01)))*10
        NIFTY['pricerange'] = (NIFTY['high'] + 0.01) - (NIFTY['low'] - 0.01)
        NIFTY['priceratio'] =  (NIFTY['ltp'] - NIFTY['open'])/NIFTY['pricerange']

        # Extract and print just the values without the column name and data type information
        strength_values = NIFTY['strength'].values
        pricerange_values = NIFTY['pricerange'].values
        priceratio_values = NIFTY['priceratio'].values

        # Assuming NIFTY is a dictionary-like object with pandas Series
        Precise = max(1.9, round(((NIFTY['ltp'] - (NIFTY['low'] - 0.01)) / ((NIFTY['high'] + 0.01) - (NIFTY['low'] - 0.01))) * 10, 2).max())
        Xlratd = Precise + (NIFTY['ltp'] - NIFTY['open']).div((NIFTY['high'] + 0.01) - (NIFTY['low'] - 0.01)).mul(5).clip(lower=0).apply(lambda x: round(x, 2)).max()
        Yield = Xlratd + max(round(total_dPnL_percentage * 2, 2).max(), 0)

        # Define the file path for the CSV file
        lstchk_file = "fileHPdf.csv"
        # Dump the DataFrame to the CSV file, overwriting any existing file 
        combined_df.to_csv(lstchk_file, index=False)
        print(f"DataFrame has been saved to {lstchk_file}")
        # Create a copy of 'filtered_df' and select specific columns
        pxy_df = filtered_df.copy()[['source', 'qty', 'close_price', 'ltp', 'open', 'high', 'key','dPnL%','PnL','PnL%_H', 'PnL%']]
        pxy_df.loc[:, 'Precise'] = Precise
        pxy_df.loc[:, 'Xlratd'] = Xlratd
        pxy_df.loc[:, 'Yield'] = Yield 

        # Create a copy for just printing 'filtered_df' and select specific columns
        prnt_df = pxy_df[['source', 'key', 'qty', 'ltp', 'Precise','Xlratd','Yield','dPnL%', 'PnL%', 'PnL%_H', 'PnL']]

        # Sort the DataFrame by 'PnL%' in ascending order
        prnt_df_sorted = prnt_df.sort_values(by='PnL%', ascending=True)

        only_prnt_df_sorted = prnt_df_sorted[['source', 'key','dPnL%','PnL%_H','PnL%','Precise','Xlratd','Yield']]
        
        SILVER = "\033[97m"
        UNDERLINE = "\033[4m"
        RESET = "\033[0m"
        print(f'{SILVER}{UNDERLINE}"PXY™ PreciseXceleratedYield Pvt Ltd® All Rights Reserved."{RESET}')
        # ANSI escape codes for text coloring
        RESET = "\033[0m"
        BRIGHT_YELLOW = "\033[93m"
        BRIGHT_RED = "\033[91m"
        BRIGHT_GREEN = "\033[92m"

        # Always print "Table" in bright yellow
        print(f"{BRIGHT_YELLOW}Table– Above Precise and reaching Xcelerated{RESET}")

        # Print prnt_df_sorted without color
        print(only_prnt_df_sorted)

        import pandas as pd

        # Your real-time data
        shoot_df = only_prnt_df_sorted.copy()  # Make a copy to avoid warnings on the original DataFrame

        # Function to determine the action and reason
        def determine_action_and_reason(row):
            reasons_met = []

            if row['source'] == 'holdings':
                if (row['PnL%_H'] > row['Precise']) and (row['PnL%'] < row['Precise']):
                    reasons_met.append("PnL%_H is higher than Precise, and PnL% is lower than Precise")
                if (row['PnL%_H'] > row['Xlratd']) and (row['PnL%'] < row['Xlratd']):
                    reasons_met.append("PnL%_H is higher than Xlratd, and PnL% is lower than Xlratd")
                if row['PnL%'] > row['Yield']:
                    reasons_met.append("PnL% is higher than Yield")

            if row['source'] == 'positions' and (row['PnL%'] > row['Precise']):
                reasons_met.append("PnL% is higher than Precise")

            if reasons_met:
                return "Shoot_", ", ".join(reasons_met)
            else:
                return "", ""

        # Apply the function to create 'Action' and 'Reason' columns
        shoot_df[['Action', 'Reason']] = shoot_df.apply(determine_action_and_reason, axis=1, result_type='expand')

        # Set display options to prevent column truncation
        pd.set_option('display.max_colwidth', None)

        pd.options.display.max_colwidth = 53


        # Filter rows where the "Action" is not empty
        shoot_df = shoot_df[shoot_df['Action'] != ""]

        # Display the filtered DataFrame with the "Action" and "Reason" columns
        print(shoot_df[['key','Reason']])


        # Always print "Market view" in bright yellow
        print(f"{BRIGHT_YELLOW}My Trades Overview & Market Dynamics {RESET}")


        # ANSI escape codes for text coloring
        RESET = "\033[0m"
        BRIGHT_YELLOW = "\033[93m"
        BRIGHT_RED = "\033[91m"
        BRIGHT_GREEN = "\033[92m"

        # Print all three sets of values in a single line with rounding to 2 decimal places
        column_width = 42
        left_aligned_format = "{:<" + str(column_width) + "}"
        right_aligned_format = "{:>" + str(column_width) + "}"

        print(left_aligned_format.format(f"Strength Value: {round(strength_values[0], 2)}"), end="")
        print(right_aligned_format.format(f"Total Day dPnL {BRIGHT_GREEN if total_dPnL > 0 else BRIGHT_RED}{round(total_dPnL, 2)}{RESET}"))
        print(left_aligned_format.format(f"Price Range Value: {round(pricerange_values[0], 2)}"), end="")
        print(right_aligned_format.format(f"Total Day dPnL% {BRIGHT_GREEN if total_dPnL_percentage > 0 else BRIGHT_RED}{round(total_dPnL_percentage, 2)}{RESET}"))
        print(left_aligned_format.format(f"Price Ratio Value: {round(priceratio_values[0], 2)}"), end="")
        print(right_aligned_format.format(f"Level Check (Precise): {BRIGHT_GREEN if Precise > 2.9 else BRIGHT_RED}{round(Precise, 2)}{RESET}"))
        print(left_aligned_format.format(f"Total PnL {round(total_PnL, 2)}"), end="")
        print(right_aligned_format.format(f"Xcelerated Check (Xlratd): {BRIGHT_GREEN if Xlratd > 5 else BRIGHT_RED}{round(Xlratd, 2)}{RESET}"))
        print(left_aligned_format.format(f"Total PnL% {round(total_PnL_percentage, 2)}"))
        
  
        print(f"{BRIGHT_YELLOW}Nifty Todays OHLC  -open,high,low,close {RESET}")
        command_cndlpxy = "cndlpxy.py"
        try:
            subprocess.run(command_cndlpxy, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

        print(f"{BRIGHT_YELLOW}Laks Dash-Board{RESET}")
        command_dshpxy = "dshpxy.py"
        try:
            subprocess.run(command_dshpxy, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
        response = broker.kite.margins()
        available_cash = response["equity"]["available"]["live_balance"]
        print(f"Available Cash: {available_cash}")       
        command_prftpxy = "prftpxy.py"
        try:
            subprocess.run(command_prftpxy, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

        command_prntpxy = "prntpxy.py"
        try:
            subprocess.run(command_prntpxy, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")


        # Create an empty list to store the rows that meet the condition
        selected_rows = []

        # Define the CSV file path
        csv_file_path = "filePnL.csv"

        # Loop through the DataFrame and place orders based on conditions

        if mktpxy in ['Sell', 'Bear']:  # Check if mktpxy is 'Sell' or 'Bear'
            try:
                for index, row in prnt_df_sorted.iterrows():
                    key = row['key']  # Get the 'key' value

                    # Check the common conditions first
                    if (
                        (row['ltp'] > 0) and
                        (row['PnL%'] > 1.4)
                    ):
                        if row['source'] == 'holdings' and (
                            ((row['PnL%_H'] > row['Precise']) and (row['PnL%'] < row['Precise'])) or
                            ((row['PnL%_H'] > row['Xlratd']) and (row['PnL%'] < row['Xlratd'])) or
                            ((row['PnL%'] > row['Yield']))
                        ):
                            # Print the row before placing the order
                            print(row)

                            try:
                                import telegram
                                import asyncio
                                message_text = str(row)                                
                                # Define the bot token and your Telegram username or ID
                                bot_token = '6409002088:AAH9mu0lfjvHl_IgRAgX7YrjJQa2Ew9qaLo'  # Replace with your actual bot token
                                user_usernames = ('-4022487175')
                                 # Replace with your Telegram username or ID
                                # Function to send a message to Telegram
                                async def send_telegram_message(message_text):
                                    bot = telegram.Bot(token=bot_token)
                                    await bot.send_message(chat_id=user_usernames, text=message_text)
                            except Exception as e:
                                # Handle the exception (e.g., log it) and continue with your code
                                print(f"Error sending message to Telegram: {e}")
                                    
                            # Send the 'row' content as a message to Telegram immediately after printing the row
                            loop = asyncio.get_event_loop()
                            loop.run_until_complete(send_telegram_message(message_text))
                            try:
                                is_placed = order_place(key, row)
                                if is_placed:
                                    # Write the row to the CSV file here
                                    with open(csv_file_path, 'a', newline='') as csvfile:
                                        csvwriter = csv.writer(csvfile)
                                        csvwriter.writerow(row.tolist())  # Write the selected row to the CSV file
                            except InputException as e:
                                # Handle the specific exception and print only the error message
                                print(f"An error occurred while placing an order for key {key}: {e}")
                            except Exception as e:
                                # Handle any other exceptions that may occur during order placement
                                print(f"An unexpected error occurred while placing an order for key {key}: {e}")

                        elif row['source'] == 'positions' and (row['PnL%'] > row['Precise']):
                            # Print the row before placing the order
                            print(row)
                            try:
                                import telegram
                                import asyncio
                                message_text = str(row)                                
                                # Define the bot token and your Telegram username or ID
                                bot_token = '6409002088:AAH9mu0lfjvHl_IgRAgX7YrjJQa2Ew9qaLo'  # Replace with your actual bot token
                                user_usernames = ('-4022487175')
                                 # Replace with your Telegram username or ID
                                # Function to send a message to Telegram
                                async def send_telegram_message(message_text):
                                    bot = telegram.Bot(token=bot_token)
                                    await bot.send_message(chat_id=user_usernames, text=message_text)
                            except Exception as e:
                                # Handle the exception (e.g., log it) and continue with your code
                                print(f"Error sending message to Telegram: {e}")
                            # Your code for 'positions' condition here

                            # Place an order after both common and 'positions' conditions are met
                            try:
                                is_placed = order_place(key, row)
                                if is_placed:
                                    # Write the row to the CSV file here
                                    with open(csv_file_path, 'a', newline='') as csvfile:
                                        csvwriter = csv.writer(csvfile)
                                        csvwriter.writerow(row.tolist())  # Write the selected row to the CSV file
                            except InputException as e:
                                # Handle the specific exception and print only the error message
                                print(f"An error occurred while placing an order for key {key}: {e}")
                            except Exception as e:
                                # Handle any other exceptions that may occur during order placement
                                print(f"An unexpected error occurred while placing an order for key {key}: {e}")

            except Exception as e:
                # Handle any other exceptions that may occur during the loop
                print(f"An unexpected error occurred: {e}")

        print("\033[32mLast 30 Days P&L - https://console.zerodha.com/verified/29d1be0e\033[0m")
       
        SILVER = "\033[97m"
        UNDERLINE = "\033[4m"
        RESET = "\033[0m"



         # Your original code
        text = "PXY™ PreciseXceleratedYield Pvt Ltd® All Rights Reserved."

        # Calculate the original width of the box
        original_width = len(text) + 4  # 2 characters for each side of the box

        # Calculate the new width with a 20% increase
        new_width = int(original_width * 1.3)

        # Calculate the number of spaces to add on the left side for center alignment
        padding_left = (new_width - len(text)) // 2

        # Create the top border line with the new width
        bottom_border = f"{'_' * new_width}"

        # Create the middle part with the text, centered
        middle = f"{' ' * padding_left} {text} {' ' * padding_left}"

        # Create the top border line with the new width
        top_border = f"{' ' * new_width}"

        # Print the top border line
        print(top_border)

        # Print the middle part with the text
        print(middle)

        # Print the bottom border line
        print(bottom_border)



        import time
        import random
        from colorama import Fore, Style, init

        init(autoreset=True)  # Initialize colorama

        def sleep_with_countdown_and_messages(secs):
            message_change_interval = 15  # Change the message every 15 seconds
            current_message = ""

            for i in range(secs, 0, -1):
                if i % message_change_interval == 0:
                    current_message = random.choice(spiritual_messages)
                    # Generate a random color code from colorama
                    random_color = random.choice([Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW])
                    # Create the countdown message with the random color
                    countdown_message = f"{random_color}|{i}|{current_message}{Style.RESET_ALL}"
                else:
                    # Create the countdown message without a color
                    countdown_message = f"|{i}|{current_message}"

                # Check if the width of the message exceeds 40 characters
                if len(countdown_message) > 38:
                    sys.stdout.write(countdown_message + '\r')
                    sys.stdout.flush()
                else:
                    print(countdown_message, end='\r')
                
                time.sleep(1)
                print(" " * len(countdown_message), end='\r')  # Clear the previous message

            print("\nCountdown complete!")

        secs = 30  # Set the initial number of seconds
        time.sleep(1)
        sleep_with_countdown_and_messages(secs)



    except Exception as e:
        remove_token(dir_path)
        print(traceback.format_exc())
        logging.error(f"{str(e)} in the main loop")
