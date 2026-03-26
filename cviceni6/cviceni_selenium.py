import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth

r_clean = re.compile(r'[^\d,]+')

options = Options()
# Stabilní headless režim pro běh v Linux kontejneru
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
options.add_argument("--window-size=1920,915")

driver = webdriver.Chrome(options=options)

from selenium_stealth import stealth
stealth(driver, languages=["en-US"], vendor="Google Inc.", platform="Win32",
        webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine", fix_hairline=True)

from_iata = 'VIE'
to_iata = 'TFS'
departure_date = '2025-04-03'
return_date = '2025-04-08'


#url = f'https://www.ryanair.com/cz/cs/booking/home/{from_iata}/{to_iata}/{departure_date}/{return_date}/1/0/0/0'
#url = f'https://www.wizzair.com/en-gb/booking/select-flight/{from_iata}/{to_iata}/{departure_date}/{return_date}/1/0/0/null'
url = 'https://www.pelikan.cz/cs/akcni-letenky/'
driver.get(url)

#time.sleep(5)

print(driver.title)

try:
    try:
        cookie_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "codeblocks-accept-cookies"))
        )
        print("Klikám na 'Přijmout všechny cookies'...")
        cookie_button.click()
    except:
        print("Tlačítko 'Přijmout cookies' se nezobrazilo.")

    time.sleep(1)
    driver.save_screenshot("screenshot.png")


    # test if there is departure element
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "calendar-item-info-action"))
    )

    print("Načteny ceny...")

    items = driver.find_elements(By.CLASS_NAME, "calendar-item-info-action")

    print(f"Nelezeno ")

    if items:
        print(f"Nalezeno {len(items)} cen:")
        for i, p in enumerate(items, 1):
            text = p.text.strip()
            if text:
                print(f"Cena #{i}: {text}")
    else:
        print("Žádné ceny nebyly nalezeny.")

except Exception as e:
    print("Chyba při získávání dat:", e)

driver.quit()