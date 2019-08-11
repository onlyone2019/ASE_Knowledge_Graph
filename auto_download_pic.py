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
        element = self.driver.find_element_by_css_selector('[id="sbtc"] input')
        element.clear()
        element.send_keys(aircraft + '\n')

        sleep(2)
        try:
            pictures = self.driver.find_element_by_xpath('//*[@id="rg"]').find_elements_by_tag_name('img')
            for pic in pictures:
                image = Image.open(BytesIO(b64decode(pic.get_attribute('src').split(',')[-1].replace('%0A', '\n'))))
                pic_width, pic_height = image.size
                if pic_width / pic_height > 1.5:
                    image.save('%s.jpeg' % aircraft)
                    return 1
        except:
            return 0

    def quit(self):
        self.driver.quit()


if __name__ == "__main__":
    try:
        os.mkdir('aircraft_images')
    except:
        pass
    with open('客机型号.txt', 'r') as f:
        to_download = {i[:-1] for i in f.readlines()}   # 集合推导式，去除重复项和行尾换行符
    os.chdir('aircraft_images')
    already_exist = os.listdir()

    pic_spider = Pic_spider()
    pic_spider.startup()

    with open('../下载失败.txt', 'w') as f:
        f.write('下载失败：\n')
    for aircraft in to_download:
        if aircraft + '.jpeg' in already_exist:
            print(aircraft + '.jpeg already existed.')
            continue
        if not pic_spider.get_picture(aircraft):
            with open('../下载失败.txt', 'a') as f:
                f.write(aircraft + '\n')

    pic_spider.quit()
