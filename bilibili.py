from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from time import sleep
import pickle

URL = "https://show.bilibili.com/platform/detail.html?id=17824" # 测试用抢票链接

driver = webdriver.Chrome()
# 设置等待时间
wait = WebDriverWait(driver, 0.3)
driver.get(URL)


def login():
    # 登登登、有验证码自动登陆泥🐎啊，给泥30秒，自己手动登
    # 登陆完把cookies存下来（bilibili好像cookies过期很快
    sleep(30)
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))


def choose(seletor):
    try:
        # 控件可点击时才选定
        choice = wait.until(EC.element_to_be_clickable((By.XPATH, seletor)))
        return choice
    except TimeoutException as e:
        print("Time out!")
        return None
    except Exception:
        print("Not found!")
        return None


def choose_time_and_price():
    # time = None
    # while None == time:
    #     time = choose('//*[@id="performList"]/div/ul/li[1]')
    # time.click()

    print("choosing time...")
    # time = choose('//li[@class="screens"]/div[1]')
    time = choose("//*[contains(text(), '7月27日 19：30')]")
    print(time)
    time.click()

    print("choosing price...")
    # price = choose('//li[@class="tickets"]/div[0]')
    price = choose("//*[contains(text(), '¥980(980票价)')]")
    price.click()

    sleep(0.5)

def load_cookies():
    # 使用cookies储存登陆信息
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

    sleep(2)

def book_ticket():

    load_cookies() # bilibili貌似不能加载cookies登陆，有时需要开头手动登陆

    buy, submit = None, None
    while True:
        try:
            print('refreshing...')
            driver.refresh()
            sleep(0.5)
            choose_time_and_price()

            print("choosing buy...")
            # buy = choose('//div[@class="product-buy-wrapper"]/div[0]')
            buy = choose("//*[contains(text(), '立即购票')]")
            if buy is not None:
                buy.click()
                for i in range(10): # 10 tries
                    print("choosing submit")
                    submit = choose("//div[@class='confirm-paybtn active']")
                    # driver.execute_script("arguments[0].scrollIntoView();", submit)
                    if submit is not None:
                        submit.click()
                        return 'OK'
        except Exception as e:
            print(e)
            return 'NG'


def main():
    status = 'NG'
    while status != 'OK':
        status = book_ticket()
        if status == 'OK':
            sleep(120)
            exit(0)



if __name__ == '__main__':
    login() # 第一次使用调用login()创建cookies
    main()
