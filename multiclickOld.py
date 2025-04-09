import pyautogui
import time
import threading
import keyboard
from pynput import mouse

# Global variable to store the click coordinate
coordinate = None
clickDelay = 3
num_clicks = 10
pause_duration = 1

# Global flag to indicate when to stop the clicking loop
stop_program = False

# ----------------------------
# Input Listener Function
# ----------------------------

def check_for_exit():
    """
    This function waits for console input.
    When you press Enter (or input any text and press Enter),
    it sets the stop_program flag to True.
    """
    global stop_program
    while True:
        if keyboard.is_pressed('x'):
            stop_program=True
            break
            


# Define a callback to capture the first click
def on_click(x, y, button, pressed):
    global coordinate
    if pressed:
        coordinate = (x, y)
        print(f"Coordinate set to {coordinate}")
        # Stop the listener after the first click
        return False

def main():
    global coordinate

    """
    try:
        # Get user input for the number of clicks and pause duration
        num_clicks = int(input("Enter the number of clicks: "))
        pause_duration = float(input("Enter the pause duration between clicks (in seconds): "))
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        return
    """

    print("Please click anywhere on your screen to set the click coordinate.")
    # Wait for the first click to capture the coordinate
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

    if coordinate is None:
        print("No coordinate was captured. Exiting.")
        return

    # Start the input listener in a separate daemon thread.
    # This will allow the program to monitor for user input (pressing Enter) concurrently.
    threading.Thread(target=check_for_exit, daemon=True).start()

    print(f"Starting automated clicks in {clickDelay} seconds. Press Enter to quit at any time.")
    time.sleep(clickDelay)
    
    try:
        for i in range(num_clicks):
            if stop_program:
                print("Program stopped by user input.")
                break
            pyautogui.click(coordinate[0], coordinate[1])
            print(f"Clicked at {coordinate} ({i+1}/{num_clicks})")
            time.sleep(pause_duration)
    except KeyboardInterrupt:
        print("\nScript terminated by user.")

if __name__ == "__main__":
    main()