import requests
import time
import json
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

# ====== Step 1: Load token from data.txt ======
tokens = load_tokens()
if not tokens:
    print("[-] No tokens available. Exiting.")
    exit()
token = tokens[0]  # use the first token

# ====== Step 2: Poll the API for User Balance ======
headers = {
    "authorization": f"Bearer {token}",
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
}
progress_api_url = "https://gold-eagle-api.fly.dev/user/me/progress"
user_data_loaded = False
for i in range(30):  # poll for up to 30 seconds
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

# ====== Step 3: Set up Selenium with Request Interceptor and Mobile Emulation ======
chrome_options = Options()
# For debugging, you might temporarily disable headless mode:
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
# Set a mobile user agent similar to Kiwi's
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Kiwi/5.0 Chrome/87.0.4280.141 Mobile Safari/537.36")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Attach the authorization header to every outgoing request.
def interceptor(request):
    request.headers['authorization'] = f"Bearer {token}"
driver.request_interceptor = interceptor

# ====== Step 4: Navigate to the User Page ======
driver.get("https://telegram.geagle.online")
time.sleep(3)  # wait for the page to load completely

# ====== Step 5: Inject Telegram Initialization Data ======
# Replace the values below with the ones captured from your Kiwi session.
init_params = {
    "tgWebAppData": "query_id=AAG8XExdAAAAALxcTF0fzld9&user=%7B%22id%22%3A1565285564%2C%22first_name%22%3A%22%E6%B0%94DARTON%E4%B9%88%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22DartonTV%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A//t.me/i/userpic/320/iy3Hp0CdIo6mZaYfi83EHd7h2nPyXG1Fd5V50-SkD2I.svg%22%7D",
    "tgWebAppVersion": "7.10",
    "tgWebAppPlatform": "ios",
    "tgWebAppThemeParams": "{\"bg_color\":\"#212121\",\"button_color\":\"#8774e1\",\"button_text_color\":\"#ffffff\",\"hint_color\":\"#aaaaaa\",\"link_color\":\"#8774e1\",\"secondary_bg_color\":\"#181818\",\"text_color\":\"#ffffff\",\"header_bg_color\":\"#212121\",\"accent_text_color\":\"#8774e1\",\"section_bg_color\":\"#212121\",\"section_header_text_color\":\"#8774e1\",\"subtitle_text_color\":\"#aaaaaa\",\"destructive_text_color\":\"#ff595a\"}"
}
# Inject these parameters into the page as window.Telegram.WebApp.initParams and also into session storage.
driver.execute_script(f"""
    window.Telegram = window.Telegram || {{}};
    window.Telegram.WebApp = window.Telegram.WebApp || {{}};
    window.Telegram.WebApp.initParams = {json.dumps(init_params)};
    sessionStorage.setItem('__telegram__initParams', JSON.stringify({json.dumps(init_params)}));
""")
print("[+] Telegram initParams injected.")
time.sleep(2)

# ====== Step 6: Inject the External JS File ======
js_url = "https://telegram.geagle.online/assets/index-BC9KxTS7.js"
inject_script = f"""
var script = document.createElement('script');
script.type = 'text/javascript';
script.src = '{js_url}';
document.head.appendChild(script);
"""
driver.execute_script(inject_script)
print("[+] External JS injected.")
time.sleep(5)  # wait for the external JS to load and process the initParams

# ====== Step 7: Locate the Coin/Tap Area Element ======
# Try locating an element whose style contains the coin image.
try:
    coin_element = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(@style, 'gold-eagle-coin.svg')]")
        )
    )
    print("[+] Coin element found.")
except Exception as e:
    print("[-] Coin element not found:", e)
    # For debugging, save a screenshot and print part of the page source.
    driver.get_screenshot_as_file("debug_after_injection.png")
    print("Screenshot saved as debug_after_injection.png")
    print(driver.page_source[:2000])
    driver.quit()
    exit()

# ====== Step 8: Tap the Coin Element Repeatedly ======
tap_count = 10  # Adjust number of taps as needed
for i in range(tap_count):
    try:
        driver.execute_script("arguments[0].click();", coin_element)
        print(f"[+] Tapped coin {i+1} times.")
        time.sleep(1)
    except Exception as e:
        print(f"[-] Error on tap {i+1}:", e)

driver.quit()
