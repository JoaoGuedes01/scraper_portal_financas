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

def checkMessages(headless, screenshot, save_file):
    # Creating driver
    driver = utils.CreateDriver(headless)
    utils.LoginWithCredentials(driver)
    # Login with config credentials
    utils.NavigateToMyArea(driver)
    # Check the messages
    current_messages = utils.CheckMessages(driver)

    # Take and save screenshot
    if screenshot:
        current_messages = utils.ScreenShotRoutine(driver, 'current-messages', current_messages)
    # Save results
    if save_file:
        utils.SaveObjectToFile(current_messages, 'current_messages')
    driver.quit()

def checkInteractions(headless, screenshot, save_file):
    # Creating driver
    driver = utils.CreateDriver(headless)
    utils.LoginWithCredentials(driver)
    # Login with config credentials
    utils.NavigateToMyArea(driver)
    # Check the messages
    current_interactions = utils.CheckInteractions(driver)

    # Take and save screenshot
    if screenshot:
        current_messages = utils.ScreenShotRoutine(driver, 'current-interactions', current_interactions)
    # Save results
    if save_file:
        utils.SaveObjectToFile(current_interactions, 'current_interactions')
    driver.quit()

def checkPayments(headless, screenshot, save_file, current_payments, missing_payments, refund_payments):
    if not current_payments and not missing_payments and not refund_payments:
        print("Please select a payments option to check (--help for more )")
        return
     # Creating driver
    driver = utils.CreateDriver(headless)
    utils.LoginWithCredentials(driver)
    # Login with config credentials
    utils.NavigateToMyArea(driver)
    utils.NavigateToPagamentos(driver)
    payments = {}
    if current_payments:
        current_payments = utils.CheckPayments(driver, 'current')

        if screenshot:
            current_payments = utils.ScreenShotRoutine(driver, 'current_payments', current_payments)

        payments["current_payments"] = current_payments

    if missing_payments:
        missing_payments = utils.CheckPayments(driver, 'missing')

        if screenshot:
            missing_payments = utils.ScreenShotRoutine(driver, 'missing_payments', missing_payments)

        payments["missing_payments"] = missing_payments
    if refund_payments:
        refund_payments = utils.CheckPayments(driver, 'refund')

        if screenshot:
            refund_payments = utils.ScreenShotRoutine(driver, 'refund_payments', refund_payments)
        
        payments["refund_payments"] = refund_payments

    # Save results
    if save_file:
        utils.SaveObjectToFile(payments, 'payments')
    driver.quit()