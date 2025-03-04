from seleniumwire import webdriver  # Using seleniumwire to capture network requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

# Optional: for debugging, you can take a screenshot to ensure the page loaded correctly
# driver.get_screenshot_as_file("screenshot.png")

# Wait for the element to be visible using a more generic selector if needed.
try:
    # You can try either the exact class or a more flexible one:
    tap_area = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div._tapArea_njdmz_15"))
        # Alternatively, try:
        # EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class^='_tapArea']"))
    )
    # Use JavaScript click if normal click doesn't work
    driver.execute_script("arguments[0].click();", tap_area)
    print("Button clicked using JavaScript.")
except Exception as e:
    print("Button not found or not clickable:", e)

# Wait for the POST request to be generated after clicking the button
time.sleep(15)  # Adjust this based on how long the request takes

# Intercept the network requests to find the POST request to the API endpoint
captured_payload = None
target_url = 'https://gold-eagle-api.fly.dev/tap'
for request in driver.requests:
    if target_url in request.url and request.method == 'POST':
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
        'Authorization': 'Bearer YOUR_TOKEN_HERE',
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
