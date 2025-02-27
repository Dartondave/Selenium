const { Builder, By } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');

(async function runHeadlessSelenium() {
  // Configure Chrome options for headless mode.
  let options = new chrome.Options();
  options.addArguments('--headless');               // Run Chrome in headless mode.
  options.addArguments('--no-sandbox');             // Required in some environments like CI.
  options.addArguments('--disable-dev-shm-usage');  // Overcome limited resource problems.

  // Initialize the WebDriver.
  let driver = await new Builder()
    .forBrowser('chrome')
    .setChromeOptions(options)
    .build();

  try {
    // Navigate to the origin page to satisfy CORS.
    await driver.get('https://telegram.geagle.online');
    console.log("Origin page loaded successfully.");

    // Execute the JavaScript fetch request to perform the POST request.
    let response = await driver.executeScript(async () => {
      try {
        const res = await fetch("https://gold-eagle-api.fly.dev/tap", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7ImlkIjoiYzA5YTE2MGMtNTFmMC00MjdiLTkxM>",
            "Origin": "https://telegram.geagle.online"
          },
          body: JSON.stringify({
            "exampleKey": "exampleValue"
          })
        });

        const data = await res.json();
        return { status: res.status, data: data };
      } catch (error) {
        return { error: error.toString() };
      }
    });

    // Log the response.
    console.log("Response from POST request:", JSON.stringify(response, null, 2));

  } catch (err) {
    console.log("An error occurred:", err);
  } finally {
    // Close the WebDriver instance.
    await driver.quit();
  }
})();