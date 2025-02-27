from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remote-debugging-port=9222")

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Navigate to a website
driver.get("https://example.com")

# Perform your automation tasks here
print(driver.title)

# Close the browser
driver.quit()
