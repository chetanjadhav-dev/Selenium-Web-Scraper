from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

website = "https://yokohama-atg.com/usa/tire-selector-yokohama-off-highway-tires/"
path = "C:\\Users\\cheta\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"  # Change according to your pc's file path
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)

my_designs = ['350']

folder = 'Alliance'

if not os.path.exists(folder):
    os.mkdir(folder)

try:
    driver.get(website)

    # Wait for the cookie accept button and click it
    try:
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@data-cookie-set="accept"]'))
        )
        accept_button.click()
    except Exception as e:
        print(f"Cookie notice not found or could not be clicked: {str(e)}")

    print('working...')
    
    # Click on the brand select button
    select_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//span[@class="select2-arrow"]'))
    )
    brands_button = select_buttons[2]
    brands_button.click()

    # Select the brand
    select_brands = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//li[@class="select2-results-dept-0 select2-result select2-result-selectable"]'))
    )
    select_brands[0].click()

    # Wait for the loader to disappear
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element((By.XPATH, '//div[@class="loader-wrapper"]'))
    )

    # Click on the design select button
    select_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//span[@class="select2-arrow"]'))
    )
    design_button = select_buttons[3]
    design_button.click()

    select_design = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//li[@class="select2-results-dept-0 select2-result select2-result-selectable"]'))
    )

    def get_design(values):
        new_design = []

        if isinstance(values, str):
            values = [values]

        for des in select_design:
            if des.text in values:
                new_design.append(des)
                print(des.text)

        return new_design

    designs = get_design(my_designs)
    print(designs)
    for design in designs:
        print(f'For Design: {design.text}')
        design.click()

        # Click the search button
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@title="Search"]'))
        )
        search_button.click()
        print('Search...')

        # Try finding tables with both class names
        try:
            find_tables = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class=" table-responsive"]'))
            )
            print('We found tables with class=" table-responsive"!')
        except:
            try:
                find_tables = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@class="table-responsive"]'))
                )
                print('We found tables with class="table-responsive"!')
            except Exception as e:
                print(f"An error occurred while fetching tables: {str(e)}")
                continue

        try:
            tables = find_tables.find_elements(By.XPATH, '//table[@id="tblResultView"]')
            if len(tables) > 1:
                table1 = tables[0]
                table2 = tables[1]
                print('\n')
                print('Table 1')
                print(table1.text)
                print()
                print('\n')
                print('Table 2')
                print()
                print(table2.text)
                print('\n')
            else:
                table = tables[0]
                print('\n')
                print('Table')
                print('\n')
                print(table.text)
        except Exception as e:
            print(f"An error occurred while processing tables: {str(e)}")

finally:
    time.sleep(10)
    driver.quit()
    print("All data has been collected and the browser is closed.")
