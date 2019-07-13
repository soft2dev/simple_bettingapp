from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
# from bs4 import BeautifulSoup
# import requests
# import xlrd
from datetime import datetime
import time
import pytz
import math
import schedule
import random

inputData = {
    "user_name": "lukicama",
    "user_pass": "test12345",
    "bet_type": 0,
    "bet_number": 1,
    "maxNum_A": 4,
    "maxNum_B": 5,
    "maxNum_C": 5,
    "nextStake": 2,
    "money_risk": 100
}

time_run = []

def set_time(bet_type):
    if bet_type == 0:
        for i in range(8, 22):
            for j in range(3, 60, 5):
                if i < 10:
                    str_hour = '0' + str(i)
                else:
                    str_hour = str(i)
                if j < 10:
                    str_min = '0' + str(j)
                else:
                    str_min = str(j)
                str_time = str_hour + ':' + str_min
                time_run.append(str_time)
    else:
        for i in range(7, 22):
            if i < 10:
                str_hour = '0' + str(i)
            str_hour = str(i)
            str_time = str_hour + ':' + '50'
            time_run.append(str_time)

at_times = ['13:58', '14:03', '14:08', '14:13', '17:50', '18:50', '19:50', '20:50', '21:50', '22:50', '23:50',
            '00:50', '01:50', '02:50', '03:50', '05:50']
at_times1 = ['21:13', '21:18', '21:23', '21:28', '21:33', '20:37', '20:42', '20:47']

class Bettingbot:

    def __init__(self, username, password, url, bet_type, maxNum_A, maxNum_B, maxNum_C, nextStake, result_url, money_risk):
        self.username = username
        self.password = password
        self.bet_type = bet_type
        self.money_onAccount = 0
        self.money_risk = money_risk
        self.statusA = 1
        self.statusB = 1
        self.statusC = 0
        self.maxNum_A = maxNum_A
        self.maxNum_B = maxNum_B
        self.maxNum_C = maxNum_C
        self.trigger = 1
        self.nextStake = nextStake
        self.url = url
        self.result_url = result_url
        self.ka = []
        self.kb = []
        self.prevResult = {"kolo": "", "datetime": "", "status": ""}
#        self.driver = webdriver.Firefox(executable_path='./geckodriver')
        self.driver = webdriver.Chrome('./chromedriver.exe')

    def closedriver(self):
        self.driver.quit()

    def set_inputData(self, bet_type, maxNum_A, maxNum_B, maxNum_C, initialstake, money_risk):
        self.bet_type = bet_type
        self.money_risk = money_risk
        self.maxNum_A = maxNum_A
        self.maxNum_B = maxNum_B
        self.maxNum_C = maxNum_C
        self.nextStake = initialstake
    
