import csv
from rich import print
from rich.table import Table

# Assuming you already have csv_file_path defined
csv_file_path = "filePnL.csv"  # Replace with your CSV file path

# Create a table to display the selected columns with custom headers
table = Table(show_header=True, header_style="bold cyan")
table.add_column("Source", style="bold")
table.add_column("Key", style="bold")
table.add_column("P&L", style="bold")
table.add_column("P&L%", style="bold")  # Add the "PnL%" column

# Initialize the total profit variable
total_profit = 0
try:
    # Open the CSV file for reading
    with open(csv_file_path, newline='') as csvfile:
        # Create a CSV reader
        csvreader = csv.reader(csvfile)
        
        # Skip the header row
        header_row = next(csvreader)
        
        # Iterate over each row in the CSV file and add it to the table
        for row in csvreader:
            source, key, pnl, pnl_percentage = row[0], row[1], row[4], row[6]
            total_profit += float(pnl)  # Accumulate the total profit
            table.add_row(source, key, pnl, pnl_percentage)

    # Print the table
    print(table)

    # Print the total profit in green
    print(f"[bold green]Day Profit Booked: ${total_profit:.2f}[/bold green]")
except FileNotFoundError:
    print("[bold red]Still Waiting on Profits![/bold red]")
