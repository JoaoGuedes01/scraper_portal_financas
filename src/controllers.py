from . import utils

def CLIConfig(user_nif, user_password, sender_email, sender_password, recipient_list, email_type):
    utils.ConfigCLI(user_nif, user_password, sender_email, sender_password, recipient_list, email_type)

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
        fiscal_situation = utils.ScreenShotRoutine(driver, 'fiscal_situation', fiscal_situation)

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
        current_alerts = utils.ScreenShotRoutine(driver, 'current_alerts', current_alerts)
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
        current_messages = utils.ScreenShotRoutine(driver, 'current_messages', current_messages)
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
        current_messages = utils.ScreenShotRoutine(driver, 'current_interactions', current_interactions)
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

def RunGeneral(headless, screenshot, save_file, check_fiscal, check_alerts, check_messages, check_interactions, check_payments, current_payments, missing_payments, refund_payments, send_email, attach_screenshots):
    utils.SetupRootFolder()
    if check_payments and not current_payments and not missing_payments and not refund_payments:
        print("Please select a payments option to check (--help for more )")
        return
    # Creating driver
    driver = utils.CreateDriver(headless)
    utils.LoginWithCredentials(driver)
    # Login with config credentials
    utils.NavigateToMyArea(driver)

    # Initializing data
    data = {}

    # Command Checks
    if check_fiscal:
        fiscal_situation = utils.CheckFiscalSituationText(driver)

        if screenshot:
            fiscal_situation = utils.ScreenShotRoutine(driver, 'fiscal_situation', fiscal_situation)

        data["fiscal_situation"] = fiscal_situation

    if check_alerts:
        current_alerts = utils.CheckAlerts(driver)

        if screenshot:
            current_alerts = utils.ScreenShotRoutine(driver, 'current_alerts', current_alerts)

        data["current_alerts"] = current_alerts

    if check_messages:
        current_messages = utils.CheckMessages(driver)

        if screenshot:
            current_messages = utils.ScreenShotRoutine(driver, 'current_messages', current_messages)

        data["current_messages"] = current_messages

    if check_interactions:
        current_interactions = utils.CheckInteractions(driver)

        if screenshot:
            current_interactions = utils.ScreenShotRoutine(driver, 'current_interactions', current_interactions)

        data["current_interactions"] = current_interactions

    if check_payments:
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
        
        data["payments"] = payments

    # Save data to file
    if save_file:
        utils.SaveObjectToFile(data, 'data')

    if send_email:
        subject = "Finanças Report"
        body = utils.GenerateEmailBody()
        utils.SendEmail(subject, body, attach_screenshots)

    # Close Driver
    driver.quit()
    print("GuedesMoney ran successfully")
    return

def SendEmail():
    subject = "[GUEDESMONEY] - TESTEMAIL"
    body = utils.GenerateEmailBody()
    utils.SendEmail(subject, body)