import requests
import time
import json
from seleniumwire import webdriver  # using seleniumwire for request interception
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

# === Step 1: Load token from data.txt ===
tokens = load_tokens()
if not tokens:
    print("[-] No tokens available. Exiting.")
    exit()
token = tokens[0]

# === Step 2: Poll the API for User Balance ===
headers = {
    "authorization": f"Bearer {token}",
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
}
progress_api_url = "https://gold-eagle-api.fly.dev/user/me/progress"
user_data_loaded = False
for i in range(30):
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

# === Step 3: Set up Selenium with Request Interceptor and Mobile Emulation ===
chrome_options = Options()
# Uncomment the following line to disable headless mode for debugging:
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Kiwi/5.0 Chrome/87.0.4280.141 Mobile Safari/537.36")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def interceptor(request):
    request.headers['authorization'] = f"Bearer {token}"
driver.request_interceptor = interceptor

# === Step 4: Load the Mini-App UI ===
# Use the full UI URL (e.g. the referral URL you see in Kiwi)
full_url = "https://t.me/gold_eagle_coin_bot/main?startapp=r_gTGFKMkFC5"
driver.get(full_url)
time.sleep(5)

# === Step 5: Inject Telegram Initialization Data ===
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

# === Step 6: Inject External Telegram JS (if necessary) ===
external_js_url = "https://telegram.geagle.online/assets/index-BC9KxTS7.js"
driver.execute_script(f"""
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = '{external_js_url}';
    document.head.appendChild(script);
""")
print("[+] External JS injected.")
time.sleep(5)

# === Step 7: Run the Tapping Loop ===
# In this approach, we send a batch of 200 tap requests in rapid succession,
# then sleep for 3 minutes, then repeat.
# Here, we run the loop for a given number of cycles; adjust cycles as needed.
cycles = 3  # For example, run 3 cycles (each cycle: one batch then 3 minutes sleep)
for cycle in range(1, cycles + 1):
    print(f"[+] Starting cycle {cycle}: Sending batch of 200 taps.")
    batch_script = f"""
    (function() {{
        for (var i = 0; i < 200; i++) {{
            fetch('https://gold-eagle-api.fly.dev/tap', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer {token}',
                    'Accept': 'application/json, text/plain, */*'
                }},
                body: JSON.stringify({{}})
            }}).catch(function(error) {{ console.error("Tap error:", error); }});
        }}
    }})();
    """
    driver.execute_script(batch_script)
    print(f"[+] Cycle {cycle}: Batch of 200 taps sent. Sleeping for 3 minutes...")
    time.sleep(180)  # Sleep for 3 minutes (180 seconds)

print("[+] Finished all cycles.")
driver.quit()
