from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from time import sleep
import pickle

# URL = "https://piao.damai.cn/160275.html?spm=a2oeg.search_category.0.0.38e34fe0L4ybGg&clicktitle=%E6%83%8A%E5%A4%A9%E9%AD%94%E7%9B%97%E5%9B%A2%EF%BC%88Now%20You%20See%20Me%EF%BC%89Live%20%E4%B8%96%E7%95%8C%E5%B7%A1%E6%BC%94%E6%88%90%E9%83%BD%E7%AB%99"  # PC页面
URL = "https://piao.damai.cn/159203.html?spm=a2o6e.11081723.1329302258.dcarditem_3.67f33a03Z0EkwW"

driver = webdriver.Chrome(executable_path='/Users/srt_kid/Downloads/chromedriver')
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


def book_ticket():
    # 使用cookies储存登陆信息
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

    time = None
    while None == time:
        time = choose('//*[@id="performList"]/div/ul/li[1]')
    time.click()

    price = None
    while None == price:
        price = choose('//*[@id="priceList"]/div/ul/li[3]')
    price.click()

    plus = None
    while None == plus:
        plus = choose('//*[@id="cartList"]/div[1]/ul/li/span[3]/a[2]')
    # for i in range(10):
    #     plus.click()

    buybtn = None
    while None == buybtn:
        buybtn = choose('//*[@id="btnBuyNow"]')
    driver.execute_script("arguments[0].scrollIntoView();", buybtn)
    buybtn.click()


def confirm_booking():
    submit = None
    while None == submit:
        submit = choose('//*[@id="orderConfirmSubmit"]')
    driver.execute_script("arguments[0].scrollIntoView();", submit)
    submit.click()


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



if __name__ == '__main__':
    book_ticket()
    # handle_id()
    confirm_booking()
