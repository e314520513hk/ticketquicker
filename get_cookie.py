from selenium import webdriver
from time import sleep
import json
import sys

if __name__ == '__main__':
    with open("cookies_jar.json") as f:
        cookies = json.load(f)

    driver = webdriver.Chrome()
    driver.get('https://tixcraft.com/')    
    print("type:"+str(type(cookies))+"value:" + str(cookies))
    driver.add_cookie(cookies[0])
    
    driver.refresh()

    sleep(300)