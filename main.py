from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
import time
import rgbmatrix
import subprocess # for running mp3 audio sound; pygame and other libraries have nice packages for playing audio
import os
os.environ['DISPLAY'] = ':0' # to avoid error when ssh
os.system("amixer set Master 30%")  # Linux way to set the audio

# Set up LED matrix panel (some of the attribute variables have different names than the CLI flags)
options = rgbmatrix.RGBMatrixOptions()
options.hardware_mapping = 'adafruit-hat' # also works for adafruit bonnet
options.rows = 32  # Set the number of rows to match your matrix
options.cols = 64  # Set the number of columns to match your matrix
options.gpio_slowdown = 4 # may be needed for raspberry pi 4 
options.chain_length = 1 # mayb be needed
options.parallel = 1 # may be needed
#options.brightness = 50
#options.limit_refresh_rate_hz = 30
matrix = rgbmatrix.RGBMatrix(options=options)
font = ImageFont.truetype("kongtext.ttf", 12)
image = Image.new("RGB", (matrix.width, matrix.height), color=(0, 0, 0))
draw = ImageDraw.Draw(image)


# load images
running_seq = []
for i in range(7):
    ping_img = Image.open(f"./run/{i}.png").convert("RGBA")
    ping_img = ping_img.transpose(Image.FLIP_LEFT_RIGHT)
    ping_img_with_black_bg = Image.new("RGBA", ping_img.size, (0,0,0,0))
    ping_img_with_black_bg.paste(ping_img, (0, 0), ping_img)
    running_seq.append(ping_img_with_black_bg)

# Set up the Selenium webdriver
#driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
url = "https://www.panynj.gov/path/en/index.html"
chrome_service = Service('/usr/lib/chromium-browser/chromedriver')
driver = webdriver.Chrome(service=chrome_service)

for _ in range(3):
    driver.get(url)
    # Wait for some time to let the page load
    time.sleep(2)

    # Get the page source after dynamic content has loaded
    page_source = driver.page_source

    # Close the browser
    #driver.quit()

    # Use BeautifulSoup to parse the dynamically loaded content
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find the div with "Grove Street" in it
    grove_street_div = soup.find('div', string='Grove Street')


    if grove_street_div:
        next_train_div = grove_street_div.find_next('div', string='Next Train to NY')

        if next_train_div:
            siblings = next_train_div.find_next_siblings()
            text_to_display = ""
            text_color = (155, 255, 55)
            for sibling in siblings:
                for i, val in enumerate(sibling.text[-8:]):
                    if val.isdigit():
                        index = len(sibling.text)-8 + i
                        break
                text_to_display += " " + sibling.text[:index] + " " + sibling.text[index:] + "\n"
        else:
            text_to_display = "Path Train to NY not found."
            text_color = (255, 0, 0)
    else:
        text_to_display = "Grove Street div not found."
        text_color = (255, 0, 0)

    try:
        subprocess.Popen(["cvlc", "-d", "transition.mp3"])
    except Exception as e:
        print(f"Error playing sound: {e}")

    for _ in range(3):
        for i in range(550):
             draw.rectangle((0, 0, 1000, 1000), fill=(0,0,0,0))
             time.sleep(0.015)
             image.paste(running_seq[(i//10)%7], (-i + 150, 2))
             draw.text((-i + 150 + 20, 2), text_to_display, font=font, fill=text_color)
             matrix.SetImage(image.convert("RGB"))

# Clear the LED matrix
matrix.Clear()
