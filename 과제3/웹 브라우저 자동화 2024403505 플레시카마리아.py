from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

try:
    driver.get('https://www.youtube.com/')

    search_field = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input#search'))
    )
    search_field.send_keys('Never Gonna Give You Up')
    search_field.send_keys(Keys.RETURN)
    
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a#video-title'))
    )

    video = driver.find_element(By.CSS_SELECTOR, 'a#video-title')
    video.click()

finally:
    print("Video is playing.")
