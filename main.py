from seleniumwire import webdriver  # Note: using seleniumwire instead of selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json
import requests
from webdriver_manager.chrome import ChromeDriverManager

# Configure Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up the Chrome driver using WebDriverManager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the target URL where the website generates the payload
driver.get('https://telegram.geagle.online')

# Wait for the page to load and for the website to generate its dynamic payload
time.sleep(10)  # Adjust the sleep time if necessary

# Intercept the network requests to find the POST request to the API endpoint
captured_payload = None
target_url = 'https://gold-eagle-api.fly.dev/tap'
for request in driver.requests:
    if request.url == target_url and request.method == 'POST':
        try:
            captured_payload = request.body.decode('utf-8')
        except Exception:
            captured_payload = request.body
        break

if captured_payload:
    print("Captured Payload:")
    print(captured_payload)
    
    # Optionally, forward this payload using the requests library
    headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7ImlkIjoiYzA5YTE2MGMtNTFmMC00MjdiLTkxMzktNGQwZDdmYWNhMWU5IiwiZmlyc3RfbmFtZSI6IuawlERBUlRPTuS5iCIsImxhbmd1YWdlX2NvZGUiOiJlbiIsInVzZXJuYW1lIjoiRGFydG9uVFYifSwic2Vzc2lvbl9pZCI6MTQzNzI1NCwic3ViIjoiYzA5YTE2MGMtNTFmMC00MjdiLTkxMzktNGQwZDdmYWNhMWU5IiwiZXhwIjoxNzQyOTc4MjUzfQ.f_0ScBVxthVpykNsiFI-QCqxDxhaxioVqq3PXtyG_Iw',
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36'
    }
    response = requests.post(target_url, headers=headers, data=captured_payload)
    print("Forwarded Request Response Status Code:", response.status_code)
    print("Forwarded Request Response Text:", response.text)
else:
    print("No POST request to", target_url, "was captured.")

# Clean up and close the browser
driver.quit()
