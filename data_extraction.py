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
    

def collect_filtered_data(driver, div_class):
    """
    Collect filtered data from tables based on the specified div class.
    """
    try:
        data_div = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f'//div[@class="{div_class} "]'))
        )
        tables = data_div.find_elements(By.XPATH, './/table[@id="tblResultView"]')
        if div_class == 'data_in_inch':
            driver.execute_script("arguments[0].style.display = 'block';", data_div)
        
        table_data = []
        
        xpath_expression = f'//tbody/tr[./td[@style="color:#a30e13 !important"]]'
        table_unit = {'data_in_mm': 'tables_mm', 'data_in_inch': 'tables_inch'}

        if table_unit[div_class] == 'tables_mm':

            table_info = {}

            for i, table in enumerate(tables):

                header_rows = table.find_element(By.TAG_NAME, 'thead').find_elements(By.TAG_NAME, 'tr')
                headers_dict = {index: row.find_elements(By.TAG_NAME, 'th') for index, row in enumerate(header_rows) if index != 3}
                headers_text = {
                    index: {i: th.text for i, th in enumerate(th_list)}
                    for index, th_list in headers_dict.items()
                }

                table_data_in_mm = table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')

                data_rows = [{i: td.text for i, td in enumerate(table_data_in_mm[0].find_elements(By.TAG_NAME, 'td'))}]
                data_row = {k: data_rows[0][k] for k in range(7)}

                filtered_data = {}
                for index, tr in enumerate(table_data_in_mm):
                    filter_list = tr.find_elements(By.XPATH, xpath_expression)
                    for idx, ftr in enumerate(filter_list):
                        filtered_data[idx] = ftr.text

                data = filtered_data[i]
                table_data.append({0: data})
                
                print(f'Table_{i+1} Data Collected')

                processed_data = [
                    {
                        i: {j: txt for j, txt in enumerate(td.split(' '))}
                        for i, td in table.items()
                    }
                    for table in table_data
                ]

                table_info[f"Table_{i+1}"] = {
                    "headers": headers_text,
                    "data": [data_row, processed_data[i]]
                }

            return table_info

        else:
            table_info = {}

            for i, table in enumerate(tables):

                header_rows = table.find_element(By.TAG_NAME, 'thead').find_elements(By.TAG_NAME, 'tr')
                headers_dict = {index: row.find_elements(By.TAG_NAME, 'th') for index, row in enumerate(header_rows) if index != 3}
                headers_text = {
                    index: {i: th.text for i, th in enumerate(th_list)}
                    for index, th_list in headers_dict.items()
                }

                table_data_in_inch = table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')
                data_rows = [{i: td.text for i, td in enumerate(table_data_in_inch[0].find_elements(By.TAG_NAME, 'td'))}]
                data_row = {k: data_rows[0][k] for k in range(7)}

                filtered_data = {}
                for index, tr in enumerate(table_data_in_inch, start=2):
                    filter_list = tr.find_elements(By.XPATH, xpath_expression)
                    for idx, ftr in enumerate(filter_list):
                        filtered_data[idx] = ftr.text

                data = filtered_data[i+2]
                table_data.append({0: data})

                print(f'Table_{i+1} Data Collected')

                processed_data = [
                    {
                        i: {j: txt for j, txt in enumerate(td.split(' '))}
                        for i, td in table.items()
                    }
                    for table in table_data
                ]

                table_info[f"Table_{i+1}"] = {
                    "headers": headers_text,
                    "data": [data_row, processed_data[i]]
                }
        
        return table_info
    
    except Exception as e:
        print(f"An error occurred while fetching tables: {str(e)}")
        return []

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
    try:
        columns = table_info[table_key]['headers']
        table_data = table_info[table_key]['data']

        dr1 = [text.replace('\n', ' ') for text in list(table_data[0].values())]

        if len(dr1) <= 7:
            max_key = max(table_data[0])
            combined_dict = table_data[0].copy()

            for k,v in table_data[1][0].items():
                combined_dict[max_key + 1 + k] = v

            combined_data = list(combined_dict.values())

            data_rows = [combined_data]

            return create_dataframe(columns, data_rows)
        
        else:
            data_rows = [dr1]

        for i, dr in enumerate(table_data[1:], start=2):
            drs = globals()[f'dr{i}'] = [''] * 7 + list(dr.values())
            data_rows.append(drs)

        return create_dataframe(columns, data_rows)
    except Exception as e:
        print(f"An error occurred while fetching tables: {str(e)}")
        return []

def save_to_csv(df, folder, filename):
    """
    Saves the DataFrame to a CSV file.
    """
    try:
        df.to_csv(os.path.join(folder,filename), index=False)
        print(f"CSV file '{filename}' saved successfully.")
    except Exception as e:
        print(f"No Important rows found!!!")

def main():
    # Configuration
    website = "https://yokohama-atg.com/usa/tire-selector-yokohama-off-highway-tires/"
    driver_path = "C:\\Users\\cheta\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"  # Change according to your PC's file path
    # my_designs = '350'
    my_designs = input("Enter the design: ")
    folder = f'Alliance/{my_designs}'

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
        brands[0].click()

        # Wait for the loader to disappear
        WebDriverWait(driver, 10).until(EC.invisibility_of_element((By.XPATH, '//div[@class="loader-wrapper"]')))

        # Select design
        design_button = select_buttons[3]
        design_button.click()
        available_designs = get_select_elements(driver, By.XPATH, '//li[@class="select2-results-dept-0 select2-result select2-result-selectable"]')
        selected_designs = get_designs([my_designs], available_designs)
        if selected_designs:
            selected_designs[0].click()

        wait_and_click(driver, By.XPATH, '//a[@title="Search"]')

        international_data = collect_table_info(driver, "data_in_mm")
        usa_data = collect_table_info(driver, "data_in_inch")

        international_filtered_data = collect_filtered_data(driver, "data_in_mm")
        usa_filtered_data = collect_filtered_data(driver, "data_in_inch")

        inter_table1 = process_table(international_data, 'Table_1')
        save_to_csv(inter_table1, folder, 'inter_table1.csv')

        inter_table2 = process_table(international_data, 'Table_2')
        save_to_csv(inter_table2, folder, 'inter_table2.csv')

        usa_table1 = process_table(usa_data, 'Table_1')
        save_to_csv(usa_table1, folder, 'usa_table1.csv')

        usa_table2 = process_table(usa_data, 'Table_2')
        save_to_csv(usa_table2, folder, 'usa_table2.csv')

        inter_table1_filtered = process_table(international_filtered_data, 'Table_1')
        save_to_csv(inter_table1_filtered, folder, 'inter_table1_filtered.csv')

        inter_table2_filtered  = process_table(international_filtered_data, 'Table_2')
        save_to_csv(inter_table2_filtered, folder, 'inter_table2_filtered.csv')

        usa_table1_filtered  = process_table(usa_filtered_data, 'Table_1')
        save_to_csv(usa_table1_filtered, folder, 'usa_table1_filtered.csv')

        usa_table2_filtered  = process_table(usa_filtered_data, 'Table_2')
        save_to_csv(usa_table2_filtered, folder, 'usa_table2_filtered.csv')

    finally:
        time.sleep(5)
        driver.quit()
        print("Data extraction and processing complete.")

if __name__ == "__main__":
    main()
