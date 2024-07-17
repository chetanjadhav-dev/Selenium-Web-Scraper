from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

website = "https://yokohama-atg.com/usa/tire-selector-yokohama-off-highway-tires/"
path = "C:\\Users\\cheta\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"  # Change according to your PC's file path
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)

my_designs = ['350']
folder = 'Alliance'

if not os.path.exists(folder):
    os.mkdir(folder)

def wait_and_click(driver, by, value, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        element.click()
    except Exception as e:
        print(f"Element not found or could not be clicked: {str(e)}")

def get_select_elements(driver, by, value, timeout=10):
    try:
        elements = WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((by, value))
        )
        return elements
    except Exception as e:
        print(f"Elements not found: {str(e)}")
        return []

def get_designs(designs_list, available_designs):
    selected_designs = []
    for design in available_designs:
        if design.text in designs_list:
            selected_designs.append(design)
    return selected_designs

def collect_table_headers(tables):
    table_data = []
    for i, table in enumerate(tables):
        header_rows = table.find_element(By.TAG_NAME, 'thead').find_elements(By.TAG_NAME, 'tr')
        headers_dict = {index: row.find_elements(By.TAG_NAME, 'th') for index, row in enumerate(header_rows) if index != 3}
        headers_text = {
            index: {i: th.text for i, th in enumerate(th_list)}
            for index, th_list in headers_dict.items()
        }
        table_data.append({f"Table_{i+1}": headers_text})
    return table_data

def collect_data(driver, div_class):
    try:
        data_div = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f'//div[@class="{div_class} "]'))
        )
        tables = data_div.find_elements(By.XPATH, './/table[@id="tblResultView"]')
        if div_class == 'data_in_inch':
            driver.execute_script("arguments[0].style.display = 'block';", data_div)
        return collect_table_headers(tables)
    except Exception as e:
        print(f"An error occurred while fetching tables: {str(e)}")
        return []

try:
    driver.get(website)

    # Accept cookies
    wait_and_click(driver, By.XPATH, '//span[@data-cookie-set="accept"]')

    # Select brand
    select_buttons = get_select_elements(driver, By.XPATH, '//span[@class="select2-arrow"]')
    brands_button = select_buttons[2]
    brands_button.click()
    brands = get_select_elements(driver, By.XPATH, '//li[@class="select2-results-dept-0 select2-result select2-result-selectable"]')
    brands[0].click()

    # Wait for the loader to disappear
    WebDriverWait(driver, 10).until(EC.invisibility_of_element((By.XPATH, '//div[@class="loader-wrapper"]')))

    # Select design
    design_button = select_buttons[3]
    design_button.click()
    available_designs = get_select_elements(driver, By.XPATH, '//li[@class="select2-results-dept-0 select2-result select2-result-selectable"]')
    selected_designs = get_designs(my_designs, available_designs)
    if selected_designs:
        selected_designs[0].click()

    # Click search button
    wait_and_click(driver, By.XPATH, '//a[@title="Search"]')

    # Collect table headers
    headers = {
        "Tables_in_mm": collect_data(driver, "data_in_mm"),
        "Tables_in_inch": collect_data(driver, "data_in_inch")
    }
    print('*'*55)
    print()
    print("Headers Collected:", list(headers.keys()))
    print()
    print('*'*55)

finally:
    time.sleep(5)
    driver.quit()
    print("All data has been collected and the browser is closed.")
