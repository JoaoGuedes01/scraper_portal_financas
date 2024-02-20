import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options


home_dir = os.path.expanduser("~")
home_dir = os.path.join(home_dir, "GuedesMoney")
home_dir_screenshot = os.path.join(home_dir, "ScreenShots")

os.makedirs(home_dir, exist_ok=True)
os.makedirs(home_dir_screenshot, exist_ok=True)

goodFiscalSituation = "Situação Fiscal Regularizada"
financas_login_page = "https://www.acesso.gov.pt/v2/loginForm?partID=PFAP&path=/geral/dashboard"

# Controller Functions

def LoginWithCredentials(driver):
    # Loading Configuration to memory
    with open(f'{home_dir}\\config.json', 'r') as f:
        data = json.load(f)

    nif = data['user_nif']
    password = data['user_password']
    print(f'Loggin in NIF: {nif}')

    driver.get(financas_login_page)
    wait_until_element_is_present(driver,By.LINK_TEXT,"Autoridade Tributária e Aduaneira", 10)

    tabs = driver.find_elements(By.CLASS_NAME, 'tab-label')
    for tab in tabs:
        spans = tab.find_elements(By.TAG_NAME, 'span')
        for span in spans:
            if span.text == 'NIF':
                span.click()

    driver.find_element(By.ID, 'input-username-nif-group').find_element(By.CLASS_NAME, 'input-container').find_element(By.TAG_NAME, 'input').send_keys(nif)

    driver.find_element(By.ID, 'input-password-nif-group').find_element(By.CLASS_NAME, 'pw-input-container').find_element(By.TAG_NAME, 'input').send_keys(password)

    driver.find_element(By.XPATH, '//*[@id="sbmtLogin"]').click()
    wait_until_element_is_present(driver, By.ID, 'cumprimento', 10)
    print('successful login')
   
def NavigateToMyArea(driver):
    print('Navigating to My Area')
    driver.find_element(By.CLASS_NAME, 'user-area').click()
    wait_until_element_is_present(driver, By.LINK_TEXT, 'A Minha Área', 10)

def CheckFiscalSituationText(driver):
    wait_until_element_is_not(driver, By.XPATH, '//*[@id="brief-title"]', 'Em Actualização...', 10)
    situation = driver.find_element(By.XPATH, '//*[@id="brief-title"]').text
    if situation == goodFiscalSituation:
        print(f"GOOD | {situation}")
        return {"state": "good", "literal": situation}
    else:
        print(f"BAD | {situation}")
        return {"state": 'bad', "literal": situation}
    
def CheckAlerts(driver):
    # Clicking on Consultar Alertas
    driver.find_element(By.XPATH,'//*[@id="collapseMenu18"]/ul/li[6]').click()
    wait_until_element_is_present(driver, By.ID, 'alertas-table', 10)
    alert_table = driver.find_element(By.ID, 'alertas-table')
    rows = alert_table.find_elements(By.TAG_NAME, 'tr')
    del rows[0]
    alert_rows_obj = []
    for row in rows:
        # Get all columns in each row
        cols = row.find_elements(By.TAG_NAME, 'td')

        # Get the text from each column
        cols_text = [col.text for col in cols]

        new_alert_obj = {
            "desc": next(iter(cols_text), 'no data'),
            "limit_date": next(iter(cols_text[1:]), 'no data')
        }
        alert_rows_obj.append(new_alert_obj)
        
    return {"alerts": alert_rows_obj}

def CheckMessages(driver):
    # Clicking on Consultar Mensagens
    driver.find_element(By.XPATH,'//*[@id="collapseMenu18"]/ul/li[5]').click()
    wait_until_element_is_present(driver, By.ID, 'mensagens-table', 10)
    
    # Finding Messages Table and extracting rows
    messages_table = driver.find_element(By.ID, 'mensagens-table')
    rows = messages_table.find_elements(By.TAG_NAME, 'tr')
    del rows[0]
    
    # Extracting data out of the rows
    all_messages = []
    for row in rows:
        # Get all columns in each row
        cols = row.find_elements(By.TAG_NAME, 'td')

        # Get the text from each column
        for col in cols:
            all_messages.append(col.text)
            
    return {"messages": all_messages}

def CheckInteractions(driver):
    # Clicking on Interacoes recentes
    driver.find_element(By.XPATH,'//*[@id="collapseMenu18"]/ul/li[4]').click()
    wait_until_element_is_present(driver, By.ID, 'interacoes-table', 10)
    
    # Finding Interactions Table and extracting rows
    messages_table = driver.find_element(By.ID, 'interacoes-table')
    rows = messages_table.find_elements(By.TAG_NAME, 'tr')
    del rows[0]
    
    all_interactions = []
    for row in rows:
        # Get all columns in each row
        cols = row.find_elements(By.TAG_NAME, 'td')

        # Get the text from each column
        cols_text = [col.text for col in cols]
        new_interaction = {
            "imposto": cols_text[0],
            "desc": cols_text[1],
            "date": cols_text[2],
        }
        all_interactions.append(new_interaction)
    
    return {"interactions": all_interactions}

