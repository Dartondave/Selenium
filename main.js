const { Builder, By } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const path = require('path');

(async function runHeadlessSelenium() {
  // Specify Chrome binary location
  let chromePath = '/usr/bin/google-chrome'; // Explicit Chrome path
  let options = new chrome.Options();
  options.setChromeBinaryPath(chromePath);  // Set binary path
  options.addArguments('--headless');       // Run headless mode
  options.addArguments('--no-sandbox');     // Required in some environments
  options.addArguments('--disable-dev-shm-usage'); // Overcome resource issues

  let driver = await new Builder()
    .forBrowser('chrome')
    .setChromeOptions(options)
    .build();

  try {
    // Your script logic
    await driver.get('https://telegram.geagle.online');
    console.log("Page loaded.");

    let response = await driver.executeScript(async () => {
      try {
        const res = await fetch("https://gold-eagle-api.fly.dev/tap", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer YOUR_TOKEN_HERE",
            "Origin": "https://telegram.geagle.online"
          },
          body: JSON.stringify({
            "exampleKey": "exampleValue"
          })
        });
        return await res.json();
      } catch (err) {
        return { error: err.toString() };
      }
    });

    console.log("Response from POST request:", JSON.stringify(response, null, 2));

  } catch (err) {
    console.error("An error occurred:", err);
  } finally {
    await driver.quit();
  }
})();