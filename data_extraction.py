from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os

def setup_driver(driver_path):
    """
    Set up the Chrome WebDriver.
    """
    service = Service(executable_path=driver_path)
    return webdriver.Chrome(service=service)

def wait_and_click(driver, by, value, timeout=10):
    """
    Wait for an element to be clickable and click it.
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        element.click()
    except Exception as e:
        print(f"Element not found or could not be clicked: {str(e)}")

def get_select_elements(driver, by, value, timeout=10):
    """
    Wait for and return all elements matching the selector.
    """
    try:
        elements = WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((by, value))
        )
        return elements
    except Exception as e:
        print(f"Elements not found: {str(e)}")
        return []

def get_designs(designs_list, available_designs):
    """
    Filter and return the selected designs from the available designs list.
    """
    selected_designs = []
    for design in available_designs:
        if design.text in designs_list:
            selected_designs.append(design)
    return selected_designs

def collect_table_info(driver, div_class):
    """
    Collect both table headers and data based on the specified div class.
    """
    try:
        data_div = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f'//div[@class="{div_class} "]'))
        )
        tables = data_div.find_elements(By.XPATH, './/table[@id="tblResultView"]')
        if div_class == 'data_in_inch':
            driver.execute_script("arguments[0].style.display = 'block';", data_div)
        
        table_info = {}
        for i, table in enumerate(tables):
            header_rows = table.find_element(By.TAG_NAME, 'thead').find_elements(By.TAG_NAME, 'tr')
            headers_dict = {index: row.find_elements(By.TAG_NAME, 'th') for index, row in enumerate(header_rows) if index != 3}
            headers_text = {
                index: {i: th.text for i, th in enumerate(th_list)}
                for index, th_list in headers_dict.items()
            }
            
            table_data_rows = table.find_elements(By.TAG_NAME, 'tbody')[0].find_elements(By.TAG_NAME, 'tr')
            data_rows = [{i: td.text for i, td in enumerate(row.find_elements(By.TAG_NAME, 'td'))} for row in table_data_rows]
            
            table_info[f"Table_{i+1}"] = {
                    "headers": headers_text,
                    "data": data_rows
                }
        
        return table_info
    
    except Exception as e:
        print(f"An error occurred while fetching tables: {str(e)}")
        return {}

def extract_headers(table):
    """
    Extracts and processes the headers from the table.
    """
    row1 = [text.replace('\n', ' ') for text in list(table[0].values())]
    row2 = list(table[1].values())
    row3 = list(table[2].values())
    row4 = [text.replace('\n', ' ') for text in list(table[4].values())]
    
    return row1, row2, row3, row4

def create_multi_index(row1, row2, row3, row4):
    """
    Creates a multi-level index for DataFrame columns based on the headers.
    """
    tuples = []
    for col in row1:
        if col == 'Unloaded Dimension':
            tuples.extend([(col, '', '', row4[0]), (col, '', '', row4[1])])
        elif col == 'Recommended Load':
            tuples.extend([(col, row2[0], row3[0], subcol) for subcol in row4[2:]])
        else:
            tuples.append((col, '', '', ''))
    
    return pd.MultiIndex.from_tuples(tuples)

def create_dataframe(headers, sample_data):
    """
    Creates a DataFrame from the processed headers and sample data.
    """
    row1, row2, row3, row4 = extract_headers(headers)
    columns = create_multi_index(row1, row2, row3, row4)
    return pd.DataFrame(sample_data, columns=columns)

def process_table(table_info, table_key):
    columns = table_info[table_key]['headers']
    table_data = table_info[table_key]['data']

    dr1 = [text.replace('\n', ' ') for text in list(table_data[0].values())]
    data_rows = [dr1]

    for i, dr in enumerate(table_data[1:], start=2):
        drs = globals()[f'dr{i}'] = [''] * 7 + list(dr.values())
        data_rows.append(drs)

    return create_dataframe(columns, data_rows)

def save_to_csv(df, filename):
    """
    Saves the DataFrame to a CSV file.
    """
    df.to_csv(filename, index=False)
    print(f"CSV file '{filename}' saved successfully.")

def main():
    # Configuration
    website = "https://yokohama-atg.com/usa/tire-selector-yokohama-off-highway-tires/"
    driver_path = "C:\\Users\\cheta\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"  # Change according to your PC's file path
    # my_designs = ['350']
    my_brands = input('Enter brand name: ').upper()
    my_designs = input('Enter the design values: ')

    brands_names = {'ALLIANCE': 0, 'GALAXY': 1, 'PRIMEX': 2}
    brand = brands_names[my_brands]
    folder = my_brands.capitalize()

    if not os.path.exists(folder):
        os.mkdir(folder)

    try:
        # Initialize WebDriver
        driver = setup_driver(driver_path)
        driver.get(website)

        # Accept cookies
        wait_and_click(driver, By.XPATH, '//span[@data-cookie-set="accept"]')

        # Select brand
        select_buttons = get_select_elements(driver, By.XPATH, '//span[@class="select2-arrow"]')
        brands_button = select_buttons[2]
        brands_button.click()
        brands = get_select_elements(driver, By.XPATH, '//li[@class="select2-results-dept-0 select2-result select2-result-selectable"]')
        brands[brand].click()

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

        # Collect data for both mm and inch tables
        international_table_info = collect_table_info(driver, "data_in_mm")
        usa_table_info = collect_table_info(driver, "data_in_inch")

        # Process and save international tables
        table1_mm = process_table(international_table_info, 'Table_1')
        save_to_csv(table1_mm, os.path.join(folder, 'table1_mm.csv'))

        table2_mm = process_table(international_table_info, 'Table_2')
        save_to_csv(table2_mm, os.path.join(folder, 'table2_mm.csv'))

        # Process and save USA tables
        table1_inch = process_table(usa_table_info, 'Table_1')
        save_to_csv(table1_inch, os.path.join(folder, 'table1_inch.csv'))

        table2_inch = process_table(usa_table_info, 'Table_2')
        save_to_csv(table2_inch, os.path.join(folder, 'table2_inch.csv'))

    finally:
        time.sleep(5)
        driver.quit()
        print("Data extraction and processing complete.")

if __name__ == "__main__":
    main()
