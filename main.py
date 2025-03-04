import time
import json
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def main():
    # 1) Basic Selenium setup
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Kiwi/5.0 Chrome/87.0.4280.141 Mobile Safari/537.36"
    )
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 2) (Optional) If you need to attach an authorization header to every request:
    token = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7ImlkIjoiYzA5YTE2MGMtNTFmMC00MjdiLTkxMzktNGQwZDdmYWNhMWU5IiwiZmlyc3RfbmFtZSI6IuawlERBUlRPTuS5iCIsImxhbmd1YWdlX2NvZGUiOiJlbiIsInVzZXJuYW1lIjoiRGFydG9uVFYifSwic2Vzc2lvbl9pZCI6MTQzNzI1NCwic3ViIjoiYzA5YTE2MGMtNTFmMC00MjdiLTkxMzktNGQwZDdmYWNhMWU5IiwiZXhwIjoxNzQyOTc4MjUzfQ.f_0ScBVxthVpykNsiFI-QCqxDxhaxioVqq3PXtyG_Iw"
    def interceptor(request):
        request.headers['authorization'] = f"Bearer {token}"
    driver.request_interceptor = interceptor

    # 3) Navigate to the mini‑app UI (replace URL with your referral or known working URL)
    driver.get("https://t.me/gold_eagle_coin_bot/main?startapp=r_gTGFKMkFC5")
    time.sleep(5)

    # 4) (Optional) Inject Telegram initParams, external JS, etc. if needed
    # driver.execute_script(...)
    # time.sleep(...)

    try:
        # 5) Locate the tap area container by class name or partial style.
        #    Here we use a direct class selector. If the class name changes frequently,
        #    try a partial match like: div[class^="tapAreaContainer_"] or
        #    search by the background style: [style*="gold-eagle-coin.svg"].
        tap_area = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div.tapAreaContainer_njdmz_15")
            )
        )
        print("[+] Coin container element found.")

        # 6) Simulate repeated taps on the element
        tap_count = 200
        for i in range(tap_count):
            driver.execute_script("arguments[0].click();", tap_area)
            # If you need a slight delay between taps, uncomment below:
            # time.sleep(0.05)
        print(f"[+] Simulated {tap_count} taps on the coin container.")

    except Exception as e:
        print("[-] Could not find or tap the coin container:", e)
        driver.get_screenshot_as_file("debug_coin.png")
        print("Screenshot saved as debug_coin.png")
        print(driver.page_source[:2000])
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
