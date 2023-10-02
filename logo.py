# Define the ASCII art for "PXY" with "X" from "PrecisionXceleratedYield"
pxy_ascii = """
  P   Y
    X
  P   Y
"""

# Define the surrounding text
surrounding_text = "PrecisionXceleratedYield Securities™: All Rights Reserved."

# Calculate the number of spaces needed to center the text
total_width = max(len(pxy_ascii.splitlines()[0]), len(surrounding_text))
padding = " " * ((total_width - len(surrounding_text)) // 2)

# Combine the "PXY" graphics with the surrounding text
output = f"{padding}{surrounding_text.replace('X', pxy_ascii)}\n{padding}"

# Print the combined output
print(output)

