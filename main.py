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

    def _initScrape(self):
        driver = self.driver
        driver.get('https://www.google.com/')
        driver.maximize_window()

        search_bar = driver.find_element(By.XPATH, '//input[@name="q"]')

        search_bar.click()
        search_bar.clear()
        search_bar.send_keys('centros de rehabilitacion mexico')
        search_bar.submit()

        #esperamos a que se muestre el botón de "mostrar más"
        WebDriverWait(driver,15).until(EC.presence_of_element_located((By.XPATH,'//g-more-link')))
        
        show_button = driver.find_element(By.XPATH, '//g-more-link/a')

        show_button.click()

        #encontramos la lista de elemenos para luego procesarla con xpath
        places_data = driver.find_elements(By.XPATH,'//div[@class="rl_tile-group"]/div[@class and @jscontroller and @jsaction]//a[contains(@class,"a-no-hover-decoration")]')

        data = {'nombre':[],'telefono':[],'pais':[],'direccion':[]}

        for i in places_data:
            i.click()
            time.sleep(2)

            name = driver.find_element(By.XPATH,'//div[@class="immersive-container"]//h2/span').text
            try:
                direction = driver.find_elements(By.XPATH,'//div[@class="immersive-container"]//div[@style]//div[@data-dtype]/span')[1].text
                data['direccion'].append(direction)
            except NoSuchElementException:
                data['direccion'].append('No disponible')
            try:    
                phone = driver.find_element(By.XPATH,'//div[@class="immersive-container"]//a[@jsdata]/span').text
                data['telefono'].append(phone)
            except NoSuchElementException:
                data['telefono'].append('No disponible')
            data['nombre'].append(name)
            data['pais'].append('Mexico')
    
        df = pd.DataFrame(data,columns=['nombre','telefono','pais','direccion'])
        return df

    def _scrape(self,name):
        driver = self.driver

        search_bar = driver.find_element(By.XPATH, '//input[@name="q"]')
        search_bar.click()
        search_bar.clear()
        search_bar.send_keys(name)
        search_bar.submit()

        #esperamos a que se muestre un elemento
        WebDriverWait(driver,15).until(EC.presence_of_element_located((By.XPATH,'//div[@class="rl_tile-group"]/div[@class and @jscontroller and @jsaction]')))

        places_data = driver.find_elements(By.XPATH,'//div[@class="rl_tile-group"]/div[@class and @jscontroller and @jsaction]//a[contains(@class,"a-no-hover-decoration")]')
        data = {'nombre':[],'telefono':[],'pais':[],'direccion':[]}

        for i in places_data:
            i.click()
            time.sleep(2)

            name = driver.find_element(By.XPATH,'//div[@class="immersive-container"]//h2/span').text
            try:
                direction = driver.find_elements(By.XPATH,'//div[@class="immersive-container"]//div[@style]//div[@data-dtype]/span')[1].text
                data['direccion'].append(direction)
            except NoSuchElementException:
                data['direccion'].append('No disponible')
            try:    
                phone = driver.find_element(By.XPATH,'//div[@class="immersive-container"]//a[@jsdata]/span').text
                data['telefono'].append(phone)
            except NoSuchElementException:
                data['telefono'].append('No disponible')
            data['nombre'].append(name)
            data['pais'].append('Mexico')
    
        df = pd.DataFrame(data,columns=['nombre','telefono','pais','direccion'])
        return df  

    def begin(self):
        driver = self.driver

        df1 = self._initScrape()
        df2 = self._scrape('directorio de centros de rehabilitacion mexico')
        df3 = self._scrape('directorios de rehabilitacion mexico')

        frames = [df1,df2,df3]
        result = pd.concat(frames)
        result.to_excel(os.path.join(os.getcwd(),'rehab_mx.xlsx'),index=False,header=True)
        print('Succesfully scraped the required data')

        driver.quit()

if __name__ == '__main__':
    scraper = Scraper()
    scraper.begin()