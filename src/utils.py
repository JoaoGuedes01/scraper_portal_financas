from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

goodFiscalSituation = "Situação Fiscal Regularizada"
financas_login_page = "https://www.acesso.gov.pt/v2/loginForm?partID=PFAP&path=/geral/dashboard"

# Util Functions
def wait_for_element(driver, element_id, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, element_id))
        )
        print(f'successfully found {element_id}')
        print(element.text)
    except TimeoutException:
        print(f"Timed out waiting for element with id {element_id} to load")

def wait_for_element_by_text(driver, element_text, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.LINK_TEXT, element_text))
        )
        print(f'successfully found {element_text}')
        print(element.text)
    except TimeoutException:
        print(f"Timed out waiting for element with id {element_text} to load")

def wait_for_element_text_change(driver, xpath, undesired_text, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(
            lambda driver: driver.find_element(By.XPATH, xpath).text != undesired_text
        )
    except TimeoutException:
        print(f"Timed out waiting for element with text different from {undesired_text}")


# Controller Functions

def LoginWithCredentials(driver, nif, password):
    print(f'Loggin in NIF: {nif}')

    driver.get(financas_login_page)

    tabs = driver.find_elements(By.CLASS_NAME, 'tab-label')
    for tab in tabs:
        spans = tab.find_elements(By.TAG_NAME, 'span')
        for span in spans:
            if span.text == 'NIF':
                span.click()

    driver.find_element(By.ID, 'input-username-nif-group').find_element(By.CLASS_NAME, 'input-container').find_element(By.TAG_NAME, 'input').send_keys(nif)

    driver.find_element(By.ID, 'input-password-nif-group').find_element(By.CLASS_NAME, 'pw-input-container').find_element(By.TAG_NAME, 'input').send_keys(password)

    driver.find_element(By.XPATH, '//*[@id="sbmtLogin"]').click()
    wait_for_element(driver, 'cumprimento', 10)
    print('successful login')

def NavigateToMyArea(driver):
    print('Navigating to My Area')
    print('CHANGE')
    driver.find_element(By.CLASS_NAME, 'user-area').click()
    wait_for_element_by_text(driver, 'A Minha Área', 10)
    wait_for_element_text_change(driver, '//*[@id="brief-title"]', 'Em Actualização...', 10)

def CheckFiscalSituationText(driver):
    situation = driver.find_element(By.XPATH, '//*[@id="brief-title"]').text
    if situation == goodFiscalSituation:
        print(f"GOOD | {situation}")
    else:
        print(f"BAD | {situation}")

def CreateDriver(headless):
    options = Options()
    if headless:
        options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver