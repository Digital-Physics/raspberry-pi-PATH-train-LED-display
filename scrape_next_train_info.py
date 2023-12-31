from selenium import webdriver
from bs4 import BeautifulSoup
import time


# Set up the Selenium webdriver; You may need to download the appropriate webdriver for your browser
# We use this to act like a human user that loads the webpage, because the train information on the site is dynamically loaded
driver = webdriver.Chrome()  

# Load the webpage
url = "https://www.panynj.gov/path/en/index.html"
driver.get(url)

# Wait for some time to let the page load
time.sleep(1)

# Now, get the page source after dynamic content has loaded
page_source = driver.page_source

# Close the browser
driver.quit()

# Now, use BeautifulSoup to parse the dynamically loaded content
soup = BeautifulSoup(page_source, 'html.parser')

# Find the div with "Grove Street" in it
grove_street_div = soup.find('div', string='Grove Street')

if grove_street_div:
    next_train_div = grove_street_div.find_next('div', string='Next Train to NY')

    # Print the content if found
    if next_train_div:
        # Print all the siblings
        siblings = next_train_div.find_next_siblings()
        for sibling in siblings:
            print(sibling.text)
    else:
        print("Path Train to NY not found.")
else:
    print("Grove Street div not found.")