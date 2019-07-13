from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
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
    "bet_type": False,
    "bet_number": 1,
    "maxNum_A": 4,
    "maxNum_B": 5,
    "maxNum_C": 5,
    "nextStake": 2,
    "money_risk": 100
}
at_times = ['13:58', '14:03', '14:08', '14:13', '17:50', '18:50', '19:50', '20:50', '21:50', '22:50', '23:50',
            '00:50', '01:50', '02:50', '03:50', '05:50']
at_times1 = ['00:53', '00:58', '01:03', '01:08', '22:13', '22:17', '22:22', '22:27', '14:46', '17:33']


class Bettingbot:

    def __init__(self, username, password, url, bet_type, maxNum_A, maxNum_B, maxNum_C, nextStake, result_url,
                 money_risk):
        self.username = username
        self.password = password
        self.bet_type = bet_type
        #        self.bet_number = bet_number
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
        self.driver = webdriver.Chrome('./chromedriver')

    def closedriver(self):
        self.driver.close()

    # login function
    def login(self):
        driver = self.driver
        driver.get(self.url)
        time.sleep(10)
        driver.find_element_by_xpath('//*[@id="username"]').send_keys(self.username)
        driver.find_element_by_xpath('//*[@id="password2"]').send_keys(self.password)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="loginBtn"]').click()  # click login button

        timeout = 20
        element_present = EC.element_to_be_clickable((By.XPATH, '//*[@id="moneyOpen"]'))
        WebDriverWait(driver, timeout).until(element_present)
        driver.find_element_by_xpath('//*[@id="moneyOpen"]').click()  # click show money on account button

    #        time.sleep(5)

    # italy bet
    def bet_italy(self):

        driver = self.driver
        time.sleep(10)
        driver.find_element_by_xpath('//*[@id="loto-countries"]/div[2]').click()  # click loto by country
        time.sleep(10)
        driver.find_element_by_partial_link_text('Win for life Classico').click()  # click italy loto

        time.sleep(10)
        driver.find_element_by_xpath('//*[@id="main-lottobetting-content"]/div[2]/div[1]/table/tbody/tr[2]').click()
        time.sleep(5)

        xpath = '//*[@id="main-lottobetting-content"]/div[2]/div[1]/table/tbody/tr[3]/td/ul/li['  # choose a bet number
        betnumber = 2 * random.randint(1, 20)
        xpath = xpath + str(betnumber) + ']'  # bet number xpath
        driver.find_element_by_xpath(xpath).click()  # click selected bet number button
        time.sleep(5)

        driver.find_element_by_xpath('//*[@id="input"]').clear()
        driver.find_element_by_xpath('//*[@id="input"]').send_keys(2)
        driver.find_element_by_xpath('//*[@id="submit-ticket"]').click()

        time.sleep(10)
        try:
            driver.find_element_by_xpath('//*[@id="buyin"]').click()  # payment button
        except NoSuchElementException:
            print("Exception occurs")
            time.sleep(5)
            driver.find_element_by_xpath('//*[@id="buyin"]').click()


        time.sleep(10)

    #        driver.find_element_by_xpath('//*[@id="close"]').click()     # close button

    # hungary bet
    def bet_hungary(self):
        print("bet_hungary is running!")
        driver = self.driver
        time.sleep(10)
        driver.find_element_by_xpath('//*[@id="loto-countries"]/div[2]').click()  # click loto by country
        time.sleep(5)
        driver.find_element_by_partial_link_text('Putto').click()  # click italy loto

        time.sleep(10)
        driver.find_element_by_xpath('//*[@id="main-lottobetting-content"]/div[2]/div[1]/table/tbody/tr[2]').click()

        xpath = '//*[@id="main-lottobetting-content"]/div[2]/div[1]/table/tbody/tr[3]/td/ul/li['
        betnumber = 2 * random.randint(1, 20)
        xpath = xpath + str(betnumber) + ']'

        timeout = 20
        element_present = EC.element_to_be_clickable((By.XPATH, xpath))
        WebDriverWait(driver, timeout).until(element_present)
        driver.find_element_by_xpath(xpath).click()

        time.sleep(10)

        driver.find_element_by_xpath('//*[@id="input"]').clear()
        driver.find_element_by_xpath('//*[@id="input"]').send_keys(2)
        driver.find_element_by_xpath('//*[@id="submit-ticket"]').click()

        element_present = EC.visibility_of_element_located((By.XPATH, '/html/body/div[7]'))
        WebDriverWait(driver, 5).until(element_present)

