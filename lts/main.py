from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import os
import sys
import traceback
import configparser
from ticketholder import verify
import json
import time



def alert_is_present(driver):
    try:
        alert = driver.switch_to.alert
        alert.text
        return alert
    except:
        return False
checkCodeList = ["YES","A"]

expectedTicketAmount = "1"
expectedArea = ""
baseUrl = 'https://tixcraft.com/activity/detail/23_ssf4'

        

cf = configparser.ConfigParser()
cf.read("config.ini")



# secs = cf.sections()

# print(secs)
# options = cf.options("account_info")
# print(options)

# items =  cf.items("account_info")
# print(items)


s = Service(r"./chromedriver")
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.page_load_strategy = 'eager'
# options.add_argument('--headless')  # 啟動Headless 無頭
# options.add_argument('--disable-gpu') #關閉GPU 避免某些系統或是網頁出錯

# driver.set_window_size(1080, 768)
# driver.implicitly_wait(100)


driver = webdriver.Chrome(options=options, service=s)
driver.get(baseUrl)

# 動作:登入
with open(r"./lts/cookies_jar.json") as f:
    cookies = json.load(f)

driver.add_cookie(cookies[0])
driver.refresh()   
print("登入成功")
print(driver.title)

# 接受cookie政策
WebDriverWait(driver, 3, 0.5).until(EC.visibility_of_element_located(
    (By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()

redirectFlag = False ## 是否有跳轉頁面
currentPageTitle = False ## 當前頁面的Title



# 立即購票按鈕
locator1 = (By.XPATH, '//*[@id="content"]/div/div/ul/li[1]/a/div')
locator2 = (By.LINK_TEXT, '立即購票')
locator3 = (By.XPATH, '//*[@id="gameList"]/table/tbody/tr/td[4]/input')

while True:
        
    if redirectFlag and (driver.title == 'tixCraft拓元售票系統' or '節目資訊' in driver.title) or not redirectFlag:
        redirectFlag = False
        try:
            WebDriverWait(driver, 600, 0.1).until(
                EC.presence_of_element_located(locator1))  # 最長等待10秒，每0.5秒檢查一次條件是否成立
            WebDriverWait(driver, 600, 0.1).until(
                EC.presence_of_element_located(locator2))  # 最長等待10秒，每0.5秒檢查一次條件是否成立
            
    
        except Exception as e:
            print("逾時，未進入購票頁，reason: "+ type(e).__name__)
            if type(e).__name__ == "NoSuchWindowException":
                sys.exit(e)
            continue
        
        startTime = time.time()    
        #頁面:節目資訊
        currentPageTitle = driver.title
        while True:

            try:
                driver.find_element(
                    By.XPATH, '//*[@id="content"]/div/div/ul/li[1]/a/div').click()

                driver.find_element(
                    By.XPATH, '//*[@id="gameList"]/table/tbody/tr/td[4]/input').click()
                break
            except:
                continue

    if redirectFlag and ('區域' in driver.title) or not redirectFlag:
        redirectFlag = False       

        #頁面:區域
        currentPageTitle = driver.title
        currentUrl = driver.current_url
        while True:
            areaList = driver.find_elements(
                By.CSS_SELECTOR, 'div.zone.area-list > ul > li')
            print("length of areaList:" + str(len(areaList)) + " length of len(areaList[0].text):"+str(len(areaList[0].text)))
            if len(areaList)==0:
                break
            if (len(areaList[0].text) > 50):        
                break
            if verify.verifySeat(areaList,expectedTicketAmount,expectedArea):
                break
            driver.get(currentUrl)

        try: 
            
            WebDriverWait(driver, 1, 0.1).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.normal tr select')))
        except:
            #回答問題頁面  

            currentPageTitle = driver.title
            
            if verify.verifyCheckCode(driver,checkCodeList):
                print("checkCode's passed")
            else:
                print("failed to verify checkCode")
                
    if redirectFlag and ('票種' in driver.title) or not redirectFlag:
        redirectFlag = False 

        #頁面:票種
        
        currentPageTitle = driver.title   
        while True:    
            try:
                WebDriverWait(driver, 10, 0.1).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '.normal tr select')))    
                Select(driver.find_element(By.CSS_SELECTOR, '.normal tr select')
                            ).select_by_value(expectedTicketAmount)

                driver.find_element(By.XPATH, '//*[@id="TicketForm_agree"]').click()

                WebDriverWait(driver, 10, 0.1).until(
                    EC.visibility_of_element_located((By.ID, 'TicketForm_verifyCode')))
                toElement = driver.find_element(By.ID, 'TicketForm_verifyCode').click()
            
                endTime = time.time()
                print('程序执行时间: ',endTime - startTime)
                while True:
                    
                    if not driver.title == currentPageTitle:
                        
                        redirectFlag = True
                        break
                        
                    sleep(1)

            
                break    
            except Exception as e:
                alert_is_present(driver)
                print("錯誤類型: "+ type(e).__name__)
                if type(e).__name__ == 'NoSuchWindowException':
                    sys.exit("window already closed")
                if type(e).__name__ == 'UnexpectedAlertPresentException':
                    sleep(1.4)
                    continue
                    

    continue