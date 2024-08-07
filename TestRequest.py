import requests
import json
import string

# Define the URL
url = 'http://localhost:8001/users'

 

# Define the headers
headers = {
    'Content-Type': 'application/json',
    'Token': 'exampleToken',
    'Session': 'exampleSession'
}

# Define the data to send
data = {
}

# Send a PUT request
try:
    response = requests.get(url, headers = headers)
except ConnectionError as e:
    print(f"Connection error has occurred, -->")

# Print the response
print(f"Status Code: {response.status_code}")
print(f"Response Body: {response.text}")
