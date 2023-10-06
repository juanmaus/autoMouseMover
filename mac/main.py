# Import required libraries and modules
import tkinter as tk
from tkinter import ttk
import datetime
import pyautogui
import logging
import subprocess
import platform
import threading

# Initialize logging for debugging and tracking
def init_logger():
    logging.basicConfig(
        filename='mouse_mover.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

# Function to update elapsed time on the GUI
def update_time(start_time, time_var):
    elapsed_time = datetime.datetime.now() - start_time
    time_var.set(f"Running for {str(elapsed_time).split('.')[0]}")
    root.after(1000, update_time, start_time, time_var)

# Function to move the mouse
def move_mouse(stop_event, text_var, counter_var):
    counter = 0
    while not stop_event.is_set():
        try:
            # Move mouse 150 pixels down
            pyautogui.moveRel(0, 150)
            # Wait for 0.5 seconds
            time.sleep(0.5)
            # Move mouse 150 pixels up
            pyautogui.moveRel(0, -150)
            # Increment the movement counter
            counter += 1
            counter_var.set(f"Mouse has moved {counter} times")
            text_var.set("Mouse moving")
            logging.info("Mouse moved successfully.")
            # Wait for 5 seconds before the next movement
            time.sleep(5)
        except pyautogui.FailSafeException:
            logging.warning("FailSafeException triggered, moving mouse to center.")
            text_var.set("FailSafeException, moved to center")
            stop_event.set()

# Main function to create and control the GUI
def main():
    # Initialize the logger
    init_logger()
    
    # Set up the Tkinter GUI
    global root
    root = tk.Tk()
    root.title("Mouse Mover for macOS")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    text_var = tk.StringVar()
    text_var.set("Press Start to move mouse")
    label = ttk.Label(frame, textvariable=text_var)
    label.grid(row=0, column=0, columnspan=2)

    counter_var = tk.StringVar()
    counter_var.set("Mouse has not moved yet")
    counter_label = ttk.Label(frame, textvariable=counter_var)
    counter_label.grid(row=1, column=0, columnspan=2)

    time_var = tk.StringVar()
    time_var.set("Not started yet")
    time_label = ttk.Label(frame, textvariable=time_var)
    time_label.grid(row=2, column=0, columnspan=2)

    stop_event = threading.Event()
    caffeinate_process = None

    def start_moving():
        nonlocal caffeinate_process
        stop_event.clear()
        start_time = datetime.datetime.now()
        update_time(start_time, time_var)
        threading.Thread(target=move_mouse, args=(stop_event, text_var, counter_var)).start()
        if platform.system() == 'Darwin':
            caffeinate_process = subprocess.Popen(['caffeinate'])
            logging.info("Caffeinate command started.")

    def stop_moving():
        stop_event.set()
        text_var.set("Mouse stopped")
        counter_var.set("Mouse has not moved yet")
        if caffeinate_process:
            caffeinate_process.terminate()
            logging.info("Caffeinate command terminated.")

    start_button = ttk.Button(frame, text="Start", command=start_moving)
    start_button.grid(row=3, column=0)

    stop_button = ttk.Button(frame, text="Stop", command=stop_moving)
    stop_button.grid(row=3, column=1)

    root.mainloop()

if __name__ == '__main__':
    main()