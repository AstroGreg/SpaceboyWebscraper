import urllib.request

from bs4 import BeautifulSoup
from deepface import DeepFace
import sys
import httplib2
import pdfkit
import fitz
import cv2
import re
import os
from selenium import webdriver
import urllib.request
import urllib
import os


class ChromefoxTest:
    def __init__(self, url, location):
        self.url = url
        self.uri = []
        self.folder = f'/Users/gregreynders/PycharmProjects/Webscrapper/{location}'

    def chromeTest(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options,
                                       executable_path="/Applications/chrome/chromedriver")
        self.driver.get(self.url)
        self.r = self.driver.find_elements_by_tag_name('img')
        for v in self.r:
            src = v.get_attribute("src")
            if (len(src) < 150):
                self.uri.append(src)
                pos = len(src) - src[::-1].index('/')
                print(src[pos:])
                self.g = urllib.request.urlretrieve(src, "/".join([self.folder, src[pos:]]))
        self.driver.quit()


def gezichsherkening(image):
    img1 = cv2.imread(image)
    results = []
    if img1 is not None:
        for filename in os.listdir("match"):
            img2 = cv2.imread(f"match/{filename}")
            try:
                analise = DeepFace.verify(img1, img2, model_name="Dlib")
            except:
                break
            print(analise)
            if analise is not None:
                results.append(analise["distance"] < 0.04)
    return True in results


def zalando():
    location = input("location")
    if not os.path.isdir(location):
        os.makedirs(location)
    brand = input("Which brand, notice that the spelling has to be the same "
                  "as it is in the browser. Suggestions are "
                  "\ntommy-hilfiger\nalpha-industries\n")

    print(f"searching: https://www.zalando.be/heren/{brand}")
    FT = ChromefoxTest(f"https://www.zalando.be/heren/{brand}", location)
    FT.chromeTest()
    imagenumber = 0
    for file in os.listdir(location):
        imagenumber += 1
        filename = os.fsdecode(file)
        os.path.join(location, filename)
        if (gezichsherkening(f'{location}/{filename}')):
            os.rename(f'{location}/{filename}', f'{location}/image{imagenumber}' + ".jpg")
        else:
            os.remove(f'{location}/{filename}')


if __name__ == '__main__':
    avaialblesites = {"zalando": zalando()}
    site = input("site")
    if site.lower() in avaialblesites:
        avaialblesites[site.lower()]
    else:
        print("seems like Greg hasn't implemented this site yet")
