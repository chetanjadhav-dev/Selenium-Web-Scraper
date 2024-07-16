from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import csv

website = "https://yokohama-atg.com/usa/tire-selector-yokohama-off-highway-tires/"
path = "C:\\Users\\cheta\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"  # Change according to your PC's file path
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
        return new_design

    designs = get_design(my_designs)
    for design in designs:
        print(f'For Design: {design.text}')
        design.click()

        # Click the search button
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@title="Search"]'))
        )
        search_button.click()
        print('Search...')

        # Wait for tables to become visible
        try:
            # Find the parent div element containing the tables you're interested in
            data_in_mm = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="data_in_mm "]'))
            )

            # Find all tables within the parent div
            tables_mm = data_in_mm.find_elements(By.XPATH, './/table[@id="tblResultView"]')

            for i, table in enumerate(tables_mm):
                # Extract header row
                header_row = table.find_element(By.TAG_NAME, 'thead').find_elements(By.TAG_NAME, 'tr')
                speeds = header_row[-1].find_elements(By.TAG_NAME, 'th')
                print(f'Table {i+1}:\n\n', 'tr 1:\n\n',header_row[0].text, '\n\ntr 2:\n\n', header_row[1].text, '\n\ntr 3:\n\n', header_row[2].text, '\n\ntr 4:\n\n', [speed.text for speed in speeds])
                print()
                print('end...')
                print()

            # Print tables for demonstration
            if len(tables_mm) > 1:
                for i, table in enumerate(tables_mm):
                    table_html = table.text
                    print()
                    print(f'Table {i+1} for "International Standard (mm - bar - kg - kmph)":\n\n', table_html)
                    print()
            else:
                print('Tables not found!!!')

            data_in_inch = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="data_in_inch "]'))
            )

            # Find all table elements within the parent div
            tables_inch = data_in_inch.find_elements(By.XPATH, './/table[@id="tblResultView"]')

            # Execute JavaScript to change the display style to block (making it visible)
            driver.execute_script("arguments[0].style.display = 'block';", data_in_inch)

            # Print the HTML content of each table for demonstration
            if len(tables_inch) > 1:
                for i, table in enumerate(tables_inch):
                    table_html = table.text
                    print()
                    print(f'Table {i+1} for "US Standard (inch - psi - lbs - mph)"):\n\n', table_html)
                    print()
            else:
                print('tables not found!!!')

        except Exception as e:
            print(f"An error occurred while fetching tables 'tblResultView': {str(e)}")



finally:
    time.sleep(10)
    driver.quit()
    print("All data has been collected and the browser is closed.")