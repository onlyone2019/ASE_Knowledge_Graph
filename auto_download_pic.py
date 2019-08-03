# -*- coding: utf-8 -*-
# 需要 chromedriver、chrome 浏览器、Ghelper 浏览器插件

from selenium import webdriver
from PIL import Image
from time import sleep
from base64 import b64decode
from io import BytesIO
import os


class Pic_spider:
    def __init__(self):
        self.BASE_URL = "https://www.google.com"
        self.option = webdriver.ChromeOptions()
        self.option.add_argument("--user-data-dir=" + r"/home/marsvet/.config/google-chrome/")

    def startup(self):
        self.driver = webdriver.Chrome(chrome_options=self.option)
        self.driver.get(self.BASE_URL + '/imghp?hl=zh-CN/')

    def get_picture(self, aircraft):
        sleep(2)
        element = self.driver.find_element_by_xpath('//*[@id="sbtc"]/div/div[1]/input')
        element.clear()
        element.send_keys(aircraft + '\n')

        sleep(2)
        try:
            pictures = self.driver.find_element_by_xpath('//*[@id="rg"]').find_elements_by_tag_name('img')
        except:
            return 0
        for pic in pictures:
            image = Image.open(BytesIO(b64decode(pic.get_attribute('src').split(',')[-1].replace('%0A', '\n'))))
            pic_width, pic_height = image.size
            if pic_width / pic_height > 1.5:
                image.save('%s.jpeg' % aircraft)
                return 1

        return 0

    def quit(self):
        self.driver.quit()


if __name__ == "__main__":
    try:
        os.mkdir('images')
    except:
        pass
    with open('客机型号.txt', 'r') as f:
        to_download = set(f.readlines())
    download_fail = []
    os.chdir('images')

    pic_spider = Pic_spider()
    pic_spider.startup()

    for aircraft in to_download:
        if not pic_spider.get_picture(aircraft):
            download_fail.append(aircraft)

    pic_spider.quit()

    print('\n下载失败：')
    for i in download_fail:
        print(i + '\n')
