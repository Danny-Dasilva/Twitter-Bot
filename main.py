

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

username = 'YOUR USERNAME'
password = 'YOUR PASSWORD'

driver = webdriver.Firefox()
driver.get("https://twitter.com/login")

## Login
time.sleep(1)
driver.find_element_by_name('session[username_or_email]').send_keys(username)


#BSend Username and Password
driver.find_element_by_name('session[password]').send_keys(password)
driver.find_element_by_css_selector('[data-testid="LoginForm_Login_Button"]').click()


time.sleep(1)
driver.find_element_by_css_selector('[aria-label="Tweet"]').click()


time.sleep(1)

# Select the tweet box
el = driver.find_element_by_css_selector('.public-DraftStyleDefault-block')
# not sure if you need to double click
el.click()
el.click()

# write
msg = "Example msg"
driver.find_element_by_css_selector('[aria-label="Tweet text"]').send_keys("Example msg")

# send tweet
driver.find_element_by_css_selector('[data-testid="tweetButton"]').click()
