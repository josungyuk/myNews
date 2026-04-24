from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from contextlib import contextmanager
import requests, random

def get_page_driver(driver, url: str) -> str:
    driver.get(url)

    return driver.page_source

@contextmanager
def driver_provider() -> webdriver.Chrome:
    driver = None
    try:
        options = Options()
        options.add_argument("--incognito")
        driver = webdriver.Chrome(options=options)
        yield driver
    finally:
        if driver is not None:
            driver.quit()

def fetch_html(url: str) -> str | None:
    headers = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Mozilla/5.0"
        ]
    
    try:
        result = requests.get(url, headers={"User-Agent": random.choice(headers)}, timeout=60)
        result.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(f"[Error] {url}에서 {e} 발생")
        return None

    return result.text