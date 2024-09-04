import requests

def get_public_ip():
    try:
        # Make a request to a public IP service
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()  # Raise an error for bad responses
        ip_data = response.json()
        return ip_data.get('ip')
    except requests.RequestException as e:
        print(f"Error fetching IP address: {e}")
        return None

if __name__ == '__main__':
    public_ip = get_public_ip()
    if public_ip:
        print(f"Your public IP address is: {public_ip}")
