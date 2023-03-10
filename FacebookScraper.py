from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re

# get Facebook email and password from a text file
with open('credentials.txt', 'r') as f:
    fb_email = f.readline().strip()
    fb_password = f.readline().strip()

# get search query from a text file
with open('search_query.txt', 'r') as f:
    search_query = f.readline().strip()

# set the maximum number of emails to extract
MAX_EMAILS = 1000

# open Facebook in Chrome browser
browser = webdriver.Chrome()
browser.get('https://www.facebook.com')

# login to Facebook
email_field = browser.find_element_by_id('email')
email_field.send_keys(fb_email)
password_field = browser.find_element_by_id('pass')
password_field.send_keys(fb_password)
password_field.send_keys(Keys.RETURN)

time.sleep(5) # wait for the page to load

# search for the query
search_field = browser.find_element_by_name('q')
search_field.send_keys(search_query)
search_field.send_keys(Keys.RETURN)

time.sleep(5) # wait for the search results to load

# extract the email addresses from the search results
email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
search_results = browser.find_elements_by_xpath("//div[@class='ecm0bbzt e5nlhep0 a8c37x1j']/div")

email_count = 0
emails = set()

for result in search_results:
    text = result.text
    new_emails = re.findall(email_regex, text)
    for email in new_emails:
        if email_count >= MAX_EMAILS:
            break
        if email not in emails:
            emails.add(email)
            print(email)
            email_count += 1
    
    if email_count >= MAX_EMAILS:
        break

# write the extracted emails to a text file
with open('extracted_emails.txt', 'w') as f:
    for email in emails:
        f.write(email + '\n')

browser.quit() # close the browser
