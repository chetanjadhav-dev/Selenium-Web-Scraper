# Selenium Web Scraper

This project is a Selenium-based web scraper designed to automate data extraction from the Yokohama Tire Selector website, specifically retrieving and saving structured information about tire designs for specified brands.

## Project Overview

The scraper navigates through the Yokohama Off-Highway Tires website, selects specific brands and designs, extracts table data (both metric and imperial units), and saves it in a structured CSV format. Users can input desired brand names and tire designs to automate data collection.

## Features

- **Dynamic Brand and Design Selection**: Allows users to input a brand and design to scrape data for specific configurations.
- **Table Data Extraction**: Collects data tables in both metric (mm) and imperial (inch) units.
- **Folder and File Organization**: Automatically creates a folder for each selected brand and stores design-specific data as CSV files.
- **Error Handling**: Includes basic error handling for missing elements or driver issues.

## Prerequisites

1. **Python 3.x**
2. **Selenium Library**: Install using `pip install selenium`.
3. **ChromeDriver**: Ensure ChromeDriver matches your Chrome version. Update `driver_path` in the `main()` function to the ChromeDriver path on your local machine.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/chetanjadhav-dev/Selenium-Web-Scraper.git
   ```
2. **Navigate to the repository**:
   ```bash
   cd Selenium-Web-Scraper
   ```
3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the script**:
   ```bash
   python data_extraction.py
   ```
2. **Input Brand and Design**:
   - Enter the desired brand name (e.g., `ALLIANCE`, `GALAXY`, `PRIMEX`).
   - Enter the tire design (e.g., `350`).

3. **Output**:
   - Extracted data is stored in CSV files within folders named by brand.

## Error Handling

- If the ChromeDriver is not available, or if there are issues finding elements on the page, the script will print an error message with details on what went wrong.

## Project Structure

```plaintext
Selenium-Web-Scraper/
├── data_extraction.py          # Main script to run the scraper
├── README.md           # Project overview and instructions
└── requirements.txt    # Required libraries
```

## Customization

You can modify the `main()` function to customize the scraping process or adapt it for additional websites.

## Contributing

Feel free to fork the repository and submit pull requests to enhance functionality or improve performance.

## License

This project is open-source and available under the MIT License.
```

This format ensures consistency across all sections for a clean, professional look.
