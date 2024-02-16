# STF Web Scraper

This Python script scrapes data from the Supremo Tribunal Federal (STF) website jurisprudencia.stf.jus.br. It utilizes Playwright for browser automation and Selectolax for HTML parsing.

## Pre requisites

Before running the script, make sure you have the following installed:

- Python 3.x
- Playwright Python library (`playwright`)
- BeautifulSoup Python library (`BeautifulSoup`)
- [Browser](https://playwright.dev/python/docs/browsers)

You can install the dependencies using pip:

```bash
pip install playwright beautifulsoup4
```

You can install the Chromium using apt-get:

```bash
sudo apt-get install chromium
```

## Usage

1. Clone this repository to your local machine:

```bash
git clone https://github.com/mvdiogo/stf-web-scraper.git
```

2. Navigate to the project directory:

```bash
cd stf-web-scraper
```

3. Run the script:

```bash
python app.py
```

4. The script will launch a browser window, navigate to the STF website, scrape the data based on the specified base and subject, and print the results to the console.

## Contributing

Contributions are welcome! If you find any issues or want to add new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
