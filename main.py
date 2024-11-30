import time
import base64
import io
from PIL import ImageGrab, Image
import pyautogui
from supabase import create_client
import threading

# Supabase settings (replace with your own Supabase project details)
SUPABASE_URL = "https://satmvokneygpwesdfdwx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNhdG12b2tuZXlncHdlc2RmZHd4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzI5MjUzNDYsImV4cCI6MjA0ODUwMTM0Nn0.-u-CEmdIL2wLIP4UnTUQMc3bvwYGoGMkbJqsS1rVmwc"
TABLE_NAME = "screenshots"

# Initialize Supabase client
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

# Function to capture the screen and send it to Supabase
def capture_screen():
    screenshot = ImageGrab.grab()
    byte_io = io.BytesIO()
    screenshot.save(byte_io, format="PNG")
    byte_io.seek(0)
    image_base64 = base64.b64encode(byte_io.read()).decode("utf-8")
    return image_base64

# Function to simulate cursor movement
def move_cursor(x, y):
    pyautogui.moveTo(x, y)

# Function to simulate mouse click
def click_mouse(x, y):
    pyautogui.click(x, y)

# Function to upsert the screenshot and cursor to Supabase
def upsert_to_supabase(image_base64, cursor_x, cursor_y, click_x, click_y, supabase_client):
    try:
        data = {
            "id": 1,  # Use a fixed ID for a single row
            "image": image_base64,
            "cursor_x": cursor_x,
            "cursor_y": cursor_y,
            "click_x": click_x,
            "click_y": click_y,
            "created_at": time.time()
        }
        response = supabase_client.table(TABLE_NAME).upsert(data, on_conflict=["id"]).execute()
        if response.status_code == 200:
            print("Screenshot, cursor, and click position upserted.")
        else:
            print("Failed to upsert screenshot.")
    except Exception as e:
        print(f"Error updating Supabase: {e}")

# Function to simulate server actions (capture screen and process updates)
def server_loop():
    supabase_client = init_supabase()
    click_position = None
    while True:
        # Capture the screen and get cursor position
        screenshot_base64 = capture_screen()
        cursor_x, cursor_y = pyautogui.position()
        
        # Check if there is a click position update from the client
        if click_position:
            click_x, click_y = click_position
        else:
            click_x, click_y = None, None

        # Upsert the data to Supabase
        upsert_to_supabase(screenshot_base64, cursor_x, cursor_y, click_x, click_y, supabase_client)
        
        time.sleep(1)  # Adjust to control how often the server updates the screen

# Listen for cursor and click events from the client
def listen_for_client_commands(supabase_client):
    while True:
        # Get the latest client input (cursor movement or click)
        response = supabase_client.table(TABLE_NAME).select("*").eq("id", 1).execute()
        if response.status_code == 200:
            data = response.data[0]
            # Check if there's any update on click or cursor position
            click_x = data.get('click_x')
            click_y = data.get('click_y')
            if click_x and click_y:
                click_mouse(click_x, click_y)
            move_cursor(data['cursor_x'], data['cursor_y'])

        time.sleep(1)  # Poll the table every second for updates

# Run server loop in separate thread
def start_server():
    supabase_client = init_supabase()
    threading.Thread(target=server_loop, args=()).start()
    listen_for_client_commands(supabase_client)

if __name__ == "__main__":
    start_server()
