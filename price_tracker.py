from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class Revolution:

    def __init__(self, name, known):
        self.followers = 0
        self.name = name
        self.known = known
        self.speciality = 0
        self.verified = "False"

    def method1(self,url):
       
       # Configure Chrome options for headless mode
       chrome_options = Options()
       chrome_options.add_argument('--headless')  # Runs Chrome in headless mode
       chrome_options.add_argument('--disable-gpu')  # Disables GPU hardware acceleration 
       options = webdriver.ChromeOptions()
       options.add_experimental_option("detach", True)
       driver = webdriver.Chrome(options=chrome_options,service=Service(ChromeDriverManager().install()))
       driver.get(url)
    #    driver.find_element(By.TAG_NAME, "a").click()
       price = driver.find_element(By.CLASS_NAME,"a-price-whole")
       new_price = price.text
       num_str_without_comma = new_price.replace(',', '') 
       dot = num_str_without_comma.replace('.', '') 

       driver.quit()
       return dot
            
    def method2(self):
        if self.followers >= 1000:
            self.speciality = True