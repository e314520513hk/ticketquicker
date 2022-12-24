from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from PIL import Image
import requests
from PIL import Image
import shutil
import urllib
from time import sleep
from twocaptcha import TwoCaptcha
import sys
config = {
            #'server':           '2captcha.com',
            'apiKey':           '8b9085a582a46254e72ed6c3779f80db',
            # 'softId':            123,
            # 'callback':         'https://your.site/result-receiver',
            'defaultTimeout':    0.5,
            #'recaptchaTimeout':  600,
            #'pollingInterval':   10,
        }
solver = TwoCaptcha(**config)

def solve(image):
  result = False
  try:
    result = solver.normal(
      image
    )
  except Exception as e:
    print("exception")
    print(e)
    
  print("balance: " + str(solver.balance()))  
  print(result)
  return result


def report(captcha_id: str, success: bool):
  solver.report(captcha_id, success)

result1 = solve("captcha.png")
sys.exit()
try:
    assert login_message == "登入成功"
except AssertionError as e:
    report(result['captchaId'], False)


report(result['captchaId'], True)

s = Service(r"./chromedriver")
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.page_load_strategy = 'eager'


driver = webdriver.Chrome(options=options, service=s)
driver.get("https://medium.com/analytics-vidhya/python-selenium-all-mouse-actions-using-actionchains-197530cf75df")
sleep(2)
ele = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/div[2]/div/main/div/div[3]/div/div/article/div/div[2]/section/div/div[2]/figure[1]/div/div/picture/img')
print(ele.get_attribute("src"))
response = requests.get(ele.get_attribute("src"))
with  open("greenland_01.png","wb") as out_file:
    out_file.write(response.content)

# urllib.request.urlretrieve(ele.get_attribute("src"), "greenland_04a.png")