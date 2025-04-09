import pyautogui
import time
import threading
from pynput import mouse, keyboard

# Global variable to store the click coordinate
coordinate = None
clickDelay = 3
num_clicks = 10
pause_duration = 1

# Global flag to indicate when to stop the clicking loop
stop_program = False

# ----------------------------
# Mouse Listener to Capture the Click Coordinate
# ----------------------------
def on_click(x, y, button, pressed):
    global coordinate
    if pressed:
        coordinate = (x, y)
        print(f"Coordinate set to {coordinate}")
        # Stop the mouse listener after the first click is captured.
        return False

# ----------------------------
# Keyboard Listener Callback
# ----------------------------
def on_press(key):
    """
    When a key is pressed, this callback is invoked.
    If the key 'x' is pressed, set the flag stop_program to True.x
    """
    global stop_program
    try:
        # Check if the pressed key's character is 'x' (case-insensitive).
        if key.char.lower() == 'x':
            stop_program = True
            print("Key 'x' pressed. Stopping...")
            # Return False to stop the keyboard listener if desired.
            return False
    except AttributeError:
        # Some keys (like special keys) don't have a 'char' attribute.
        pass

def keyboard_listener():
    """
    Starts a keyboard listener that monitors for key presses.
    When the 'x' key is detected, on_press() sets stop_program to True.
    """
    # The listener will keep running until it is stopped (for example, when 'x' is pressed).
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# ----------------------------
# Main Function
# ----------------------------
def main():
    global coordinate, stop_program

    # Capture the coordinate using a mouse click.
    print("Please click anywhere on your screen to set the click coordinate.")
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

    if coordinate is None:
        print("No coordinate was captured. Exiting.")
        return

    print(f"Starting automated clicks in {clickDelay} seconds.")
    print("Press 'x' at any time to stop the clicking.")
    time.sleep(clickDelay)

    # Start the keyboard listener in a separate daemon thread.
    kb_thread = threading.Thread(target=keyboard_listener, daemon=True)
    kb_thread.start()

    # Begin clicking loop.
    try:
        for i in range(num_clicks):
            if stop_program:
                print("Stop command received. Exiting loop.")
                break
            pyautogui.click(coordinate[0], coordinate[1])
            print(f"Clicked at {coordinate} ({i+1}/{num_clicks})")
            time.sleep(pause_duration)
    except KeyboardInterrupt:
        print("\nScript terminated by user.")
    finally:
        print("Program ended.")

if __name__ == "__main__":
    main()