#        time.sleep(10)
        timeout = 20
        time.sleep(timeout)
#        element_present = EC.element_to_be_clickable((By.XPATH, '//*[@id="buyin"]'))
#        WebDriverWait(driver, timeout).until(element_present)
#        element_present = EC.element_to_be_clickable((By.LINK_TEXT, 'UPLATI'))
#        WebDriverWait(driver, timeout).until(element_present)

        driver.find_element_by_xpath('//*[@id="buyin"]').click()


    def get_sum(self, k):
        sum = 0
        for kval in k:
            sum += kval
        return sum

    def get_nextstake(self, statusA, statusB):
        print("get_nextStake method is running")
        total_kb = self.get_sum(self.kb)

        base = (1 / total_kb) * self.money_onAccount * self.kb[statusB - 1]

        total_ka = self.get_sum(self.ka)

        self.nextStake = math.ceil((1 / total_ka) * base * self.ka[statusA - 1])
        print("NextStake:", self.nextStake)

    # get amount of money on my account
    def get_accountmoney(self):
        print("get_accountMoney is running")
        driver = self.driver
        time.sleep(5)
        money_str = driver.find_element_by_xpath('//*[@id="userBalance"]').text

        self.money_onAccount = int(money_str.split(",")[0])
        print("money on Account:", self.money_onAccount)

    # get previous result
    def get_result(self):
        driver = self.driver
        driver.get(self.result_url)
        time.sleep(15)

        self.prevResult["kolo"] = driver.find_element_by_xpath('//*[@id="summary"]/tbody/tr[1]/td[3]').text
        self.prevResult["datetime"] = driver.find_element_by_xpath('//*[@id="summary"]/tbody/tr[1]/td[5]').text
        self.prevResult["status"] = driver.find_element_by_xpath('//*[@id="summary"]/tbody/tr[1]/td[9]').text

        print(self.prevResult)
        driver.get(self.url)

    def get_status(self):
        print("get_status is running")
        self.statusC += 1
        if self.prevResult["status"] == 'Nedobitni':
            self.statusA += 1
        elif self.prevResult["status"] == 'Dobitni':
            self.statusA = 1
        else:
            self.get_result()

        if self.statusA > self.maxNum_A:
            self.statusB += 1
            self.statusC = 0
            self.statusA = 1

        if self.statusB > self.maxNum_B:
            self.trigger = 0

        if self.statusC > self.maxNum_C:
            self.statusA = 1
            self.statusB = 1
            self.statusC = 0

        print("A status: ", self.statusA)
        print("B status: ", self.statusB)
        print("C status: ", self.statusC)

    # is stop now?
    def is_stop(self):
        if self.money_onAccount <= self.money_risk or self.statusB >= self.maxNum_B:
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
    print("Crotia time is " + datetime.now(pytz.timezone('Europe/Zagreb')).time().strftime("%H:%M"))

    bot.get_accountmoney()
    bot.get_nextstake(bot.statusA, bot.statusB)
    bot.bet_hungary()

    print("Crotia time is " + datetime.now(pytz.timezone('Europe/Zagreb')).time().strftime("%H:%M"))

    time.sleep(170)
    bot.get_result()
    bot.get_status()


if __name__ == "__main__":

    username = inputData["user_name"]
    password = inputData["user_pass"]
    site_url = "https://www.lutrija.hr/lotokladenjestaro"
    result_url = "https://www.lutrija.hr/igraj/user/gamesHistory.html"
    bet_number = inputData['bet_number']
    bet_type = inputData["bet_type"]
    maxNum_A = inputData["maxNum_A"]
    maxNum_B = inputData["maxNum_B"]
    maxNum_C = inputData["maxNum_C"]
    nextStake = inputData["nextStake"]
    money_risk = inputData["money_risk"]
    array_a = [1, 2, 4, 3]
    array_b = [1, 2, 4, 5, 7]

    bot = Bettingbot(username, password, site_url, bet_type, maxNum_A, maxNum_B, maxNum_C, nextStake,
                     result_url, money_risk)
    bot.set_ka(array_a)
    bot.set_kb(array_b)

    bot.login()
    bot.bet_hungary()








