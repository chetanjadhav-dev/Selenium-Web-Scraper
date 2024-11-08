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
