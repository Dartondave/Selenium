import requests
import time
import json
from seleniumwire import webdriver  # Using seleniumwire for request interception
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def load_tokens(filename="data.txt"):
    """Load Bearer tokens from a file."""
    try:
        with open(filename, "r") as file:
            tokens = [line.strip() for line in file if line.strip()]
            return tokens
    except FileNotFoundError:
        return []

# ====== Step 1: Load token from data.txt ======
tokens = load_tokens()
if not tokens:
    print("[-] No tokens available. Exiting.")
    exit()
token = tokens[0]

# ====== Step 2: Poll the API for User Balance ======
headers = {
    "authorization": f"Bearer {token}",
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
}
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

# ====== Step 3: Set up Selenium with Request Interceptor and Mobile Emulation ======
chrome_options = Options()
# For debugging, you might remove headless mode temporarily:
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
# Set a mobile user agent similar to Kiwi's:
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Kiwi/5.0 Chrome/87.0.4280.141 Mobile Safari/537.36")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def interceptor(request):
    request.headers['authorization'] = f"Bearer {token}"
driver.request_interceptor = interceptor

# ====== Step 4: Load a UI Page ======
# We load a generic Telegram Web App page.
# (If you have the correct game URL, replace the URL below.)
ui_url = "https://telegram.geagle.online"
driver.get(ui_url)
time.sleep(5)  # Allow time for the page to load

# ====== Step 5: Inject Telegram Initialization Data ======
# Use the values from your Kiwi session (sample values below)
init_params = {
    "tgWebAppData": "query_id=AAG8XExdAAAAALxcTF0fzld9&user=%7B%22id%22%3A1565285564%2C%22first_name%22%3A%22%E6%B0%94DARTON%E4%B9%88%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22DartonTV%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A//t.me/i/userpic/320/iy3Hp0CdIo6mZaYfi83EHd7h2nPyXG1Fd5V50-SkD2I.svg%22%7D",
    "tgWebAppVersion": "7.10",
    "tgWebAppPlatform": "ios",
    "tgWebAppThemeParams": "{\"bg_color\":\"#212121\",\"button_color\":\"#8774e1\",\"button_text_color\":\"#ffffff\",\"hint_color\":\"#aaaaaa\",\"link_color\":\"#8774e1\",\"secondary_bg_color\":\"#181818\",\"text_color\":\"#ffffff\",\"header_bg_color\":\"#212121\",\"accent_text_color\":\"#8774e1\",\"section_bg_color\":\"#212121\",\"section_header_text_color\":\"#8774e1\",\"subtitle_text_color\":\"#aaaaaa\",\"destructive_text_color\":\"#ff595a\"}"
}
driver.execute_script(f"""
    window.Telegram = window.Telegram || {{}};
    window.Telegram.WebApp = window.Telegram.WebApp || {{}};
    window.Telegram.WebApp.initParams = {json.dumps(init_params)};
    sessionStorage.setItem('__telegram__initParams', JSON.stringify({json.dumps(init_params)}));
""")
print("[+] Telegram initParams injected.")
time.sleep(2)

# ====== Step 6: Inject External Telegram JS (if not auto-loaded) ======
external_js_url = "https://telegram.geagle.online/assets/index-BC9KxTS7.js"
driver.execute_script(f"""
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = '{external_js_url}';
    document.head.appendChild(script);
""")
print("[+] External JS injected.")
time.sleep(5)  # Wait for JS to load

# ====== Step 7: Send a Fetch POST Request to the Tap Endpoint ======
# Instead of trying to simulate a tap event (if the UI element isn't rendered),
# we directly trigger a POST request using fetch from the browser context.
# Note: The payload here is minimal; if the website's encryption logic relies
# on the UI event state, this may not fully work.
post_script = f"""
fetch('https://gold-eagle-api.fly.dev/tap', {{
    method: 'POST',
    headers: {{
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {token}',
        'Accept': 'application/json, text/plain, */*'
    }},
    body: JSON.stringify({{}})
}})
.then(response => response.json())
.then(data => console.log('Tap response:', data))
.catch(error => console.error('Tap error:', error));
"""
driver.execute_script(post_script)
print("[+] Fetch POST to tap endpoint executed.")
time.sleep(3)

driver.quit()
