from selenium import webdriver
from time import sleep

username = 'YOUR_USERNAME'
password = 'YOUR_PASSWORD'

driver = webdriver.Firefox()
driver.get("https://twitter.com/login")

def write(selector, message=None):
    if message:
        driver.find_element_by_css_selector(selector).send_keys(message)
    else:
        driver.find_element_by_css_selector(selector).click()

## wait for page to load
sleep(1)

#Send Username and Password
driver.find_element_by_name('session[username_or_email]').send_keys(username)
driver.find_element_by_name('session[password]').send_keys(password)

#login
write('[data-testid="LoginForm_Login_Button"]')

sleep(1)

write('[aria-label="Tweet"]')

sleep(1)

# Select the tweet box
write('.public-DraftStyleDefault-block')

# write
msg = "Example msg"
write('[aria-label="Tweet text"]', message=msg)

# send tweet
write('[data-testid="tweetButton"]')
