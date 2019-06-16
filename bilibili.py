from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from time import sleep
import pickle

URL = "https://show.bilibili.com/platform/detail.html?id=17824"

driver = webdriver.Chrome()
# 设置等待时间
wait = WebDriverWait(driver, 0.3)
driver.get(URL)


def login():
    # 登登登、登陆泥🐎啊，给你60秒，自己手动登陆！
    # 登陆完把cookies存下来
    sleep(60)
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


    time = choose('//*[@class="screens"]/div[0]')
    time.click()

    price = choose('//*[@class="tickets"]/div[3]')
    price.click()

    sleep(0.5)


def book_ticket():
    # 使用cookies储存登陆信息
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

    buy = None
    while None == buy:
        buy = choose('//*[@class="product-buy"]')
        if buy == None:
            driver.refresh()
            sleep(0.5)
            choose_time_and_price()
    buy.click()


def confirm_booking():
    submit = None
    while None == submit:
        submit = choose('//*[@id="confirm-paybtn"]')
    driver.execute_script("arguments[0].scrollIntoView();", submit)
    submit.click()
    return 'OK'


def handle_id():
    # 什么JB玩意儿？为啥不同场次的实名认证按钮会不一样？？
    # 我不管了，别用这个JB函数，有实名认证要刷验证码也买不了

    # 处理实名认证
    # 选择购票人
    booker = None
    while None == booker:
        booker = choose('/html/body/div[3]/div[3]/div[3]/div[2]/div[2]/div/div/h2/a')
        if booker == None:
            booker = choose('/html/body/div[3]/div[3]/div[2]/div[2]/div/a')
    driver.execute_script("arguments[0].scrollIntoView();", booker)
    booker.click()
    # 选择、确定
    select = None
    while None == select:
        select = choose('/html/body/div[3]/div[3]/div[13]/div/div[2]/div/div[2]/div/table/tbody/tr/label/td[1]/input')
        if select == None:
            select = choose(
                '/html/body/div[3]/div[3]/div[12]/div/div[2]/div/div[2]/div/table/tbody/tr/label/td[1]/input')
    driver.execute_script("arguments[0].scrollIntoView();", select)
    select.click()
    confirm = None
    while None == confirm:
        confirm = choose('/html/body/div[3]/div[3]/div[13]/div/div[2]/div/p/div/a')
        if confirm == None:
            confirm = choose('/html/body/div[3]/div[3]/div[12]/div/div[2]/div/p/div/a')
    driver.execute_script("arguments[0].scrollIntoView();", confirm)
    confirm.click()


def main():
    while True:
        try:
            book_ticket()
            status = confirm_booking()
            if status == 'OK':
                sleep(120)
                exit(0)
        except Exception as e:
            print(e)
            continue



if __name__ == '__main__':
    login()
    main()
