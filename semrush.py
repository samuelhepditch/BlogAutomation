from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

CHROMEDRIVER_PATH = './chromedriver'

browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)

# Open the SEMrush dashboard
browser.get('https://www.semrush.com')

try:
    # Explicitly wait for the "Keyword Magic Tool" link to be clickable
    keyword_magic_tool = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, 'Keyword Magic Tool'))
    )
    keyword_magic_tool.click()
    
except Exception as e:
    print(f"An error occurred: {e}")

# Keep the browser open for 10 seconds (you can adjust the time as needed)
time.sleep(10)

browser.quit()

