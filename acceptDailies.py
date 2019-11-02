from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys
import datetime
import pathlib


# import typing
# WE = typing.NewType("")
# TODO: Add typing hints for functions


def goToChrono() -> None:
    """Direct the browser to chrono.gg"""
    browser.get("https://www.chrono.gg/")
    assert "Chrono.gg" in browser.title


def needLogin(button) -> None:
    """Login to chrono.gg using info from a text file"""
    path = pathlib.Path("credentials.txt")
    if not path.exists():
        response = input("You do not have a credentials file."
                         + " Would you like to create one?")
        if "y" in response:
            with open("credentials.txt", "x") as login:
                text = input("Username: ")
                text += ":"
                text += input("Password: ")
                login.write(text)
        else:
            input("No credentials created. "
                  + "Please log in and press enter to continue")
            return
    with open("credentials.txt") as info:
        text = info.read()
        assert ":" in text
        login = text.split(":")
        button.click()
        browser.find_element_by_name("username").send_keys(login[0])
        browser.find_element_by_name("password").send_keys(login[1])
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


def collectDaily() -> None:  # TODO: Deal with treasure openings
    """Check if the reward coin has been clicked and, if not, click it"""
    wait = WebDriverWait(browser, 5)
    coin = wait.until(EC.presence_of_element_located(
        (By.CLASS_NAME, "coin")))
    if coin.get_attribute("class") == "coin dead":
        print("Coins already collected for the day.")
    else:
        coin.click()
        print("Coins collected for the day")


def checkStore():
    """Determine if new games are in the store"""
    pastList = parsePastText()
    currentGames = browser.find_element_by_class_name("chrono-shop__games")


def parsePastText():  # TODO: Return list of strings
    """Read the pastShop file"""
    oldGames = []
    try:
        with open("pastShop.txt") as past:
            lines = past.readlines()
            date = lines.pop(0)  # More for the user than the program
            for game in lines:  # Save the list of game titles to a list
                oldGames.append(game.split(":"))
    except OSError:
        print("No 'pastShop.txt' file.\nPlease run "
              + "'python acceptDalies.py -c' to create a new file")
        sys.exit()
    else:
        return oldGames


def createGameFile(gameDiv, overwrite) -> None:
    gameList = []
    try:
        with open("pastShop.txt", ("w" if overwrite else "x")) as file:
            for game in gameDiv.find_elements_by_tag_name("li"):
                name = game.find_element_by_class_name("game-name").text
                claimed = game.find_element_by_class_name("claimed-value").text
                claimed = claimed[:claimed.index("%")]
                gameList.append("{n}:{perc}".format(n=name, perc=claimed))
            file.write(datetime.datetime)
            for val in gameList:
                file.write(val + '\n')
    except OSError:
        print("Tried to overwrite a file that does not exist...exiting")
        sys.exit()


def breakDown(driver) -> None:
    driver.close()
    del(driver)


def determineBasePath() -> str:
    if sys.platform == "linux" or sys.platform == "linux2":
        return r'/usr/lib/firefox/firefox'
    elif "win" in sys.platform.lower():
        return r'C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe'
    elif sys.platform == "darwin":
        return r'/Applications/Firefox.app'


if __name__ == "__main__":
    ffPath = determineBasePath()
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
    breakDown(browser)
