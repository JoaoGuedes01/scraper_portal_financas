import src.utils as utils

def CheckLogin(user_nif, user_pass, headless):
    driver = utils.CreateDriver(headless)
    utils.LoginWithCredentials(driver, user_nif, user_pass)
    driver.quit()

def checkFiscalSituation(user_nif, user_pass, headless):
    driver = utils.CreateDriver(headless)
    utils.LoginWithCredentials(driver, user_nif, user_pass)
    utils.NavigateToMyArea(driver)
    utils.CheckFiscalSituationText(driver)
    driver.get_screenshot_as_file("screenshot.png")
    driver.quit()