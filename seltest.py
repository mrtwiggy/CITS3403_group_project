from selenium import webdriver

# For Chrome
driver = webdriver.Chrome()
driver.get("http://www.google.com")
print(driver.title)
driver.quit()