from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def semrush_login():
    driver = webdriver.Firefox()
    driver.get("https://www.semrush.com/")

    try:

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Log In"))
        )
        login_button.click()

        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_input.send_keys("hepditchsam@gmail.com")

        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys("Dog$tar22")

        input("Please complete the CAPTCHA and click the login button. Press Enter when done...")

        keyword_magic_tool_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Keyword Magic Tool"))
        )
        keyword_magic_tool_link.click()
    

    except Exception as e:
        print("Error encountered:", e)

    while True:
        user_input = input("Type 'q' to quit the browser: ")
        if user_input.lower() == 'q':
            driver.quit()
            break

def gpt_keyword_idea_generation():
    return


if __name__ == "__main__":
    semrush_login()
    gpt_keyword_idea_generation()


