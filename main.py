from selenium import webdriver
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
import time
import rgbmatrix

# Set up the Selenium webdriver
driver = webdriver.Chrome()
url = "https://www.panynj.gov/path/en/index.html"
driver.get(url)

# Wait for some time to let the page load
time.sleep(1)

# Get the page source after dynamic content has loaded
page_source = driver.page_source

# Close the browser
driver.quit()

# Use BeautifulSoup to parse the dynamically loaded content
soup = BeautifulSoup(page_source, 'html.parser')

# Find the div with "Grove Street" in it
grove_street_div = soup.find('div', string='Grove Street')

# Set up LED matrix panel (some of the attribute variables have different names than the CLI flags)
options = rgbmatrix.RGBMatrixOptions()
options.hardware_mapping = 'adafruit-hat' # also works for adafruit bonnet
options.rows = 32  # Set the number of rows to match your matrix
options.cols = 64  # Set the number of columns to match your matrix
options.gpio_slowdown = 4 # may be needed for raspberry pi 4 
options.chain_length = 1 # mayb be needed
options.parallel = 1 # may be needed
matrix = rgbmatrix.RGBMatrix(options=options)
font = ImageFont.load_default()
image = Image.new("RGB", (matrix.width, matrix.height), color=(0, 0, 0))
draw = ImageDraw.Draw(image)

if grove_street_div:
    next_train_div = grove_street_div.find_next('div', string='Next Train to NY')

    # Display the content on the LED matrix if found
    if next_train_div:
        siblings = next_train_div.find_next_siblings()
        text_to_display = ""
        for sibling in siblings:
            text_to_display += sibling.text + "\n"
        draw.text((2, 2), text_to_display, font=font, fill=(255, 255, 255))
        matrix.SetImage(image.convert("RGB"))
    else:
        draw.text((2, 2), "Path Train to NY not found.", font=font, fill=(255, 0, 0))
        matrix.SetImage(image.convert("RGB"))
else:
    draw.text((2, 2), "Grove Street div not found.", font=font, fill=(255, 0, 0))
    matrix.SetImage(image.convert("RGB"))

time.sleep(10)  # Display the information for 10 seconds

# Clear the LED matrix
matrix.Clear()