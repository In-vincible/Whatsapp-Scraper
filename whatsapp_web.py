from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time 
import csv

LAST_MESSAGES = 4
WAIT_FOR_CHAT_TO_LOAD = 2 # in secs

message_dic = {}
driver = webdriver.Firefox()
wait = WebDriverWait(driver, 600)

def chats():
    name = driver.find_element_by_xpath("//div[@class='_2zCDG']/span").text
    m_arg = '//div[@class="_9tCEa"]/div'
    messages = driver.find_elements_by_xpath(m_arg)  
    top_messages = messages[-1*LAST_MESSAGES:]
    message_dic[name] = [m.text for m in top_messages]
    image = driver.find_element_by_xpath("//*[@id="main"]/header/div[1]/div/img")
    message_dic[name].append(image.get_attribute('src'))
    print(message_dic[name])

def scrape(prev):
    recentList = driver.find_elements_by_xpath("//div[@class='_2wP_Y']")
    recentList.sort(key=lambda x: int(x.get_attribute('style').split("translateY(")[1].split('px')[0]), reverse=False)

    next_focus = None
    start = 0
    for idx,tab in enumerate(recentList):
        if tab == prev:
            start = idx
            break

    for l in recentList[start:]:
        try:
            l.click()
            time.sleep(WAIT_FOR_CHAT_TO_LOAD)
            chats()
            next_focus = l
        except:
            pass
    if prev == next_focus:
        return
    scrape(next_focus)

def save_to_csv():
    rows = [[key]+message_dic[key] for key in message_dic]

    with open('chats.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(rows)
    writeFile.close()

if __name__ == '__main__':
    driver.get("https://web.whatsapp.com/")
    wait = WebDriverWait(driver, 600)
    
    x_arg = '//img[@class="Qgzj8 gqwaM"]'
    group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
    scrape(None)
    save_to_csv()
