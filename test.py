import json
import os
import time
from socket import timeout
from telnetlib import EC

import fitz
import pyautogui as pyautogui
from PIL.Image import SEQUENCE
from selenium import webdriver

# setting html path
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

import json
from selenium import webdriver
import json
from selenium.webdriver.chrome.options import Options
import keyboard, time

chrome_options = webdriver.ChromeOptions()
settings = {
       "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": "",
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2,

    }



prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings),
         'savefile.default_directory': '/Users/gregreynders/PycharmProjects/Webscrapper'}
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument('--kiosk-printing')


driver = webdriver.Chrome(chrome_options=chrome_options , executable_path="/Applications/chrome/chromedriver" )
driver.get("https://www.zalando.be/heren/tommy-hilfiger-online-shop/?shipped_by_zalando=true")



pyautogui.hotkey('command', 's')
time.sleep(1)
pyautogui.hotkey('enter')
time.sleep(1)


pdf_file = fitz.open(f'tommy-hilfiger Herenartikelen • ZALANDO • Alles voor mannen online.pdf')
imgs = []
for pdfpagenumber, page in enumerate(pdf_file.pages(), start=1):
    for imgNumber, img in enumerate(page.getImageList(), start=1):
        xref = img[0]
        pix = fitz.Pixmap(pdf_file, xref)
        if pix.n > 4:
            pix = fitz.Pixmap(fitz.csRGB, pix)
        pix.writePNG(f'image/{pdfpagenumber}_{imgNumber}.png')
        imgs.append(f'{pdfpagenumber}_{imgNumber}.png')



