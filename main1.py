import requests
import time
from seleniumwire import webdriver  # using seleniumwire to intercept requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def load_tokens(filename="data.txt"):
    """Load Bearer tokens from a file."""
    try:
        with open(filename, "r") as file:
            tokens = [line.strip() for line in file if line.strip()]
            if not tokens:
                print("[-] No tokens found in", filename)
            return tokens
    except FileNotFoundError:
        print(f"[-] {filename} not found!")
        return []

# ====== Step 1: Read token from data.txt ======
tokens = load_tokens()
if not tokens:
    print("[-] No tokens available. Exiting.")
    exit()
token = tokens[0]  # Use the first token from the file

# Set headers for API calls using the token
headers = {
    "authorization": f"Bearer {token}",
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
}

# ====== Step 2: Poll the API for User Balance ======
progress_api_url = "https://gold-eagle-api.fly.dev/user/me/progress"
user_data_loaded = False
for i in range(30):  # Poll for up to 30 seconds
    try:
        response = requests.get(progress_api_url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            coins = data.get("coins_amount", 0)
            print("[+] User coins:", coins)
            user_data_loaded = True
            break
    except Exception as e:
        print("Error polling API:", e)
    time.sleep(1)

if not user_data_loaded:
    print("[-] User data not loaded. Exiting.")
    exit()

# ====== Step 3: Set up Selenium with Request Interceptor ======
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Attach the authorization header to every outgoing request.
def interceptor(request):
    request.headers['authorization'] = f"Bearer {token}"

driver.request_interceptor = interceptor

# ====== Step 4: Navigate to the User Page ======
# Now the tap area is assumed to be part of the page served at /user/me.
driver.get("https://gold-eagle-api.fly.dev/user/me")
time.sleep(3)  # Wait for the page to load fully

# ====== Step 5: Locate the Tap Area Element ======
try:
    # Adjust the selector if needed. Here we use the previously observed class.
    tap_area = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div._tapArea_njdmz_15"))
    )
    print("[+] Tap area element found.")
except Exception as e:
    print("[-] Tap area element not found:", e)
    driver.quit()
    exit()

# ====== Step 6: Tap the Element Repeatedly ======
tap_count = 10  # Adjust number of taps as needed
for i in range(tap_count):
    try:
        # Using JavaScript to click ensures the event is fired
        driver.execute_script("arguments[0].click();", tap_area)
        print(f"[+] Tapped button {i+1} times.")
        time.sleep(1)  # Delay between taps (adjust if needed)
    except Exception as e:
        print(f"[-] Error on tap {i+1}:", e)

driver.quit()
