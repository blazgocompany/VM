import pyautogui
import io
import base64
from PIL import Image
from supabase import Client, create_client
import time

# Supabase settings (replace with your own Supabase project details)
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-api-key"
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

# Send screenshot to Supabase
def send_to_supabase(image_base64, supabase_client):
    try:
        # Insert data into the 'screenshots' table (adjust table and column names as needed)
        data = {"image": image_base64, "created_at": time.time()}
        supabase_client.table(TABLE_NAME).insert(data).execute()
        print("Screenshot sent to Supabase")
    except Exception as e:
        print(f"Error sending screenshot: {e}")

# Main loop to continuously capture and send screenshots
def main():
    supabase_client = init_supabase()
    
    while True:
        # Capture the screen
        screenshot_base64 = capture_screen()
        
        # Send to Supabase
        send_to_supabase(screenshot_base64, supabase_client)
        
        # Add a delay between screenshots (adjust the frequency as needed)
        time.sleep(1)

if __name__ == "__main__":
    main()
