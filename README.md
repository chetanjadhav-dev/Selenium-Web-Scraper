
2. Navigate to the project directory:
   ```sh
   cd selenium-web-scraper
   ```
3. Install the required Python packages:
   ```sh
   pip install -r requirements.txt
   ```

### Configuration

1. Download and install [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) and place it in a known location.
2. Update the `path` variable in the script to point to your ChromeDriver executable.

## Usage

1. Modify the `my_designs` and `folder` variables in the script to suit your needs.
2. Run the script:
   ```sh
   python scraper.py
   ```

## Code Overview

The script performs the following steps:

1. Sets up the Selenium WebDriver and opens the target website.
2. Waits for and clicks the cookie accept button.
3. Selects the required brand and design from dropdown menus.
4. Initiates a search and waits for the results to load.
5. Extracts the data from the resulting tables and prints them.
6. Handles any exceptions and ensures the browser is closed after execution.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
```

Feel free to modify it as per your specific project details and requirements.
