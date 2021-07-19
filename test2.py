from selenium import webdriver
import urllib.request
import urllib
import os

class ChromefoxTest:
    def __init__(self,url):
        self.url=url
        self.uri = []
        self.folder = '/Users/gregreynders/PycharmProjects/Webscrapper/images'
        self.chrome_options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options, executable_path="/Applications/chrome/chromedriver")
        self.driver.get(self.url)
    def chromeTest(self):
        self.r=self.driver.find_elements_by_tag_name('img')
        for v in self.r:
            src = v.get_attribute("src")
            if(len(src)<150):
             self.uri.append(src)
             pos = len(src) - src[::-1].index('/')
             print(src[pos:])
             self.g=urllib.request.urlretrieve(src, "/".join([self.folder, src[pos:]]))
        self.driver.quit()
    def navigate(self):
        self.article =self.driver.find_elements_by_tag_name('article')
        for tag in self.article:
            self.anchor = tag.find_elements_by_tag_name("a")
            for href in self.anchor:
                print(href.get_attribute("href"))
            self.figure = tag.find_elements_by_tag_name("figure")
            for figure in self.figure:
                self.figure = figure.find_elements_by_tag_name("figure")


if __name__=='__main__':
    FT=ChromefoxTest("https://www.zalando.be/heren/tommy-hilfiger-online-shop/?shipped_by_zalando=true")
    #FT.chromeTest()
    FT.navigate()
    i = 0


