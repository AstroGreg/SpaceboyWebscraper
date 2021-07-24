import hashlib

from selenium import webdriver
import urllib.request
import urllib
import os
from deepface import DeepFace
import cv2
import urllib.request
import re
from webdriver_manager.chrome import ChromeDriverManager


class ChromefoxTest:
    def __init__(self, url, nameoffolder , paging, max=None):
        self.paging = paging
        self.previeuspage = None
        self.url = url
        self.chrome_options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.matchedfotos = 1
        self.fotos = 1
        self.page = 1
        self.max = max
        self.folder = nameoffolder
        self.driver.get(self.url)
        if not os.path.isdir(nameoffolder):
            os.makedirs(nameoffolder)

    def getfotofromlink(self, imglink):
        if len(imglink) < 150:
            end = re.search("(\.[A-Za-z]+)\?", imglink)
            if end is not None:
                pos = "/".join([self.folder, f"image{self.fotos}" + end.group(1)])
                urllib.request.urlretrieve(imglink, pos)
                gezichtsherkent = self.gezichsherkening(pos)
                self.fotos += 1
                return gezichtsherkent, pos
            return None, None
    def start(self):
     while(True):
      if self.paging:
        self.page += 1
        match = re.sub("p=[d]+", f"p={self.page}", self.url)
        if(match == self.url): match = f'{self.url}&p={self.page}'
        self.url = match
        self.driver.get(self.url)
        self.currentpage = self.driver.current_url
        if self.previeuspage == self.currentpage or self.page == self.max:
            return
        else:
            self.previeuspage = self.driver.current_url
            self.navigate()
      else:
         self.navigate()
         return
    def navigate(self):
        revisit = []
        self.article = self.driver.find_elements_by_tag_name('article')
        for i, tag in enumerate(self.article):
            self.figure = tag.find_element_by_tag_name("figure")
            gezichtherkent, pos = self.getfotofromlink(self.figure.find_element_by_tag_name("img").get_attribute("src"))
            if gezichtherkent:
                pos = self.foundmatch(pos)
            elif gezichtherkent is False:
                os.remove(pos)
            if gezichtherkent or gezichtherkent is None:
                self.anchor = tag.find_element_by_tag_name("a")
                revisit.append((self.anchor.get_attribute("href"), pos, gezichtherkent))
            if i == 5:
                break
        for link in revisit:
                self.navigatearticle(link[0], link[1], link[2])

    def navigatearticle(self, artcilelink, pos1, alreadymatched):
        self.driver.get(artcilelink)
        self.div = self.driver.find_element_by_xpath(
            "//ul[@class='XLgdq7 _0xLoFW JgpeIw r9BRio be4rWJ N2nrLi _4oK5GO heWLCX _MmCDa']")
        listtag = self.div.find_elements_by_tag_name("li")
        savedfotos = [pos1]
        for i in range(0, 2):
                self.driver.implicitly_wait(1)
                url = listtag[i].find_element_by_tag_name('img').get_attribute("src")
                gezichtherkent, pos2 = self.getfotofromlink(url)
                newname = pos1.split(".")
                newname[0] = f'{newname[0]}_{i + 1}'
                newname = ".".join(newname)
                os.rename(pos2, newname)
                savedfotos.append(newname)
                if gezichtherkent:
                    alreadymatched = True
        if not alreadymatched:
            for foto in savedfotos:
                os.remove(foto)

    def foundmatch(self, pos):
        parts = pos.split(".")
        newname = f'{self.folder}/match{self.matchedfotos}.' + parts[len(parts) - 1]
        os.rename(pos, newname)
        self.matchedfotos += 1
        return newname

    def gezichsherkening(self, image):
        img1 = cv2.imread(image)
        if img1 is not None:
            for filename in os.listdir("match"):
                img2 = cv2.imread(f"match/{filename}")
                try:  analise = DeepFace.verify(img1, img2, model_name="Dlib")
                except: return None
                print(analise)
                if analise is not None and analise["distance"] < 0.05:
                    return True
        return False

    def stop(self):
        self.driver.quit()


if __name__ == '__main__':
    FT = ChromefoxTest("https://www.zalando.be/heren/tommy-hilfiger-online-shop/?shipped_by_zalando=true",
                       input("name of folder\n"), True)
    FT.start()
    FT.stop()
    i = 0
