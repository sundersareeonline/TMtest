from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def driversetup():
        options = webdriver.EdgeOptions()
        options.add_argument("--headless")

        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()),options=options)
        driver.maximize_window()
        driver.implicitly_wait(10)
    
        return driver