#        self.driver = webdriver.Firefox(executable_path='./geckodriver')
        
    # login function
    def login(self):
        print("login start to run: " + datetime.now(pytz.timezone('Europe/Zagreb')).time().strftime("%H:%M"))
        driver = self.driver
        driver.get(self.url)
        time.sleep(10)
        driver.find_element_by_xpath('//*[@id="username"]').send_keys(self.username)
        driver.find_element_by_xpath('//*[@id="password2"]').send_keys(self.password)
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="loginBtn"]').click()  # click login button

        timeout = 20
        element_present = EC.element_to_be_clickable((By.XPATH, '//*[@id="moneyOpen"]'))
        WebDriverWait(driver, timeout).until(element_present)
        driver.find_element_by_xpath('//*[@id="moneyOpen"]').click()  # click show money on account button

    # italy bet
    def bet_italy(self):
        print("bet_italy start to run: " + datetime.now(pytz.timezone('Europe/Zagreb')).time().strftime("%H:%M"))
        driver = self.driver
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="loto-countries"]/div[2]').click()  # click loto by country
        time.sleep(2)
        driver.find_element_by_partial_link_text('Win for life Classico').click()  # click italy loto

        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="main-lottobetting-content"]/div[2]/div[1]/table/tbody/tr[2]').click()

        xpath = '//*[@id="main-lottobetting-content"]/div[2]/div[1]/table/tbody/tr[3]/td/ul/li[' 
        betnumber = 2 * random.randint(1, 20)
        xpath = xpath + str(betnumber) + ']'  # bet number xpath
        
        element_present = EC.element_to_be_clickable((By.XPATH, xpath))
        WebDriverWait(driver, 20).until(element_present)
        driver.find_element_by_xpath(xpath).click()  # click selected bet number button
        
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="input"]').clear()
        driver.find_element_by_xpath('//*[@id="input"]').send_keys(2)
        driver.find_element_by_xpath('//*[@id="submit-ticket"]').click()

        time.sleep(20)
        try:
            driver.find_element_by_xpath('//*[@id="buyin"]').click()  # payment button
        except Exception:
            print("Exception occurs")
            time.sleep(10)
            driver.find_element_by_xpath('//*[@id="buyin"]').click()
        time.sleep(5)
        
    # bet hungary
    def bet_hungary(self):
        print("bet_hungary start to run: " + datetime.now(pytz.timezone('Europe/Zagreb')).time().strftime("%H:%M"))
        driver = self.driver
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="loto-countries"]/div[2]').click()  # click loto by country
        time.sleep(3)
        driver.find_element_by_partial_link_text('Putto').click()  # click italy loto

        element_present = EC.element_to_be_clickable((By.XPATH, '//*[@id="main-lottobetting-content"]/div[2]/div[1]/table/tbody/tr[2]'))
        WebDriverWait(driver, 30).until(element_present)
#        time.sleep(15)
#        driver.implicitly_wait(20)

        driver.find_element_by_xpath('//*[@id="main-lottobetting-content"]/div[2]/div[1]/table/tbody/tr[2]').click()

        xpath = '//*[@id="main-lottobetting-content"]/div[2]/div[1]/table/tbody/tr[3]/td/ul/li['
        betnumber = 2 * random.randint(1, 20)
        xpath = xpath + str(betnumber) + ']'
        timeout = 10
        time.sleep(timeout)
        driver.find_element_by_xpath(xpath).click()

        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="input"]').clear()
        driver.find_element_by_xpath('//*[@id="input"]').send_keys(2)
        driver.find_element_by_xpath('//*[@id="submit-ticket"]').click()

        element_present = EC.visibility_of_element_located((By.XPATH, '/html/body/div[7]'))
        WebDriverWait(driver, 5).until(element_present)

#        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'buyin')))
        time.sleep(25)
        driver.find_element_by_xpath('//*[@id="buyin"]').click()  # payment button
        time.sleep(15)
#        except Exception:
#            print("Exception occurs")
            
