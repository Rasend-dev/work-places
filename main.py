import time
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException

class Scraper():
    
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path= 'chromedriver.exe')

    def _initScrape(self,search):
        driver = self.driver
        driver.get('https://www.google.com/')
        driver.maximize_window()

        search_bar = driver.find_element(By.XPATH, '//input[@name="q"]')

        search_bar.click()
        search_bar.clear()
        search_bar.send_keys(search)
        search_bar.submit()

        #esperamos a que se muestre el botón de "mostrar más"
        WebDriverWait(driver,15).until(EC.presence_of_element_located((By.XPATH,'//g-more-link')))
        
        show_button = driver.find_element(By.XPATH, '//g-more-link/a')

        show_button.click()

        #encontramos la lista de elemenos para luego procesarla con xpath
        available_pages = driver.find_elements(By.XPATH,'//tbody/tr/td/a')

        data = {'nombre':[],'telefono':[],'direccion':[],'ciudad':[],'pais':[]}

        for i in range(9):
            places_data = driver.find_elements(By.XPATH,'//div[@class="rl_tile-group"]/div[@class and @jscontroller and @jsaction]//a[contains(@class,"a-no-hover-decoration")]')
            next_page = driver.find_element(By.XPATH,'//tbody/tr/td[@class]/a[@id="pnnext"]')
            for d,x in enumerate(places_data):
                x.click()
                time.sleep(2.3)
                try:
                    name = driver.find_element(By.XPATH,'//div[@class="immersive-container"]//h2/span').text
                except NoSuchElementException:
                    name = driver.find_element(By.XPATH,f'//div[@class="rl_tile-group"]/div[@class and @jscontroller and @jsaction]//a[contains(@class,"a-no-hover-decoration")]//div[@role="heading"]/span[{d}]').text
                    print(name,'nombre encontrado')
                try:
                    direction = driver.find_elements(By.XPATH,'//div[@class="immersive-container"]//div[@style]//div[@data-dtype]/span') 
                    if direction:
                        raw = direction[1].text.split(',')
                        city = raw[len(raw) - 2]
                        clean_direction = ','.join(raw[:len(raw)-2])
                        data['ciudad'].append(city)
                        data['direccion'].append(clean_direction)
                    else:
                        data['ciudad'].append('No disponible')
                        data['direccion'].append('No disponible')    
                except NoSuchElementException:
                    data['direccion'].append('No disponible')

                try:    
                    phone = driver.find_element(By.XPATH,'//div[@class="immersive-container"]//a[@jsdata]/span').text
                    data['telefono'].append(phone)
                except NoSuchElementException:
                    data['telefono'].append('No disponible')

                data['nombre'].append(name)
                data['pais'].append('Mexico')

            next_page.click()
            time.sleep(2.3)

        df = pd.DataFrame(data,columns=['nombre','telefono','direccion','ciudad','pais'])
        return df

    def begin(self,search,filename):
        driver = self.driver
        df = self._initScrape(search)
        df.to_excel(os.path.join(os.getcwd(),f'{filename}.xlsx'),index=False,header=True)
        print('Succesfully scraped the required data')

        driver.quit()

if __name__ == '__main__':
    search = str(input('Que deseas buscar?: \n'))
    filename = str(input('Que nombre deseas darle al archivo?: \n'))
    scraper = Scraper()
    scraper.begin(search,filename)