from selenium import webdriver
from time import sleep
from urllib import parse
from threading import Thread
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium import webdriver
from random import uniform
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
from os import system
from math import floor


def check_exists(by, select, driver):
    try:
        driver.find_element(by, select)
    except NoSuchElementException:
        return False
    return True


def smooth_type(text, element):
    for i in range(len(text)):
        letter = text[i]
        if(letter == "@"):
            system("echo %s| clip" % "@".strip())
            element.send_keys(Keys.CONTROL, "v")
        else:
            element.send_keys(letter)
        sleep(uniform(0.05, 0.1))
    return


def login(user, password, driver, redirect=""):
    driver.delete_all_cookies()
    driver.get("https://accounts.spotify.com/en/login?continue=" +
               parse.quote(redirect.encode("utf-8")))

    sleep(1)
    if (user != None) and (password != None):
        user_elem = driver.find_element(By.ID, "login-username")
        password_elem = driver.find_element(By.ID, "login-password")
        button_elem = driver.find_element(By.ID, "login-button")

        user_elem.clear()
        sleep(uniform(0.1, 0.25))
        password_elem.clear()
        sleep(uniform(0.1, 0.25))

        smooth_type(user, user_elem)
        sleep(uniform(0.1, 0.25))
        smooth_type(password, password_elem)
        sleep(uniform(0.5, 1))
        button_elem.click()

    sleep(2)
    if driver.current_url == "https://accounts.spotify.com/en/login?continue=" + parse.quote(redirect.encode("utf-8")):
        raise Exception("Invalid login")


def testlogin(u, driver, options):
    for x in range(0, len(u)):
        user, password = u[x]
        try:
            login(user, password, driver)
            print(':'.join(u[x]))
        except:
            ""


def quickplay(u, driver, options):
    user, password = u
    login(user, password, driver, options["playlist"])

    while True:
        if(check_exists(By.CSS_SELECTOR, "#onetrust-accept-btn-handler", driver) == True):
            try:
                driver.find_element(
                    By.CSS_SELECTOR, "#onetrust-accept-btn-handler").click()  # Accept cookies
                sleep(5)
            except:
                ""

        # Shuffle
        if(check_exists(By.CSS_SELECTOR, "button[aria-label=\"Enable shuffle\"][aria-checked=\"false\"]", driver) == True):
            try:
                driver.find_element(By.CSS_SELECTOR,
                                    "button[aria-label=\"Enable shuffle\"]").click()
            except:
                ""

        # Repeat
        if(check_exists(By.CSS_SELECTOR, "button[aria-label=\"Enable repeat\"][aria-checked=\"false\"]", driver) == True) or (check_exists(By.CSS_SELECTOR, "button.ebfd411a126f1e7bea6133f21b4ef88e-scss[aria-checked=\"mixed\"]", driver) == True):
            try:
                driver.find_element(By.CSS_SELECTOR,
                                    "button[aria-label=\"Enable repeat\"]").click()
            except:
                ""

        # Play
        if(check_exists(By.CSS_SELECTOR, 'button[data-encore-id="buttonPrimary"][data-testid="play-button"][aria-label="Play"][class="Button-sc-qlcn5g-0 futnNt"]', driver) == True):
            try:
                driver.find_element(By.CSS_SELECTOR,
                                    'button[data-encore-id="buttonPrimary"][data-testid="play-button"][aria-label="Play"][class="Button-sc-qlcn5g-0 futnNt"]').click()
            except ElementNotInteractableException:
                driver.find_element(By.TAG_NAME, "body").send_keys(" ")
            except NoSuchElementException:
                ""

        # Skip
        if(options["skip"] != False):
            try:
                time = driver.find_element(By.CSS_SELECTOR,
                                           "div.playback-bar__progress-time-elapsed").text
                mins, secs = time.split(":")
                mins = int(mins)
                secs = int(secs)
                if((mins != 0) == True) or ((secs > options["skip"]) == True):
                    driver.find_element(By.TAG_NAME,
                                        "body").send_keys(Keys.ALT, Keys.ARROW_RIGHT)
            except NoSuchElementException:
                ""

        sleep(5)


def browser(options):
    chrome_options = webdriver.ChromeOptions()
    if(options["audio"] == False):
        chrome_options.add_argument("--mute-audio")
    if(options["headless"] == True):
        chrome_options.add_argument("--headless")
    driver = uc.Chrome(chrome_options)
    sleep(2)
    if(options["headless"] == True):
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                               "source": """ Object.defineProperty(window, 'navigator', { value: new Proxy(navigator, { has: (target, key) => (key === 'webdriver' ? false : key in target), get: (target, key) => key === 'webdriver' ? false : typeof target[key] === 'function' ? target[key].bind(target) : target[key] }) }); """}, )
        driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": driver.execute_script(
            "return navigator.userAgent").replace("Headless", "")}, )
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                               "source": """ Object.defineProperty(navigator, 'maxTouchPoints', { get: () => 1 })"""}, )
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                               "source": "const newProto = navigator.__proto__;" "delete newProto.webdriver;" "navigator.__proto__ = newProto;"}, )
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                               "source": """ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] }); """},)
    driver.delete_all_cookies()
    driver.get("https://www.google.com/search?q=spotify")
    sleep(2)
    return driver


def start(options, target):
    for x in range(0, int(options["threads"])):
        if(target == testlogin):
            if(x != int(options["threads"]) - 1):
                i = (x * floor(len(options["userlist"]) / options["threads"]), (x+1) * floor(
                    len(options["userlist"]) / options["threads"]) - 1)
            else:
                i = (x * floor(len(options["userlist"]) /
                     options["threads"]), len(options["userlist"]))
            u = [x.split("|")[0].split(":")
                 for x in options["userlist"][i[0]:i[1]]]
        else:
            u = options["userlist"][x].split("|")[0].split(":")
            if(len(u) != 2):
                continue
        Thread(target=target, args=(u,
                                    browser(options), options)).start()
