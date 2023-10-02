import sys
from toolkit.logger import Logger
from login_get_kite import get_kite, remove_token  # Import remove_token function
from cnstpxy import dir_path

# Configure logging
logging = Logger(30, dir_path + "main.log")

def print_available_cash(broker):
    try:
        logging.debug("getting available cash ...")
        # Assuming kite is defined somewhere in the get_kite function
        # Use the 'margins' method to get margin data without specifying a segment
        response = broker.kite.margins()

        # Access the available cash from the response
        available_cash = response["equity"]["available"]["live_balance"]
        print(f"Available Cash: {available_cash}")
        
    except Exception as e:
        remove_token(dir_path)  # Call the remove_token function
        logging.error(f"{str(e)} unable to get available cash")
        sys.exit(1)

if __name__ == "__main__":
    try:
        # Assuming kite is defined in the get_kite function
        broker = get_kite(api="bypass", sec_dir=dir_path)
    except Exception as e:
        remove_token(dir_path)  # Call the remove_token function
        logging.error(f"{str(e)} unable to get broker")
        sys.exit(1)

    print_available_cash(broker)
