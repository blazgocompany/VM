import pyautogui
import io
import base64
from PIL import Image
from supabase import Client, create_client
import time

# Supabase settings (replace with your own Supabase project details)
SUPABASE_URL = "https://satmvokneygpwesdfdwx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNhdG12b2tuZXlncHdlc2RmZHd4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzI5MjUzNDYsImV4cCI6MjA0ODUwMTM0Nn0.-u-CEmdIL2wLIP4UnTUQMc3bvwYGoGMkbJqsS1rVmwc"
TABLE_NAME = "screenshots"

# Initialize Supabase client
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

# Capture screen as an image and convert to base64
def capture_screen():
    # Capture the screen
    screenshot = pyautogui.screenshot()
    # Save screenshot to a BytesIO object
    byte_io = io.BytesIO()
    screenshot.save(byte_io, format="PNG")
    byte_io.seek(0)
    # Convert the image to base64 encoding for sending
    image_base64 = base64.b64encode(byte_io.read()).decode("utf-8")
    return image_base64

# Update or insert a single screenshot to Supabase (upsert)
def upsert_to_supabase(image_base64, supabase_client):
    try:
        # Prepare data to upsert. You can use an arbitrary unique id like '1' for this purpose.
        data = {
            "id": 1,  # This is the unique identifier; you can use any constant here
            "image": image_base64,
            "created_at": time.time()  # You can also use the current time to track updates
        }
        
        # Upsert data (insert if it doesn't exist, update if it does)
        response = supabase_client.table(TABLE_NAME).upsert(data, on_conflict=["id"]).execute()
        
        if response.status_code == 200:
            print("Screenshot upserted successfully!")
        else:
            print(f"Failed to upsert screenshot: {response.status_code}")
    
    except Exception as e:
        print(f"Error updating screenshot: {e}")

# Main loop to continuously capture and send screenshots
def main():
    supabase_client = init_supabase()
    
    while True:
        # Capture the screen
        screenshot_base64 = capture_screen()
        
        # Upsert to Supabase
        upsert_to_supabase(screenshot_base64, supabase_client)
        
        # Add a delay between screenshots (adjust the frequency as needed)
        time.sleep(1)

if __name__ == "__main__":
    main()
