import signal
import sys
import time

# Define a flag to indicate if the loop should continue running
running = True


# Define a signal handler to handle termination signal (CTRL+C)
def signal_handler(signal, frame):
    global running
    running = False
    print("Termination signal received. Stopping the loop.")


# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

# Run the loop until running flag is set to False
while running:
     print('run')
     time.sleep(2)

# Exit the script
sys.exit(0)
