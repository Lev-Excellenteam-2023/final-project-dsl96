import asyncio
import signal
import sys
import time
import explainer_service

# Define a flag to indicate if the loop should continue running
running = True


# Define a signal handler to handle termination signal (CTRL+C)
def signal_handler(signal, frame):
    global running
    running = False
    print("Termination signal received. Stopping the loop.")


# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)


async def run_loop():
    # Run the loop until running flag is set to False
    while running:
        print('run')
        await explainer_service.explain_new_presentation()

        await asyncio.sleep(2)

    print('stop')
    # Exit the script
    sys.exit(0)


if __name__ == '__main__':
    asyncio.run(run_loop())
