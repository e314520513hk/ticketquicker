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

checkCodeList = ["YES","A"]

expectedTicketAmount = "4"
expectedArea = ""
baseUrl = 'https://tixcraft.com/activity/detail/22_WuBaiOPR'

        

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
driver = webdriver.Chrome(options=options, service=s)
driver.set_window_size(1080, 768)
# driver.implicitly_wait(100)

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




while True:
    # 立即購票按鈕
    locator1 = (By.XPATH, '//*[@id="content"]/div/div/ul/li[1]/a/div')
    locator2 = (By.LINK_TEXT, '立即購票')
    locator3 = (By.XPATH, '//*[@id="gameList"]/table/tbody/tr/td[4]/input')

    try:
        WebDriverWait(driver, 600, 1).until(
            EC.presence_of_element_located(locator1))  # 最長等待10秒，每0.5秒檢查一次條件是否成立
        WebDriverWait(driver, 600, 1).until(
            EC.presence_of_element_located(locator2))  # 最長等待10秒，每0.5秒檢查一次條件是否成立
        print("已進入購票頁")
    except:
        print("逾時，未進入購票頁")

    print("開始購票1")
 
    while True:

        try:
            driver.find_element(
                By.XPATH, '//*[@id="content"]/div/div/ul/li[1]/a/div').click()

            sleep(0.5)

            driver.find_element(
                By.XPATH, '//*[@id="gameList"]/table/tbody/tr/td[4]/input').click()
            break
        except:
            continue

    print("選擇座位")
    print(driver.title)
    
    for y in range(2):
        
            if y == 0:
                print("y=0")
                areaList = driver.find_elements(
                    By.CSS_SELECTOR, 'div.zone.area-list > ul > li')
                print("areaList" + str(len(areaList)))
                if len(areaList)==0:
                    break
                if (len(areaList[0].text) > 50):        
                    break
                exit_flag = verify.verifySeat(areaList,expectedTicketAmount,expectedArea)

                print("y=0 ends")


            else:
                continue

            if exit_flag:
                break
        

    try:
        
        WebDriverWait(driver, 1, 0.2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.normal tr select')))
    except:
        #回答問題頁面  
        print(driver.title)
        print("回答問題頁面")

         
        if verify.verifyCheckCode(driver,checkCodeList):
            print("checkCode's passed")
        else:
            print("failed to verify checkCode")
            
    # 輸入驗證碼頁面   
    #  
    print(driver.title)    
    while True:    
        
        WebDriverWait(driver, 300, 0.2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.normal tr select')))    
        Select(driver.find_element(By.CSS_SELECTOR, '.normal tr select')
                    ).select_by_value(expectedTicketAmount)

        driver.find_element(By.XPATH, '//*[@id="TicketForm_agree"]').click()

        WebDriverWait(driver, 10, 0.2).until(
            EC.visibility_of_element_located((By.ID, 'TicketForm_verifyCode')))
        toElement = driver.find_element(By.ID, 'TicketForm_verifyCode').click()
    
        try:
            WebDriverWait(driver, 300, 0.2).until(
                EC.presence_of_element_located(locator1))  # 最長等待10秒，每0.5秒檢查一次條件是否成立
            WebDriverWait(driver, 300, 0.2).until(
                EC.presence_of_element_located(locator2))  # 最長等待10秒，每0.5秒檢查一次條件是否成立
        
            break    
        except Exception as e:
            
            print("驗證碼輸入錯誤: ")
            sleep(1.4)
            error_class = e.__class__.__name__ #取得錯誤類型
            detail = repr(e) #取得詳細內容
            cl, exc, tb = sys.exc_info() #取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
            fileName = lastCallStack[0] #取得發生的檔案名稱
            lineNum = lastCallStack[1] #取得發生的行號
            funcName = lastCallStack[2] #取得發生的函數名稱
            errMsg = "1File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
            print(errMsg)
            continue        

    continue