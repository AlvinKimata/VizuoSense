import requests

url = 'http://127.0.0.1:81/inference'
files = {'file': open('C:\\Users\\Alvin.Kimata\\Documents\\Python\\VizuoSense\\GeminiPRO-Tiny\\gemini\\samples\\jfk.wav', 'rb')}
data = {
    'temperature': '0.0',
    'temperature_inc': '0.2',
    'response_format': 'json'
}
headers = {'Content-Type': 'multipart/form-data'}

# Set timeout parameter to avoid hanging connections
timeout = 10

# Make the API call with retries and increased timeout
for i in range(3):
    try:
        # response = requests.post(url, headers=headers, files=data, timeout=timeout)
        response = requests.post(url, files=files)
        
        # Check the status code and print the response
        if response.status_code == 200:
            print(response.json())
            break
        else:
            print(f'Request failed with status code {response.status_code}. Retrying...')
            
    except (requests.exceptions.ChunkedEncodingError, requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
        print(f'Request failed due to exception: {str(e)}. Retrying...')
    
    # Wait for 5 seconds before retrying
    import time
    time.sleep(5)

else:
    print('All attempts have failed. Please check your network connection and try again later.')