#            time.sleep(20)
#            driver.find_element_by_id('buyin').click()
        """
        try:
            element_present = EC.text_to_be_present_in_element((By.XPATH, '//*[@id="slip"]/h2'), 'LISTIĆ JE UPLAĆEN')
            WebDriverWait(driver, 15).until(element_present)
        except Exception:
            print("Exception occurs")     
        """
        
    # get amount of next stake
    def get_sum(self, k):
        sum = 0
        for kval in k:
            sum += kval
        return sum
    
    # get amount of next stake
    def get_nextstake(self, statusA, statusB):
        print("get_nextstake start to run: " + datetime.now(pytz.timezone('Europe/Zagreb')).time().strftime("%H:%M"))
        total_kb = self.get_sum(self.kb)
        base = (1 / total_kb) * self.money_onAccount * self.kb[statusB-1]
        total_ka = self.get_sum(self.ka)
        self.nextStake = math.ceil((1 / total_ka) * base * self.ka[statusA-1])
        if self.nextStake < 2:
            self.nextStake += 1
        print("NextStake:", self.nextStake)

    # get amount of money on my account
    def get_accountmoney(self):
        print("get_accountmoney start to run: " + datetime.now(pytz.timezone('Europe/Zagreb')).time().strftime("%H:%M"))
        driver = self.driver
        time.sleep(5)
        money_str = driver.find_element_by_xpath('//*[@id="userBalance"]').text

        self.money_onAccount = int(money_str.split(",")[0])
        print("money on Account:", self.money_onAccount)

    # get previous result
    def get_result(self):
        print("get result function start to run: " + datetime.now(pytz.timezone('Europe/Zagreb')).time().strftime("%H:%M"))
        driver = self.driver
        driver.get(self.result_url)
        self.prevResult["kolo"] = driver.find_element_by_xpath('//*[@id="summary"]/tbody/tr[1]/td[3]').text
        self.prevResult["datetime"] = driver.find_element_by_xpath('//*[@id="summary"]/tbody/tr[1]/td[5]').text
        condition = driver.find_element_by_xpath('//*[@id="summary"]/tbody/tr[1]/td[9]').text

        while True:
            if condition == 'Nedobitni' or condition == 'Dobitni':
                break
            else:
                time.sleep(10)
                driver.get(self.result_url)
                time.sleep(10)
                condition = driver.find_element_by_xpath('//*[@id="summary"]/tbody/tr[1]/td[9]').text
                print("status: " + condition)

        self.prevResult["status"] = condition
        print(self.prevResult)
        driver.get(self.url)

    # get counter A, B, C status
    def get_status(self):
        print("get_status start to run: " + datetime.now(pytz.timezone('Europe/Zagreb')).time().strftime("%H:%M"))
        self.statusC += 1
        
        if self.prevResult["status"] == 'Nedobitni':
            self.statusA += 1
        else:
            self.statusA = 1
        
        if self.statusA > self.maxNum_A:
            self.statusB += 1
            self.statusA = 1
            self.statusC = 0

        if self.statusB > self.maxNum_B:
            self.trigger = 0

        if self.statusC > self.maxNum_C:
            self.statusA = 1
            self.statusB = 1
            self.statusC = 0

        print("A,B,C status: ", self.statusA, self.statusB, self.statusC)

    # is stop now?
    def is_stop(self):
        if self.money_onAccount <= self.money_risk or self.statusB > self.maxNum_B:
            self.trigger = 0
        return self.trigger

    def set_ka(self, arra):
        for value in arra:
            self.ka.append(value)
    #        print(self.ka)

    def set_kb(self, arra):
        for value in arra:
            self.kb.append(value)
    #        print(self.kb)

def betting_job(bot):
    print("Job start to run: " + datetime.now(pytz.timezone('Europe/Zagreb')).time().strftime("%H:%M"))
    bot.get_accountmoney()
    bot.get_nextstake(bot.statusA, bot.statusB)
    bot.bet_hungary()
#    bot.bet_italy()
    bot.get_result()
    bot.get_status()

if __name__ == "__main__":
    username = inputData["user_name"]
    password = inputData["user_pass"]
    site_url = "https://www.lutrija.hr/lotokladenjestaro"
    result_url = "https://www.lutrija.hr/igraj/user/gamesHistory.html"
    bet_type = inputData["bet_type"]
    maxNum_A = inputData["maxNum_A"]
    maxNum_B = inputData["maxNum_B"]
    maxNum_C = inputData["maxNum_C"]
    nextStake = inputData["nextStake"]
    money_risk = inputData["money_risk"]
    array_a = [1, 2, 4, 3]
    array_b = [1, 2, 4, 5, 7]

    bot = Bettingbot(username, password, site_url, bet_type, maxNum_A, maxNum_B, maxNum_C, nextStake, result_url, money_risk)
    bot.set_ka(array_a)
    bot.set_kb(array_b)

    bot.login()
    bot.get_accountmoney()
    bot.get_nextstake(bot.statusA, bot.statusB)
    bot.bet_hungary()
#    bot.bet_italy()
    bot.get_result()
    bot.get_status()
        

"""
    for at_time in at_times1:
        schedule.every().day.at(at_time).do(betting_job, bot)

    while True:
        schedule.run_pending()
        time.sleep(3)
"""








