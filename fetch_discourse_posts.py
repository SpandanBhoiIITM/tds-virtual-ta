import json
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

SAVE_PATH = "data/discourse_posts.json"
BASE_URL = "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34"

chromedriver_autoinstaller.install()
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

driver.get(BASE_URL)
input("Login in the browser. Then press ENTER here...")

posts = []
topics = driver.find_elements(By.CSS_SELECTOR, "tr.topic-list-item")

for topic in topics:
    try:
        title_elem = topic.find_element(By.CSS_SELECTOR, "a.title")
        title = title_elem.text
        url = title_elem.get_attribute("href")

        # Go to post URL and extract content
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(url)
        time.sleep(2)

        # First post content
        post_content_elem = driver.find_element(By.CSS_SELECTOR, ".cooked")
        content = post_content_elem.text

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        posts.append({"title": title, "url": url, "content": content})
    except Exception as e:
        print("Error:", e)
        continue

driver.quit()

os.makedirs("data", exist_ok=True)
with open(SAVE_PATH, "w", encoding="utf-8") as f:
    json.dump(posts, f, indent=2, ensure_ascii=False)

print(f"✅ Saved {len(posts)} posts to {SAVE_PATH}")
