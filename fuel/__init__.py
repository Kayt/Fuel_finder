from selenium import webdriver

driver = webdriver.Chrome()                     # Needs to be global for all classes to use
driver.get('https://web.whatsapp.com')