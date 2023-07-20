import os

# Get the width of the console screen
console_width = os.get_terminal_size().columns

# Print a message centered on the screen
message = "Hello, world!"
centered_message = message.center(console_width)
print(centered_message)
