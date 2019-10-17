from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import time
import sys


def goToChrono():
    """Direct the browser to chrono.gg"""
    browser.get("https://www.chrono.gg/")
    assert "Chrono.gg" in browser.title


def needLogin(button):
    """Login to chrono.gg using info from a text file"""
    with open("credentials.txt") as info:
        text = info.read()
        assert ":" in text
        login = text.split(":")
        button.click()
        browser.find_element_by_name("username").send_keys(login[0])
        browser.find_element_by_name("password").send_keys(login[1])
        try:
            wait = WebDriverWait(browser, 5)
            wait.until(expected_conditions.element_to_be_clickable(
                (By.ID,"recaptcha-anchor")))
            browser.find_element_by_id("recaptcha-anchor").click()
            signIn = "btn full-width modal__button--hero modal__button--login"
            browser.find_element_by_class_name(signIn).click()
        except exceptions.TimeoutException:
            browser.close()
            sys.exit("No Sign In/Recaptcha Button occurred? Closing...")

def collectDaily():
    pass


if __name__ == "__main__":
    ffLoc = FirefoxBinary(r'C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe')
    browser = webdriver.Firefox(firefox_binary=ffLoc)
    goToChrono()
    loginNav = browser.find_element_by_class_name("accountNav")
    try:
        loginButton = loginNav.find_element_by_link_text("Sign In")
    except exceptions.NoSuchElementException:
        print("You are already logged in.\nProceeding to collection")
    else:
        needLogin(loginButton)
    finally:
        collectDaily()