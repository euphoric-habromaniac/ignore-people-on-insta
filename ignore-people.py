import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

load_dotenv()

username = os.getenv('INSTAGRAM_USERNAME')
password = os.getenv('INSTAGRAM_PASSWORD')
retain_people = os.getenv('RETAIN_PEOPLE').split(',')

driver = webdriver.Chrome(executable_path='/path/to/chromedriver')

def login_instagram(username, password):
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(3)

    driver.find_element(By.NAME, 'username').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys(password)

    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div').click()
    time.sleep(5)

def navigate_to_inbox():
    driver.get('https://www.instagram.com/direct/inbox/')
    time.sleep(5)

def delete_unwanted_messages():
    message_threads = driver.find_elements(By.XPATH, '//div[@role="dialog"]//div[contains(@class, "QBdPU")]')

    for thread in message_threads:
        user = thread.find_element(By.XPATH, './/span[@class="_7UhW9"]').text

        if user not in retain_people:
            print(f"Deleting message from {user}")
            thread.click()
            time.sleep(2)

            driver.find_element(By.XPATH, '//button[contains(@aria-label, "Options")]').click()
            time.sleep(1)

            delete_button = driver.find_element(By.XPATH, '//button[text()="Delete Chat"]')
            delete_button.click()
            time.sleep(2)

if __name__ == "__main__":
    try:
        login_instagram(username, password)
        navigate_to_inbox()
        delete_unwanted_messages()
    finally:
        driver.quit()
