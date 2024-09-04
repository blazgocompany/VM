import requests
import time

def sse_client(url):
    try:
        with requests.get(url, stream=True, verify=False) as response:
            if response.status_code == 200:
                print("Connected to the SSE stream...")
                for line in response.iter_lines():
                    if line:
                        # Decode and print the message
                        decoded_line = line.decode('utf-8')
                        if decoded_line.startswith('data: '):
                            message = decoded_line[len('data: '):]
                            print(f"Received message: {message}")
                    # Add a short sleep to prevent excessive CPU usage
                    time.sleep(0.1)
            else:
                print(f"Failed to connect, status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    # URL of the SSE endpoint
    sse_url = 'https://blazgo.epizy.com/vm/vm.php'
    sse_client(sse_url)
