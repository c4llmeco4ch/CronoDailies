from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions


def goToChrono():
    browser.get("https://www.chrono.gg/")
    assert "Chrono.gg" in browser.title

def needLogin(button):
    with open("credentials.txt") as info:
        text = info.read()
        assert ":" in text
        login = text.split(":")
        button.click()
        browser.find_element_by_name("username").send_keys(login[0])
        browser.find_element_by_name("password").send_keys(login[1] + Keys.RETURN)


if __name__ == "__main__":
    ffLoc = FirefoxBinary(r'C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe')
    browser = webdriver.Firefox(firefox_binary=ffLoc)
    goToChrono()
    loginNav = browser.find_element_by_class_name("accountNav")
    try:
        loginButton = loginNav.find_element_by_link_text("Sign In")
    except NoSuchElementException:
        pass
    else:
        needLogin(loginButton)