def CheckPayments(driver, payment_type):
    # Clicking on Pagamentos
    driver.find_element(By.XPATH,'//*[@id="collapseMenu18"]/ul/li[2]').click()
    wait_until_element_is_present(driver, By.ID, 'main-content', 10)
    
    if payment_type == 'current':
        payment_iteration = 1
        table_id = "pagDecorrer"
        
    if payment_type == 'missing':
        payment_iteration = 2
        table_id = "pagEmFalta"
        
    if payment_type == 'refund':
        payment_iteration = 3
        table_id = "tabReembolsos"

    # Clicking on Pagamentos a Decorrer
    payment_suboption = f'//*[@id="collapseMenu35"]/ul/li[{payment_iteration}]'
    driver.find_element(By.XPATH, payment_suboption).click()
    wait_until_element_is_present(driver, By.ID, table_id, 10)
    wait_until_element_is_invisible(driver, By.CLASS_NAME, "loading", 10)
    
    current_payments = driver.find_element(By.ID, table_id)
    rows = current_payments.find_elements(By.TAG_NAME, 'tr')
    del rows[0]
    print(f'Found {len(rows)} rows')
    
    current_payments = []
    for row in rows:
        # Get all columns in each row
        cols = row.find_elements(By.TAG_NAME, 'td')
        
        for col in cols:
            print(col.get_attribute('innerHTML'))

        # Get the text from each column
        cols_text = [col.text for col in cols]
        if payment_type == 'current':
            new_payment_obj = {
            "doc": next(iter(cols_text), 'no data'),
            "payment_data": next(iter(cols_text[1:]), 'no data')
            }
        if payment_type == 'missing':
            new_payment_obj = {
            "process_number": next(iter(cols_text), 'no data'),
            "installation_date": next(iter(cols_text[1:]), 'no data'),
            "value": next(iter(cols_text[2:]), 'no data')
            }
        if payment_type == 'refund':
            new_payment_obj = {
            "doc": next(iter(cols_text), 'no data'),
            "situation": next(iter(cols_text[1:]), 'no data'),
            "value": next(iter(cols_text[2:]), 'no data'),
            "situation_date": next(iter(cols_text[2:]), 'no data')
            }
            
        current_payments.append(new_payment_obj)
    return {"payments": current_payments}

def wait_until_element_is_not(driver, by_method, method_expression, undesired_text, timeout=10):
    print(f'Waiting for {method_expression} to not be equal to {undesired_text} through {by_method}')
    try:
        WebDriverWait(driver, timeout).until(
            lambda driver: driver.find_element(by_method, method_expression).text != undesired_text
        )
    except TimeoutException:
        print(f"Timed out waiting for element with text different from {undesired_text}")
    

def wait_until_element_is_present(driver, by_method, method_expression , timeout=10):
    print(f'Locating {method_expression} through {str(by_method)}')
    try:
        # Wait for an element to be present on the page (you can change this condition according to your page)
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by_method, method_expression))
        )
        print('located')
        return True
    except TimeoutException:
        print('not located')
        return False
    
def wait_until_element_is_invisible(driver, by_method, method_expression, timeout=10):
    try:
        print(f'Locating {method_expression} through {str(by_method)}')
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.invisibility_of_element_located((by_method, method_expression)))
        print(f'{method_expression} became invisible')
        return True
    except:
        print(f"Timed out waiting for element with text different from {method_expression}")
        return False
    
    
def takeScreenShot(driver, filename):
    try:
        ext_filename = os.path.join(home_dir_screenshot, f'{filename}.png')
        driver.get_screenshot_as_file(ext_filename)
        print(f'Saved screenshot to {ext_filename}')
        return ext_filename
    except:
        print(f"There was an error saving screenshot to {ext_filename}")

def ScreenShotRoutine(driver, filename, result_obj):
    screenshot_path = takeScreenShot(driver, filename)
    result_obj['screenshot'] = screenshot_path
    return result_obj

def SaveObjectToFile(obj, filename):
    try:
        file_path = os.path.join(home_dir, f'{filename}.json')
        with open(file_path, 'w') as outfile:
            json.dump(obj, outfile)
    except:
        print(f"There was an error while saving results to {file_path}")

def CreateDriver(headless):
    options = Options()
    if headless:
        options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver

def ConfigCLI(user_nif, user_password):
    try:
        config_obj = {
        "user_nif": user_nif,
        "user_password": user_password
        }
        with open(f'{home_dir}\\config.json', 'w') as outfile:
            json.dump(config_obj, outfile)
        print("CLI successfully configured")
    except:
        print("There was an error while configuring thje CLI")

def CheckConfig(show_password):
    try:
        with open(f'{home_dir}\\config.json', 'r') as f:
            data = json.load(f)
        nif = data['user_nif']
        password = data['user_password']
        
        print(f'User NIF: {nif}')
        if show_password:
            print(f'User Password: {password}')
    except:
        print("There was an error while configuring thje CLI")