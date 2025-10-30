from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

print("🧠 Detecting Chrome version...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
print("✅ Chrome opened successfully")
driver.quit()

