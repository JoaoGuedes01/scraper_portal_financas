from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

# Email Imports
import smtplib
from email.mime.text import MIMEText


# Global Variables
home_dir = os.path.expanduser("~")
home_dir = os.path.join(home_dir, "GuedesMoney")
home_dir_screenshot = os.path.join(home_dir, "ScreenShots")

os.makedirs(home_dir, exist_ok=True)
os.makedirs(home_dir_screenshot, exist_ok=True)

goodFiscalSituation = "Situação Fiscal Regularizada"
financas_login_page = "https://www.acesso.gov.pt/v2/loginForm?partID=PFAP&path=/geral/dashboard"


email_provider_list = {
   "gmail": "smtp.gmail.com"
}

# Controller Functions

def LoginWithCredentials(driver):
    config_file_path = os.path.join(home_dir,"config.json")
    # Loading Configuration to memory
    with open(config_file_path) as f:
        data = json.load(f)

    nif = data['user_nif']
    password = data['user_password']
    print(f'Logging in NIF: {nif}')

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
    # Clicking on Alerts Menu Butoton
    driver.find_element(By.XPATH,'//*[@id="collapseMenu18"]/ul/li[6]').click()
    wait_until_element_is_present(driver, By.ID, 'alertas-table', 10)

    # Fetching alerts table
    alert_table = driver.find_element(By.ID, 'alertas-table')
    rows = alert_table.find_elements(By.TAG_NAME, 'tr')
    del rows[0]

    # Extracting data from table
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
    # Clicking on Consult Messages Menu Button
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

def NavigateToPagamentos(driver):
    print('Navigating to Payments')

    # Clicking on Pagamentos
    driver.find_element(By.XPATH,'//*[@id="collapseMenu18"]/ul/li[2]').click()
    wait_until_element_is_present(driver, By.ID, 'main-content', 10)

def CheckPayments(driver, payment_type):
    
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
    driver.set_window_size(1920,1080)
    return driver

def ConfigCLI(user_nif, user_password, sender_email, sender_password, recipient_list, email_type):
    config_file_path = os.path.join(home_dir,"config.json")
    try:
        config_obj = {
        "user_nif": user_nif,
        "user_password": user_password,
        "email_provider": email_type,
        "sender_email": sender_email,
        "sender_password": sender_password,
        "recipient_list": recipient_list
        }
        with open(config_file_path, 'w') as outfile:
            json.dump(config_obj, outfile)
        print("CLI successfully configured")
    except:
        print("There was an error while configuring thje CLI")

def CheckConfig(show_password):
    config_file_path = os.path.join(home_dir,"config.json")
    try:
        with open(config_file_path, 'r') as f:
            data = json.load(f)
        nif = data['user_nif']
        password = data['user_password']
        sender_email = data['sender_email']
        sender_password = data['sender_password']
        recipient_list = data['recipient_list']

        print(f'User NIF: {nif}')
        if show_password:
            print(f'User Password: {password}')
        print(f'Sender Email: {sender_email}')
        if show_password:
            print(f'Sender Password: {sender_password}')
        print(f'Email recipient list: {recipient_list}')

        print('Configuration OK')
    except:
        print("CLI is not configured properly")

def SendEmail(subject, body, attach_screenshots):
    config_file_path = os.path.join(home_dir,"config.json")
    with open(config_file_path, 'r') as f:
        data = json.load(f)

    data_file_path = os.path.join(home_dir,"data.json")
    with open(data_file_path, 'r') as f:
        results_data = json.load(f)

    screenshot_paths = find_screenshots(results_data)
    email_provider = email_provider_list[data['email_provider']]
    sender = data['sender_email']
    recipients = data['recipient_list']
    password = data['sender_password']

    print(f'Sending email to {recipients} from {sender} through {email_provider}')

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    msg.attach(MIMEText(body, 'html'))

    for image_path in screenshot_paths:
        with open(image_path, 'rb') as file:
            img = MIMEBase('application', 'octet-stream')
            img.set_payload(file.read())
        encoders.encode_base64(img)
        img.add_header('Content-Disposition', f'attachment; filename= {image_path}')
        msg.attach(img)

    with smtplib.SMTP_SSL(email_provider, 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Email sent!")

def GenerateEmailBody():
    data_file_path = os.path.join(home_dir,"data.json")
    with open(data_file_path, 'r') as f:
        data = json.load(f)
    
    html = """
<html>
<body>
    """

    if "fiscal_situation" in data:
        new_html = f"""
            <div>
            <b><h1>Fiscal Situation:</h1></b>
                <div>
                    State: {data['fiscal_situation']['state']} | {data['fiscal_situation']['literal']}
                </div>
            </div>
        """
        html = html + new_html

    if "current_alerts" in data:
        new_html = f"""
            <div>
            <b><h1>Current Alerts:</h1></b>
                {create_html_table(data["current_alerts"]["alerts"])}
            </div>
        """
        html = html + new_html
    
    if "current_messages" in data:
        new_html = f"""
            <div>
            <b><h1>Current Messages:</h1></b>
                {create_simple_list(data["current_messages"]["messages"])}
            </div>
        """
        html = html + new_html

    if "current_interactions" in data:
        new_html = f"""
            <div>
            <b><h1>Current Interactions:</h1></b>
                {create_html_table(data["current_interactions"]["interactions"])}
            </div>
        """
        html = html + new_html

    if "payments" in data:
        html += "<b><h1>Payments:</h1></b>"
        if "current_payments" in data["payments"]:
            new_html = f"""
            <div>
            <b><h3>Current Payments:</h3></b>
                {create_html_table(data["payments"]["current_payments"]["payments"])}
            </div>
        """
        html = html + new_html

        if "missing_payments" in data["payments"]:
            new_html = f"""
            <div>
            <b><h3>Missing Payments:</h3></b>
                {create_html_table(data["payments"]["missing_payments"]["payments"])}
            </div>
        """
        html = html + new_html

        if "refund_payments" in data["payments"]:
            new_html = f"""
            <div>
            <b><h3>Refund Payments:</h3></b>
                {create_html_table(data["payments"]["refund_payments"]["payments"])}
            </div>
        """
        html = html + new_html

    end_of_html = """
    </body>
    </html>
    """

    html = html + end_of_html

    return html

def create_simple_list(data):
    html = "<div style='font-family: Arial;'>"
    html += "<ul style='list-style-type: disc; padding-left: 20px;'>"
    for item in data:
        html += "<li style='color: #333; font-size: 1.2em; margin-bottom: 10px;'>" + item + "</li>"
    html += "</ul>"
    html += "</div>"
    return html

def create_html_table(data):
    html = "<table style='border: 1px solid #ddd; border-collapse: collapse; width: 100%;'>\n"
    # Add table headers
    html += "<tr style='background-color: #f9f9f9;'>\n"
    for key in data[0].keys():
        html += "<th style='border: 1px solid #ddd; padding: 15px; text-align: left; font-size: 1.2em;'>{}</th>\n".format(key)
    html += "</tr>\n"
    # Add table data
    for row in data:
        html += "<tr>\n"
        for value in row.values():
            html += "<td style='border: 1px solid #ddd; padding: 15px; text-align: left; font-size: 1.2em;'>{}</td>\n".format(value)
        html += "</tr>\n"
    html += "</table>"
    return html

def SetupRootFolder():
    try:
        data_file_path = os.path.join(home_dir, "data.json")
        os.remove(data_file_path)
    except:
        print("No data file to remove")

def find_screenshots(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'screenshot':
                yield value
            else:
                yield from find_screenshots(value)
    elif isinstance(data, list):
        for item in data:
            yield from find_screenshots(item)

