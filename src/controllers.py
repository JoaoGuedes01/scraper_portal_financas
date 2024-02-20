import utils

def CLIConfig(user_nif, user_password):
    utils.ConfigCLI(user_nif, user_password)

def CheckConfig(show_password):
    utils.CheckConfig(show_password)

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

def checkAlerts(headless, screenshot, save_file):
    # Creating driver
    driver = utils.CreateDriver(headless)
    utils.LoginWithCredentials(driver)
    # Login with config credentials
    utils.NavigateToMyArea(driver)
    # Check the alerts
    current_alerts = utils.CheckAlerts(driver)

    # Take and save screenshot
    if screenshot:
        current_alerts = utils.ScreenShotRoutine(driver, 'current-alerts', current_alerts)
    # Save results
    if save_file:
        utils.SaveObjectToFile(current_alerts, 'current_alerts')
    driver.quit()