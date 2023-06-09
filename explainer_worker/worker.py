import signal
import sys
import time
from file_db import explainer_file_db
# Define a flag to indicate if the loop should continue running
running = True


# Define a signal handler to handle termination signal (CTRL+C)
def signal_handler(signal, frame):
    global running
    running = False
    print("Termination signal received. Stopping the loop.")


# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

db = explainer_file_db()
# Run the loop until running flag is set to False
while running:
     print( db.get_all_upload_name())
     time.sleep(2)

print('stop')
# Exit the script
sys.exit(0)
