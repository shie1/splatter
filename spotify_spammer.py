from selenium import webdriver
from time import sleep
from urllib import parse
from threading import Thread
from sys import exit
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def check_exists(css, driver):
    try:
        driver.find_element_by_css_selector(css)
    except NoSuchElementException:
        return False
    return True

def check_exists_xpath(xpath, driver):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

def quickplay(user, password, playlist, driver):
    driver.delete_all_cookies()
    driver.get("https://www.google.com/search?q=spotify")
    sleep(2)
    driver.get("https://accounts.spotify.com/en/login?continue=" + parse.quote(playlist.encode("utf-8")))
    
    while True:
        if(check_exists("#onetrust-accept-btn-handler", driver) == True):
            try:
                driver.find_element_by_css_selector("#onetrust-accept-btn-handler").click() #Accept cookies
                sleep(5)
            except: ""

        #Shuffle
        if(check_exists("button._39234eb5c173f8b6de80ed73820b1be8-scss[aria-checked=\"false\"]", driver) == True):
            try:
                driver.find_element_by_css_selector("button._39234eb5c173f8b6de80ed73820b1be8-scss").click()
            except: ""
                
        #Repeat
        if(check_exists("button.ebfd411a126f1e7bea6133f21b4ef88e-scss[aria-checked=\"false\"]", driver) == True) or (check_exists("button.ebfd411a126f1e7bea6133f21b4ef88e-scss[aria-checked=\"mixed\"]", driver) == True):
            try:
                driver.find_element_by_css_selector("button.ebfd411a126f1e7bea6133f21b4ef88e-scss").click()
            except: ""
            
        #Play
        if(check_exists_xpath('(.//button[contains(concat(" ",normalize-space(@class)," ")," _8e7d398e09c25b24232d92aac8a15a81-scss ")][@aria-label="Play"])[2]', driver) == True):
            try:
                driver.find_element_by_xpath('(.//button[contains(concat(" ",normalize-space(@class)," ")," _8e7d398e09c25b24232d92aac8a15a81-scss ")][@aria-label="Play"])[2]').click()
            except ElementNotInteractableException: driver.send_keys(" ")
            except NoSuchElementException: ""
        
        #Skip
        try:
            time = driver.find_element_by_css_selector("div.playback-bar__progress-time").text
            mins, secs = time.split(":")
            mins = int(mins)
            secs = int(secs)
            if((mins != 0) == True) or ((secs > 35) == True):
                driver.find_element_by_css_selector("button[aria-label=\"Next\"]").click()
        except NoSuchElementException: ""
        
        sleep(5)

def browser(options):
    chrome_options = webdriver.ChromeOptions()
    if(options["audio"] == False): chrome_options.add_argument("--mute-audio")
    if(options["window"] == False): chrome_options.add_argument("--headless")
    return webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),chrome_options=chrome_options)

def start(options,userlist,playlist):
    for x in range(0,int(options["threads"])):
        u = userlist[x].split(":")
        if(len(u) != 2):
            continue
        user, password = u

        Thread(target=quickplay,args=(user,password,playlist,browser(options))).start()