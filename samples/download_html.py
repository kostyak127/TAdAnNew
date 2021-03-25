from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys

options = Options()
options.headless = True
options.binary_location = r"C:\Program Files\Google\Chrome Beta\Application\chrome.exe"
driver = webdriver.Chrome(options=options,
                          executable_path=r'C:\Users\1\PycharmProjects\TAdAnNew\samples\chromedriver.exe')
driver.get("https://t.me/s/novostyrus")
print("Headless Chrome Initialized")

messages = driver.find_elements_by_class_name('tgme_channel_history.js-message_history')

print(len(messages))
driver.quit()