from seleniumwire import webdriver  # Using seleniumwire to capture network requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
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

# Open the target URL
driver.get('https://telegram.geagle.online')

# Wait until the GET request to /user/me is captured (indicating user data is loaded)
user_data_loaded = False
timeout = 30  # seconds
start_time = time.time()
while time.time() - start_time < timeout:
    for request in driver.requests:
        if 'https://gold-eagle-api.fly.dev/user/me' in request.url:
            if request.response and request.response.status_code == 200:
                user_data_loaded = True
                print("User data loaded from /user/me")
                break
    if user_data_loaded:
        break
    time.sleep(1)

if not user_data_loaded:
    print("User data was not loaded within timeout.")
    driver.quit()
    exit()

# Now find the tap area element
try:
    tap_area = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div._tapArea_njdmz_15"))
    )
except Exception as e:
    print("Could not find tap area element:", e)
    driver.quit()
    exit()

# Start tapping the button repeatedly (for example, 10 times)
tap_count = 10
for i in range(tap_count):
    try:
        # Using JavaScript click to ensure the element is triggered
        driver.execute_script("arguments[0].click();", tap_area)
        print(f"Tapped button {i+1} times.")
        time.sleep(1)  # Adjust delay between taps as necessary
    except Exception as e:
        print(f"Error tapping button on iteration {i+1}:", e)

# Optionally, if you want to capture any subsequent POST requests to /tap, you can print them:
target_url = 'https://gold-eagle-api.fly.dev/tap'
for request in driver.requests:
    if target_url in request.url and request.method == 'POST':
        try:
            payload = request.body.decode('utf-8')
        except Exception:
            payload = request.body
        print("Captured POST to /tap:", payload)

driver.quit()
