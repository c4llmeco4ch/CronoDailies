from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
        mainFrame = browser.current_window_handle
        try:
            captchaFrame = browser.find_elements_by_tag_name("iframe")[1]
            browser.switch_to.frame(captchaFrame)
            wait = WebDriverWait(browser, 5)
            checkBox = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="rc-anchor-container"]')))
        except exceptions.TimeoutException:
            browser.close()
            sys.exit("No Recaptcha Button occurred? Closing...")
        else:
            checkBox.click()
            input("Please confirm Recaptcha is completed, click submit, "
                  + "then press return to continue.")
            browser.switch_to.default_content()


def collectDaily():  # TODO: Deal with treasure openings
    """Check if the reward coin has been clicked and, if not, click it"""
    wait = WebDriverWait(browser, 5)
    coin = wait.until(EC.presence_of_element_located(
        (By.CLASS_NAME, "coin")))
    if coin.get_attribute("class") == "coin dead":
        print("Coins already collected for the day.")
    else:
        coin.click()  
        


def checkStore():
    """Determine if new games are in the store"""
    pastList = parsePastText()
    currentGames = browser.find_element_by_class_name("chrono-shop__games")

def parsePastText():
    """Read the pastShop file"""
    try:
        with open("pastShop.txt") as past:
            lines = past.readlines()
            date = lines.pop(0)
            for game in lines:  # Save the list of game titles to a list
                pass
    except OSError:
        print("No 'pastShop.txt' file.\nPlease run "
              + "'python acceptDalies.py -c' to create a new file")
        sys.exit()

if __name__ == "__main__":
    ffPath = r'C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe'
    ffLoc = FirefoxBinary(ffPath)
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