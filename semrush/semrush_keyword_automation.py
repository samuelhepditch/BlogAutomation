from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from blog_keyword import Keyword, KeywordsList
from enum import Enum
import time
import os
import shutil

class Keyword:
    def __init__(self, keyword_difficulty, cost_per_click, results):
        self.keyword_difficulty = keyword_difficulty
        self.cost_per_click = cost_per_click
        self.results = results

    def __str__(self):
        return (f"Keyword Info:\n"
                f"Keyword Difficulty: {self.keyword_difficulty}\n"
                f"Cost Per Click: {self.cost_per_click}\n"
                f"Results: {self.results}")  


class SEMrushFilters(Enum):
    VERY_EASY = "H4sIAAAAAAAAA32PywrDIBBF%2F2XWLlJIN%2F5KCCI6WmGi4quUkn%2BvqSWrkt08zszhvkGFLWJxxQUvCBsS8GVloKIahXbGOFWpvHr%2FBucbpoIauJGUkUGImORxDfzOoEmqCHza2TU6n%2Bht3rvF%2BYK%2B5P%2BK82kHSXpbpcVLEtBbOOj4SDLjCDJq4byiqlFQsK5HnBgkzD1eHlTGFIVBWWofX0qW9TC0QHX7GZ4h6SxUqL581x96aIV6XQEAAA%3D%3D"
    EASY = "H4sIAAAAAAAAA32PSwrDMAwF76K1F21pFs1VQjDGkV2BYht%2FUkrI3evUoauS3ZM0YngraD8HzJTJO8m4IEM%2FjAJ00C1MZAzpwvld5xXILRgzTtAbxQkF%2BIBR7d%2FQdwIWxQWhv3abOGfvP%2Fb22KqGXEaX03%2FHQV52kJWzRVk8JQGdhZ0Oz6gStiYtS3Kay4SSvaXa8SIgYqr9UqMSxiANqlzq%2BlQyjLth8Vzmw%2FDycUpS%2B%2BLy9%2FwBezauEl4BAAA%3D"

def semrush_login(driver):
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

    except Exception as e:
        print("Error encountered:", e)


def check_for_results(driver):
    time.sleep(10)
    try:
        results = driver.find_elements(By.CSS_SELECTOR, 'div[data-test="table-row"]')
        return len(results) > 0
    except NoSuchElementException:
        return False

    
def convert_csv_to_filtered_keyword_list(driver):
    # input("Please export the keywords csv and position in csv folder. Press Enter when done...")

    ## This will download the CSV
    driver.find_element(By.CSS_SELECTOR, ".\\_theme_default_vw9c8-kmt_ > .\\___SButton_brxh6-kmt_ .\\___SIcon_1kytx-kmt_").click()
    driver.find_element(By.CSS_SELECTOR, ".kwo-one-line-layout__item:nth-child(2) > .\\___SButton_brxh6-kmt_ .\\_size_m_brxh6-kmt_").click()

    # This will move that downloaded csv to the ./csv folder
    # Path to your downloads folder
    source_dir = "D:\Downloads"

    # Path to your destination folder (current directory's .csv folder)
    dest_dir = os.path.join(os.getcwd(), "csv")

        # List all files in the downloads directory
    all_files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]

    # Filter out only .csv files
    csv_files = [f for f in all_files if f.endswith('.csv')]

    # Find the most recent .csv file based on modification time
    if csv_files:
        newest_csv = max(csv_files, key=lambda f: os.path.getmtime(os.path.join(source_dir, f)))

        # Move the most recent .csv file to the destination directory
        shutil.move(os.path.join(source_dir, newest_csv), os.path.join(dest_dir, newest_csv))
        print(f"Moved {newest_csv} to {dest_dir}")
    else:
        print("No .csv files found in the specified directory.")

    keyword_difficulty = int(input("Maximum keyword difficulty: "))
    query_number =  int(input("Minimum number of monthly queries: "))
    cost_per_click = float(input("Minimum cost-per-click: "))
    
    keywords = KeywordsList(newest_csv)
    keywords.filter_keywords(keyword_difficulty, query_number, cost_per_click)  

    for keyword in keywords:
        print(keyword)



def setup_keyword_magic_tool(driver, filter_type):
    base_url = "https://www.semrush.com/analytics/keywordmagic/"

    filter_value = SEMrushFilters[filter_type].value
    url_template = f"{base_url}?q={{keyword}}&db=ca&filter={filter_value}&currency=cad"
    
    input_str = input("Enter a list of comma separated keywords: ")

    keywords = [x.strip() for x in input_str.split(",")]

    for keyword in keywords:
        keyword_url = url_template.format(keyword=keyword)
        driver.get(keyword_url)
            


if __name__ == "__main__":
    driver = webdriver.Firefox()
    semrush_login(driver)
    setup_keyword_magic_tool(driver, filter_type='VERY_EASY')
    if check_for_results(driver):
        convert_csv_to_filtered_keyword_list(driver)
    else:
        print("No results found.")
