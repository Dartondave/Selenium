from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
import requests

# Import WebDriverManager for Chrome
from webdriver_manager.chrome import ChromeDriverManager

# Configure Selenium to use Chrome in headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up the Chrome driver using WebDriverManager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the target URL
driver.get('https://telegram.geagle.online')

# Wait for the page to load and any necessary JavaScript to execute
time.sleep(5)

# Example: If you need to interact with any elements on the page, you can do so here
# For instance:
# element = driver.find_element(By.NAME, 'element_name')
# element.send_keys('some text')
# element.send_keys(Keys.RETURN)

# Prepare to send a POST request using the requests library
url = 'https://gold-eagle-api.fly.dev/tap'
headers = {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7ImlkIjoiYzA5YTE2MGMtNTFmMC00MjdiLTkxMzktNGQwZDdmYWNhMWU5IiwiZmlyc3RfbmFtZSI6IuawlERBUlRPTuS5iCIsImxhbmd1YWdlX2NvZGUiOiJlbiIsInVzZXJuYW1lIjoiRGFydG9uVFYifSwic2Vzc2lvbl9pZCI6MTQzNzI1NCwic3ViIjoiYzA5YTE2MGMtNTFmMC00MjdiLTkxMzktNGQwZDdmYWNhMWU5IiwiZXhwIjoxNzQyOTc4MjUzfQ.f_0ScBVxthVpykNsiFI-QCqxDxhaxioVqq3PXtyG_Iw',
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36'
}
payload = json.dumps({
    # Add the necessary payload data here
})

response = requests.post(url, headers=headers, data=payload)

print("Status Code:", response.status_code)
print("Response Text:", response.text)

# Clean up and close the browser
driver.quit()
