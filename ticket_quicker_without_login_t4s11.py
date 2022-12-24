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
checkCodeList = ["YES","A"]
expectedTicketAmount = "4"

def verifySeat(ticketList):
    try:
        exit_flag = False
        for x in range(len(ticketList)):

            print("condition "+str(y)+" string length i scraped : " +
                    str(len(ticketList[x].text)) + "  : " +ticketList[x].text)
            if (len(ticketList[x].text) > 50):
                print("門票描述字串過長，系統判定html結構與系統所認知的不符，因此跳到condition "+str(y+1))
                break
            if "熱賣中" in ticketList[x].text:
                print("熱賣中")
                ticketList[x].click()
                exit_flag = True

            elif "剩餘" in ticketList[x].text:
                splitedTicketName = ticketList[x].text.split()
                remainAmount = len(splitedTicketName)
                print(
                    "condition  "+str(y)+" : "+ticketList[x].text + "門票剩餘"+splitedTicketName[remainAmount-1])

                if int(expectedTicketAmount) <= int(splitedTicketName[remainAmount-1]):
                    ticketList[x].click()
                    exit_flag = True

                else:
                    continue
            else:
                print(ticketList[x].text + "沒票")
                continue

            if exit_flag:
                print("exit_flag is true")
                break
        print("Seat's finished to choose")
        return exit_flag
    except:
        print("error occured during seat's choosing")
        return exit_flag    
    
  

def verifyCheckCode(driver):
    try:

        for x in range(len(checkCodeList)):
            print("check_code : " + checkCodeList[x])

            ## clear textbox
            WebDriverWait(driver, 1, 0.6).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#checkCode')))
            driver.find_element(By.CSS_SELECTOR, '#checkCode').clear()

            ## put text in textbox
            WebDriverWait(driver, 1, 0.6).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#checkCode')))
            driver.find_element(By.CSS_SELECTOR, '#checkCode').send_keys(checkCodeList[x]) 

            ## submit
            WebDriverWait(driver, 10, 0.6).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#submitButton')))
            driver.find_element(By.CSS_SELECTOR, '#submitButton').click()

            sleep(0.7)
            print("message of pop-up: "+ driver.switch_to.alert.text)
            if "您所輸入的驗證碼不正確" in driver.switch_to.alert.text:
                driver.switch_to.alert.accept()
                continue

            driver.switch_to.alert.accept()
        return True

    except:
        return False
        

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

driver.get('https://tixcraft.com/')

print(driver.title)

WebDriverWait(driver, 10, 0.6).until(EC.visibility_of_element_located(
    (By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()


# 動作:登入
# WebDriverWait(driver, 10, 0.6).until(EC.visibility_of_element_located(
#     (By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/ul/li[3]/a')))
# driver.find_element(
#     By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/ul/li[3]/a').click()
# WebDriverWait(driver, 10, 0.6).until(
#     EC.visibility_of_element_located((By.XPATH, '//*[@id="loginFacebook"]')))
# driver.find_element(By.XPATH, '//*[@id="loginFacebook"]').click()
# WebDriverWait(driver, 10, 0.6).until(
#     EC.visibility_of_element_located((By.XPATH, '//*[@id="email"]')))
# driver.find_element(
#     By.XPATH, '//*[@id="email"]').send_keys(fb["account"])
# WebDriverWait(driver, 10, 0.6).until(
#     EC.visibility_of_element_located((By.XPATH, '//*[@id="pass"]')))
# driver.find_element(
#     By.XPATH, '//*[@id="pass"]').send_keys(fb["password"])
# WebDriverWait(driver, 10, 0.6).until(
#     EC.visibility_of_element_located((By.XPATH, '//*[@id="loginbutton"]')))
# driver.find_element(By.XPATH, '//*[@id="loginbutton"]').click()

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

            sleep(2)

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
                ticketList = driver.find_elements(
                    By.CSS_SELECTOR, 'div.zone.area-list > ul')
                print("ticketList" + str(len(ticketList)))
                if len(ticketList)==0:
                    break
                exit_flag = verifySeat(ticketList)

                print("y=0 ends")

            elif y == 1:
                print("y=1")
                WebDriverWait(driver, 10, 0.6).until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, '.zone.area-list ul li')))  # 最長等待10秒，每0.5秒檢查一次條件是否成立
                ticketList = driver.find_elements(
                    By.CSS_SELECTOR, '.zone.area-list ul li')
                exit_flag = verifySeat(ticketList)
                print("y=1 ends")    

            else:
                continue

            if exit_flag:
                break
        

    try:
        
        WebDriverWait(driver, 1, 0.6).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.normal tr select')))
    except:
        #回答問題頁面  
        print(driver.title)
        print("回答問題頁面")

         
        if verifyCheckCode(driver):
            print("checkCode's passed")
        else:
            print("failed to verify checkCode")
            
    # 輸入驗證碼頁面    
    print(driver.title)    
    while True:    
        
        WebDriverWait(driver, 300, 0.6).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.normal tr select')))    
        Select(driver.find_element(By.CSS_SELECTOR, '.normal tr select')
                    ).select_by_value(expectedTicketAmount)

        driver.find_element(By.XPATH, '//*[@id="TicketForm_agree"]').click()

        WebDriverWait(driver, 10, 0.6).until(
            EC.visibility_of_element_located((By.ID, 'TicketForm_verifyCode')))
        toElement = driver.find_element(By.ID, 'TicketForm_verifyCode').click()
    
        try:
            WebDriverWait(driver, 300, 1).until(
                EC.presence_of_element_located(locator1))  # 最長等待10秒，每0.5秒檢查一次條件是否成立
            WebDriverWait(driver, 300, 1).until(
                EC.presence_of_element_located(locator2))  # 最長等待10秒，每0.5秒檢查一次條件是否成立
        
            break    
        except:
            
            print("驗證碼輸入錯誤: ")
            sleep(1.4)
            continue        

    continue






