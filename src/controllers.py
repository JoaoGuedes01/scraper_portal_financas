import utils

def CLIConfig(user_nif, user_password):
    utils.ConfigCLI(user_nif, user_password)

def CheckLogin(headless):
    driver = utils.CreateDriver(headless)
    utils.LoginWithCredentials(driver)
    driver.quit()

def checkFiscalSituation(headless, screenshot, save_file):

    driver = utils.CreateDriver(headless)
    utils.LoginWithCredentials(driver)
    utils.NavigateToMyArea(driver)
    fiscal_situation = utils.CheckFiscalSituationText(driver)

    if screenshot:
        fiscal_situation = utils.ScreenShotRoutine(driver, 'fiscal-situation', fiscal_situation)

    if save_file:
        utils.SaveObjectToFile(fiscal_situation, 'fiscal_situation')
        
    driver.quit()