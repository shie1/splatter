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


def check_exists(by, select, driver):
    try:
        driver.find_element(by, select)
    except NoSuchElementException:
        return False
    return True


def smooth_type(text, element):
    text = text.split()
    for letter in text:
        element.send_keys(letter)
        sleep(uniform(0.5, 1))
    return


def quickplay(user, password, playlist, driver, options):
    driver.delete_all_cookies()
    driver.get("https://www.google.com/search?q=spotify")
    sleep(2)
    driver.get("https://accounts.spotify.com/en/login?continue=" +
               parse.quote(playlist.encode("utf-8")))

    if (user != None) and (password != None):
        user_elem = driver.find_element(By.ID, "login-username")
        password_elem = driver.find_element(By.ID, "login-password")
        button_elem = driver.find_element(By.ID, "login-button")

        user_elem.clear()
        sleep(uniform(0.1, 0.25))
        password_elem.clear()
        sleep(uniform(0.1, 0.25))

        smooth_type(user, user_elem)
        smooth_type(password, password_elem)
        sleep(uniform(0.5, 1))
        button_elem.click()

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
        try:
            time = driver.find_element(By.CSS_SELECTOR,
                                       "div.playback-bar__progress-time-elapsed").text
            mins, secs = time.split(":")
            mins = int(mins)
            secs = int(secs)
            print(mins, secs)
            if((mins != 0) == True) or ((secs > 35) == True):
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
    return uc.Chrome(chrome_options)


def start(options, playlist):
    for x in range(0, int(options["threads"])):
        if(options["login"] == True):
            u = options["userlist"][x].split(":")
            if(len(u) != 2):
                continue
            user, password = u
        else:
            user, password = None, None

        Thread(target=quickplay, args=(user, password,
               playlist, browser(options), options)).start()
