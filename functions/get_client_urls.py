from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time, requests, json, os

def get_client_url(auth_token, GUACAMOLE_URL):
    guacamole_url = f"{GUACAMOLE_URL}/#/?token={auth_token}"

    display = Display(visible=0, size=(800, 600))
    display.start()

    options = Options()
    options.headless = True

    abspath = os.path.abspath('functions/geckodriver')
    driver_service = Service(abspath)
    driver = webdriver.Firefox(service=driver_service, options=options)

    driver.get(guacamole_url)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    specific_links = [link['ng-href'] for link in soup.find_all('a', class_='home-connection ng-scope') if link.has_attr('ng-href') and link['ng-href'].startswith('#/client/')]

    display.stop()
    driver.quit()

    return specific_links
