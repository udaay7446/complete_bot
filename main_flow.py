import glob
import os
import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from email_utils import MailBox

Download_path = os.path.join(os.getcwd(), 'download')
email_id = "udaay7446@outlook.com"
password = "Aruna@270895"


def delete_all_files(download_path):
    try:
        files = glob.glob(download_path + "/*")
        if len(files) > 0:
            for i in files:
                try:
                    os.remove(i)
                except Exception as e:
                    pass
    except Exception as e:
        pass


delete_all_files(download_path=Download_path)
mailbox_obj = MailBox(email_id, password)
latest_mail = mailbox_obj.get_latest_mail(subject="This is test mail")
print(latest_mail)
options = webdriver.ChromeOptions()

options.add_argument('--disable-infobars')
options.add_argument('--start-fullscreen')
options.add_argument("--incognito")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
# options.add_argument("headless")
options.add_argument("--disable-extensions")
options.add_argument("--disable-browser-side-navigation")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
wait = WebDriverWait(driver, 30)


def close_driver(driver):
    time.sleep(5)
    driver.delete_all_cookies()
    driver.close()


driver.get("https://www.google.com/search?q=cat+images")
close_driver(driver)


