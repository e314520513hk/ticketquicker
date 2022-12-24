import sys
from selenium.webdriver.support.wait import WebDriverWait

def verifySeat(areaList,expectedTicketAmount,expectedArea):
    defaultArea = False
    try:
    
        for x in range(len(areaList)):

            if expectedArea:
                if "熱賣中" in areaList[x].text:
            
                    if expectedArea.lower() in areaList[x].text.lower():
                        areaList[x].click()    
                        return True

                if "剩餘" in areaList[x].text:
                 
                    if expectedArea.lower() in areaList[x].text.lower():
                        splitedAreaName = areaList[x].text.split()
                        remainAmount = len(splitedAreaName)

                        if int(expectedTicketAmount) <= int(splitedAreaName[remainAmount-1]):
                            areaList[x].click()
                            return True
            if not defaultArea:
                if "熱賣中" in areaList[x].text:
       
                    defaultArea = areaList[x]
                    

                if "剩餘" in areaList[x].text:
                 
                    splitedAreaName = areaList[x].text.split()
                    remainAmount = len(splitedAreaName)
                    
                    if int(expectedTicketAmount) <= int(splitedAreaName[remainAmount-1]):
                        defaultArea = areaList[x]

        if defaultArea:
            defaultArea.click()
            return True

        return False

    except Exception as e:
        if type(e).__name__ == 'NoSuchWindowException':
            print("##您的選購條件已無足夠數量")
        return False
    
  

def verifyCheckCode(driver,checkCodeList):
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